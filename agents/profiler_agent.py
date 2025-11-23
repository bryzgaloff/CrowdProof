import os
from typing import List

from openai import OpenAI
from pydantic import BaseModel

from mock_data import Comment, Tag, User


class TagsResponse(BaseModel):
    tags: List[str]


class ProfilerAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def enrich_user(self, user: User, comments: List[Comment]) -> User:
        """
        Enriches the user with behavioral tags based on their comments.
        If user already has tags (mock data), returns as is.
        """
        if user.tags:
            return user

        user_comments = [c.text for c in comments if c.author == user.id]

        if not user_comments:
            user.tags = [Tag(label='New User', color='gray')]
            return user

        comments_text = '\n'.join(f'- {c}' for c in user_comments)

        prompt = f"""
        Analyze the following comments made by a Reddit user and infer their behavioral profile.
        Assign 2-4 short, descriptive tags that characterize them (e.g., "Tech Savvy", "Price Sensitive", "Early Adopter", "Skeptic", "Industry Expert", "Casual User").
        
        Comments:
        {comments_text}
        """

        try:
            completion = self.client.beta.chat.completions.parse(
                model='gpt-4o-2024-08-06',
                messages=[
                    {'role': 'system', 'content': 'You are an expert user profiler.'},
                    {'role': 'user', 'content': prompt},
                ],
                response_format=TagsResponse,
            )

            tags_str = completion.choices[0].message.parsed.tags
            # Limit to 4 tags and ensure they are short
            # Assign random colors for generated tags
            user.tags = [Tag(label=t, color='blue') for t in tags_str[:4]]

        except Exception as e:
            print(f'Error profiling user {user.id}: {e}')
            user.tags = [Tag(label='Unprofiled', color='gray')]

        return user
