import json
import os
from typing import Dict, List

from openai import OpenAI
from pydantic import BaseModel

from mock_data import Comment, User


class Feature(BaseModel):
    name: str
    description: str


class FeatureAnalysis(BaseModel):
    feature_name: str
    related_comment_ids: List[str]
    sentiment_scores: List[float]  # Corresponds to related_comment_ids
    intensity_scores: List[float]  # Corresponds to related_comment_ids


class FeatureAnalysisResponse(BaseModel):
    analyses: List[FeatureAnalysis]


class PrioritizedFeature(BaseModel):
    name: str
    description: str
    related_comments_count: int
    consensus_weight: float


class PMFReport(BaseModel):
    score: int  # 0-100
    summary: List[str]  # 5-7 bullet points
    validation_text: str  # Short summary


class ProductAnalystAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def mine_features(
        self, comments: List[Comment], project_description: str
    ) -> List[Feature]:
        """
        Extracts potential features from comments.
        """
        comments_text = '\n'.join(f'ID: {c.id}, Text: {c.text}' for c in comments)

        prompt = f"""
        Project Description: {project_description}
        
        Analyze the following user comments and extract potential product features or requirements.
        Focus on features that solve the pains mentioned or fulfill the desires expressed.
        Return a list of distinct features with a name and a short description.
        
        Comments:
        {comments_text}
        """

        class FeaturesResponse(BaseModel):
            features: List[Feature]

        try:
            completion = self.client.beta.chat.completions.parse(
                model='gpt-4o-2024-08-06',
                messages=[
                    {'role': 'system', 'content': 'You are an expert product manager.'},
                    {'role': 'user', 'content': prompt},
                ],
                response_format=FeaturesResponse,
            )
            return completion.choices[0].message.parsed.features
        except Exception as e:
            print(f'Error mining features: {e}')
            return []

    def prioritize_features(
        self, features: List[Feature], comments: List[Comment], users: List[User]
    ) -> List[PrioritizedFeature]:
        """
        Prioritizes features based on Consensus Weight.
        W_consensus = Sum(Credibility * Sentiment * Intensity)
        """
        if not features:
            return []

        comments_map = {c.id: c for c in comments}
        users_map = {u.username: u for u in users}

        comments_text = '\n'.join(f'ID: {c.id}, Text: {c.text}' for c in comments)
        features_text = '\n'.join(
            f'Name: {f.name}, Desc: {f.description}' for f in features
        )

        prompt = f"""
        For each feature listed below, identify which of the provided comments are relevant to it.
        For each relevant comment, assign:
        1. Sentiment Score (-1.0 to 1.0): How positive/supportive is the comment regarding this feature?
        2. Intensity Score (0.0 to 1.0): How strongly does the comment imply the need for this feature?
        
        Features:
        {features_text}
        
        Comments:
        {comments_text}
        """

        try:
            completion = self.client.beta.chat.completions.parse(
                model='gpt-4o-2024-08-06',
                messages=[
                    {'role': 'system', 'content': 'You are an expert data analyst.'},
                    {'role': 'user', 'content': prompt},
                ],
                response_format=FeatureAnalysisResponse,
            )

            analyses = completion.choices[0].message.parsed.analyses

            prioritized = []
            for analysis in analyses:
                # Find the original feature object
                feature_obj = next(
                    (f for f in features if f.name == analysis.feature_name), None
                )
                if not feature_obj:
                    continue

                consensus_weight = 0.0
                valid_comments_count = 0

                for i, comment_id in enumerate(analysis.related_comment_ids):
                    if comment_id not in comments_map:
                        continue

                    comment = comments_map[comment_id]
                    user = users_map.get(comment.author)
                    credibility = user.credibility_score if user else 0.5

                    sentiment = analysis.sentiment_scores[i]
                    intensity = analysis.intensity_scores[i]

                    # Formula: C_u * S * I
                    # Note: If sentiment is negative, it reduces the weight (or makes it negative).
                    # The user prompt says "Consensus weight... feature is important if credible users agree".
                    # So negative sentiment should probably reduce the score if it's "disagreement".
                    # But if it's "I hate X" (current solution) -> Feature "Fix X", then sentiment towards the *need* is positive?
                    # The prompt asks for sentiment "regarding this feature".
                    # If feature is "Offline Mode" and comment is "I hate that it's online only", sentiment towards "Offline Mode" is Positive.
                    # So I'll assume LLM handles this logic.

                    weight = credibility * sentiment * intensity
                    consensus_weight += weight
                    valid_comments_count += 1

                prioritized.append(
                    PrioritizedFeature(
                        name=feature_obj.name,
                        description=feature_obj.description,
                        related_comments_count=valid_comments_count,
                        consensus_weight=round(consensus_weight, 2),
                    )
                )

            # Sort by consensus weight descending
            prioritized.sort(key=lambda x: x.consensus_weight, reverse=True)
            return prioritized

        except Exception as e:
            print(f'Error prioritizing features: {e}')
            return []

    def validate_idea(
        self, prioritized_features: List[PrioritizedFeature], project_description: str
    ) -> PMFReport:
        """
        Generates a PMF Validation Report.
        """
        top_features = prioritized_features[:5]
        features_text = '\n'.join(
            f'- {f.name} (Weight: {f.consensus_weight}, Comments: {f.related_comments_count})'
            for f in top_features
        )

        prompt = f"""
        Project Description: {project_description}
        
        Top Validated Features:
        {features_text}
        
        Based on the validation of these features by credible users, generate a Product-Market Fit (PMF) report.
        1. Assign a PMF Confidence Score (0-100). Be optimistic but realistic based on the weights.
        2. Provide a short summary explaining why the idea is valid.
        3. Provide 5-7 bullet points highlighting the positive aspects confirmed by the data.
        """

        try:
            completion = self.client.beta.chat.completions.parse(
                model='gpt-4o-2024-08-06',
                messages=[
                    {'role': 'system', 'content': 'You are a startup validator.'},
                    {'role': 'user', 'content': prompt},
                ],
                response_format=PMFReport,
            )
            return completion.choices[0].message.parsed
        except Exception as e:
            print(f'Error validating idea: {e}')
            return PMFReport(
                score=0, summary=[], validation_text='Error generating report.'
            )
