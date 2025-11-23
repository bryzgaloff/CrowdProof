import os
import time

from dotenv import load_dotenv

from agents.product_analyst_agent import ProductAnalystAgent
from agents.profiler_agent import ProfilerAgent
from agents.scout_agent import ScoutAgent

# Config
STEP_DELAY = 5  # Seconds


def print_step(step_name):
    print(f'\n--- {step_name} ---')
    print('Processing...', end='', flush=True)
    for _ in range(STEP_DELAY):
        time.sleep(1)
        print('.', end='', flush=True)
    print(' Done!\n')


def main():
    load_dotenv()

    if not os.getenv('OPENAI_API_KEY'):
        print(
            'WARNING: OPENAI_API_KEY not found in environment variables. OpenAI calls will fail.'
        )
        # You might want to input it here or exit
        # return

    print('Welcome to CrowdProof AI Demo')
    print('-----------------------------')

    default_description = 'An AI-powered travel itinerary planner that learns from your past trips and finds hidden gems, integrating with booking platforms.'
    print(
        f"Enter project description (Press Enter for default: '{default_description[:50]}...'):"
    )
    project_description = input('> ').strip()
    if not project_description:
        project_description = default_description

    print(f'\nStarting analysis for: {project_description}\n')

    # Initialize Agents
    scout = ScoutAgent()
    profiler = ProfilerAgent()
    analyst = ProductAnalystAgent()

    # Step 1: Scout Agent - Selecting Subreddits
    print_step('Scout Agent: Selecting relevant subreddits')
    subreddits = scout.select_subreddits(project_description)
    print('Found Subreddits:')
    for sub in subreddits:
        print(f'[{sub.relevance}] {sub.name} - {sub.description}')

    # Step 2: Scout Agent - Selecting Credible Users (and Profiling)
    print_step('Scout Agent: Selecting credible users')
    users = scout.select_credible_users()
    comments = scout.mine_opinions()  # Need comments for profiling

    print('Enriching User Profiles...')
    enriched_users = []
    for user in users:
        enriched_user = profiler.enrich_user(user, comments)
        enriched_users.append(enriched_user)

    print('Selected Users:')
    for user in enriched_users:
        tags_str = ', '.join([t.label for t in user.tags])
        print(f'User: {user.id} (Credibility: {user.credibility}) | Tags: [{tags_str}]')

    # Step 3: Scout Agent - Mining Opinions
    print_step('Scout Agent: Mining opinions')
    # We already fetched comments for profiling, but conceptually this is the step
    # Sort comments by score
    sorted_comments = sorted(comments, key=lambda x: x.score, reverse=True)
    print('Top Opinions:')
    for c in sorted_comments[:3]:  # Show top 3
        print(f'Score: {c.score} | {c.author}: {c.text[:100]}...')

    # Step 4: Product Analyst Agent - Mining Features
    print_step('Product Analyst Agent: Mining features')
    features = analyst.mine_features(comments, project_description)
    print('Extracted Features:')
    for f in features:
        print(f'- {f.title} ({f.category})')

    # Step 5: Product Analyst Agent - Prioritizing Features
    print_step('Product Analyst Agent: Prioritizing features')
    prioritized_features = analyst.prioritize_features(
        features, comments, enriched_users
    )
    print('Priority Backlog:')
    for pf in prioritized_features:
        print(f'Feature: {pf.title}')
        print(f'  Consensus Weight: {pf.consensusWeight}')
        print(f'  Related Comments: {pf.linkedComments}')

    # Step 6: Product Analyst Agent - Validating the Idea
    print_step('Product Analyst Agent: Validating the idea')
    pmf_report = analyst.validate_idea(prioritized_features, project_description)

    print('PMF REPORT')
    print('==========')
    print(f'PMF Confidence Score: {pmf_report.score}/100')
    # print(f"Summary: {pmf_report.validation_text}") # Removed from model
    print('Key Validation Points:')
    for point in pmf_report.summary:
        print(f'* {point}')

    print('\nDone. You can now continue the discussion.')


if __name__ == '__main__':
    main()
