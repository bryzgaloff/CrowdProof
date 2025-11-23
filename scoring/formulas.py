import math
from typing import List

# Constants for Subreddit Relevance
W1 = 0.6  # Weight for Similarity
W2 = 0.2  # Weight for Active Users
W3 = 0.2  # Weight for Engagement Rate

# Constants for User Credibility
EPSILON = 1.0
LAMBDA = 0.5

# Constants for PMF Score
ALPHA = 0.1
BETA = 0.05
DELTA = 5.0


def calculate_subreddit_relevance(
    similarity: float, active_users: int, engagement_rate: float
) -> float:
    """
    Calculates Subreddit Relevance Index (Rs).
    Rs = w1 * Sim + w2 * log(Active) + w3 * Engagement
    """
    # Avoid log(0)
    log_active = math.log(active_users) if active_users > 1 else 0

    rs = (W1 * similarity) + (W2 * log_active) + (W3 * engagement_rate)
    return round(rs, 2)


def calculate_user_credibility(
    domain_karma: int, total_karma: int, account_age_years: float, badges_weight: float
) -> float:
    """
    Calculates User Credibility Score (Cu).
    Cu = (K_domain / (K_total + epsilon)) * (1 - e^(-lambda * T_age)) + Sum(Badges)
    """
    term1 = domain_karma / (total_karma + EPSILON)
    term2 = 1 - math.exp(-LAMBDA * account_age_years)

    cu = (term1 * term2) + badges_weight
    return min(max(cu, 0.0), 1.0)  # Clamp between 0 and 1


def calculate_consensus_weight(
    credibility: float, sentiment: float, intensity: float
) -> float:
    """
    Calculates contribution to Consensus Weight for a single comment.
    Weight = Cu * S * I
    """
    return credibility * sentiment * intensity


def calculate_pmf_score(top_features_consensus: List[float], total_volume: int) -> int:
    """
    Calculates PMF Confidence Score.
    PMF = 1 / (1 + e^-(alpha * Avg(W_top5) + beta * Vol - delta)) * 100
    """
    if not top_features_consensus:
        return 0

    avg_weight = sum(top_features_consensus) / len(top_features_consensus)

    exponent = -(ALPHA * avg_weight + BETA * total_volume - DELTA)

    try:
        sigmoid = 1 / (1 + math.exp(exponent))
    except OverflowError:
        sigmoid = 0 if exponent > 0 else 1

    return int(sigmoid * 100)
