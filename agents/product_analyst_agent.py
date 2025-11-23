import os
from typing import List

from openai import OpenAI
from pydantic import BaseModel

from mock_data import Comment, Feature, PMFReport, PrioritizedFeature, User


class FeatureAnalysis(BaseModel):
    feature_id: str
    related_comment_ids: List[str]
    sentiment_scores: List[float]  # Corresponds to related_comment_ids
    intensity_scores: List[float]  # Corresponds to related_comment_ids
    description: str  # Generated description


class FeatureAnalysisResponse(BaseModel):
    analyses: List[FeatureAnalysis]


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
        
        Analyze the following user comments and extract potential product features.
        Return a list of distinct features with a title and a category (e.g., Core, AI, UI/UX, Social, Integrations).
        Assign a unique ID to each feature (e.g., f1, f2...).
        
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
        """
        if not features:
            return []

        comments_map = {c.id: c for c in comments}
        users_map = {u.id: u for u in users}

        comments_text = '\n'.join(f'ID: {c.id}, Text: {c.text}' for c in comments)
        features_text = '\n'.join(
            f'ID: {f.id}, Title: {f.title}, Category: {f.category}' for f in features
        )

        prompt = f"""
        For each feature listed below, identify which of the provided comments are relevant to it.
        For each relevant comment, assign:
        1. Sentiment Score (-1.0 to 1.0): How positive/supportive is the comment regarding this feature?
        2. Intensity Score (0.0 to 1.0): How strongly does the comment imply the need for this feature?
        
        Also, generate a detailed description for each feature based on the user needs.
        
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
                    (f for f in features if f.id == analysis.feature_id), None
                )
                if not feature_obj:
                    continue

                consensus_weight = 0.0
                valid_comments_count = 0
                representative_comments = []

                for i, comment_id in enumerate(analysis.related_comment_ids):
                    if comment_id not in comments_map:
                        continue

                    comment = comments_map[comment_id]
                    user = users_map.get(comment.author)
                    credibility = (
                        user.credibility if user else 50
                    )  # Default 50 if not found

                    sentiment = analysis.sentiment_scores[i]
                    intensity = analysis.intensity_scores[i]

                    # Normalize credibility to 0-1 for calculation
                    cred_norm = credibility / 100.0

                    weight = cred_norm * sentiment * intensity * 100  # Scale up
                    consensus_weight += weight
                    valid_comments_count += 1
                    representative_comments.append(comment)

                # Limit representative comments to top 3 (simple logic for now)
                representative_comments = representative_comments[:3]

                prioritized.append(
                    PrioritizedFeature(
                        id=feature_obj.id,
                        title=feature_obj.title,
                        category=feature_obj.category,
                        linkedComments=valid_comments_count,
                        consensusWeight=int(consensus_weight),
                        description=analysis.description,
                        representativeComments=representative_comments,
                    )
                )

            # Sort by consensus weight descending
            prioritized.sort(key=lambda x: x.consensusWeight, reverse=True)
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
            f'- {f.title} (Weight: {f.consensusWeight}, Comments: {f.linkedComments})'
            for f in top_features
        )

        prompt = f"""
        Project Description: {project_description}
        
        Top Validated Features:
        {features_text}
        
        Based on the validation of these features by credible users, generate a Product-Market Fit (PMF) report.
        1. Assign a PMF Confidence Score (0-100). Be optimistic but realistic based on the weights.
        2. Provide 5-7 bullet points highlighting the positive aspects confirmed by the data.
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
            return PMFReport(score=0, summary=['Error generating report.'])
            # Wait, PMFReport in mock_data has score and summary. Does it have validation_text?
            # Let's check mock_data.py
