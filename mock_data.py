from pydantic import BaseModel
from typing import List, Optional

class Subreddit(BaseModel):
    name: str
    url: str
    relevance_score: float  # 0.0 to 10.0
    color: str # "green" or "orange"

class User(BaseModel):
    username: str
    credibility_score: float
    tags: List[str] = [] # To be filled by Profiler

class Comment(BaseModel):
    id: str
    text: str
    author: str
    score: int
    subreddit: str

# Mock Data for a "Smart Travel Planner" project

MOCK_SUBREDDITS = [
    Subreddit(name="r/travel", url="https://reddit.com/r/travel", relevance_score=9.8, color="green"),
    Subreddit(name="r/digitalnomad", url="https://reddit.com/r/digitalnomad", relevance_score=9.5, color="green"),
    Subreddit(name="r/solotravel", url="https://reddit.com/r/solotravel", relevance_score=9.2, color="green"),
    Subreddit(name="r/TravelHacks", url="https://reddit.com/r/TravelHacks", relevance_score=8.2, color="orange"),
]

MOCK_USERS = [
    User(username="t2_wanderlust_king", credibility_score=0.95),
    User(username="t2_nomad_life", credibility_score=0.88),
    User(username="t2_budget_backpacker", credibility_score=0.75),
    User(username="t2_luxury_traveler", credibility_score=0.92),
    User(username="t2_tech_tourist", credibility_score=0.85),
]

MOCK_COMMENTS = [
    Comment(id="c1", text="I honestly hate planning itineraries. I spend hours on TripAdvisor and still feel like I'm missing out. An AI that actually understands my vibe would be a game changer.", author="t2_wanderlust_king", score=150, subreddit="r/travel"),
    Comment(id="c2", text="Most 'AI' planners just give you generic tourist traps. If this tool can find hidden gems based on my past trips, I'd pay for it.", author="t2_nomad_life", score=89, subreddit="r/digitalnomad"),
    Comment(id="c3", text="I don't trust AI with my flights. Too many variables. But for restaurant recommendations? Sure.", author="t2_budget_backpacker", score=45, subreddit="r/solotravel"),
    Comment(id="c4", text="Integration with booking platforms is a must. I don't want to copy-paste everything.", author="t2_luxury_traveler", score=120, subreddit="r/TravelHacks"),
    Comment(id="c5", text="It needs to handle group trips. Coordinating 5 people is a nightmare.", author="t2_tech_tourist", score=200, subreddit="r/travel"),
    Comment(id="c6", text="Make it offline accessible. Data roaming is expensive.", author="t2_budget_backpacker", score=60, subreddit="r/solotravel"),
    Comment(id="c7", text="I've tried 5 different apps and I always go back to spreadsheets. They are just too rigid.", author="t2_nomad_life", score=110, subreddit="r/digitalnomad"),
]
