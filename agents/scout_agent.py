from typing import List

from mock_data import (
    MOCK_COMMENTS,
    MOCK_SUBREDDITS,
    MOCK_USERS,
    Comment,
    Subreddit,
    User,
)


class ScoutAgent:
    def __init__(self):
        pass

    def select_subreddits(self, project_description: str) -> List[Subreddit]:
        """
        Simulates selecting relevant subreddits based on the project description.
        In a real scenario, this would search Reddit and use LLM to filter.
        """
        # Simulate processing time
        # time.sleep(1)
        return MOCK_SUBREDDITS

    def select_credible_users(self) -> List[User]:
        """
        Simulates selecting credible users.
        """
        # time.sleep(1)
        return MOCK_USERS

    def mine_opinions(self) -> List[Comment]:
        """
        Simulates mining opinions (comments).
        """
        # time.sleep(1)
        return MOCK_COMMENTS
