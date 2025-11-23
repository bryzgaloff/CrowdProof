from typing import List

from pydantic import BaseModel


class Subreddit(BaseModel):
    name: str
    relevance: float
    description: str


class Tag(BaseModel):
    label: str
    color: str


class User(BaseModel):
    id: str
    credibility: int
    tags: List[Tag]


class Comment(BaseModel):
    id: str
    author: str
    text: str
    score: int
    isExpert: bool


class Feature(BaseModel):
    id: str
    title: str
    category: str


class PrioritizedFeature(BaseModel):
    id: str
    title: str
    category: str
    linkedComments: int
    consensusWeight: int
    description: str
    representativeComments: List[Comment]


class PMFReport(BaseModel):
    score: int
    summary: List[str]


# MOCK DATA from constants.ts

MOCK_SUBREDDITS = [
    Subreddit(
        name='EatCheapAndHealthy',
        relevance=9.9,
        description='Focus on affordable, nutritious cooking.',
    ),
    Subreddit(
        name='MealPrepSunday',
        relevance=9.8,
        description='Dedicated to batch cooking and planning.',
    ),
    Subreddit(
        name='ZeroWaste',
        relevance=9.7,
        description='Lifestyle discussions on reducing waste.',
    ),
    Subreddit(
        name='Cooking',
        relevance=9.6,
        description='General cooking discussions and help.',
    ),
    Subreddit(
        name='Frugal',
        relevance=9.5,
        description='Money-saving tips, including groceries.',
    ),
    Subreddit(
        name='KitchenConfidential',
        relevance=9.3,
        description='Professional kitchen culture & tips.',
    ),
    Subreddit(
        name='BudgetFood',
        relevance=9.2,
        description='Low cost recipes and shopping hacks.',
    ),
    Subreddit(
        name='FoodHacks',
        relevance=9.0,
        description='Shortcuts and efficiency in the kitchen.',
    ),
    Subreddit(
        name='HealthyFood',
        relevance=8.9,
        description='Discussions on diet and nutrition.',
    ),
    Subreddit(
        name='PersonalFinance',
        relevance=8.7,
        description='Budgeting and expense management.',
    ),
    Subreddit(
        name='Parenting',
        relevance=8.6,
        description='Family management and household logistics.',
    ),
    Subreddit(
        name='Adulting',
        relevance=8.4,
        description='Learning to manage household responsibilities.',
    ),
    Subreddit(
        name='TechSupport',
        relevance=8.2,
        description='General tech help and app suggestions.',
    ),
    Subreddit(
        name='FrugalLiving', relevance=8.1, description='Living well on less money.'
    ),
    Subreddit(
        name='AskCulinary',
        relevance=8.0,
        description='Expert answers to cooking questions.',
    ),
]

MOCK_USERS = [
    User(
        id='t2_j9k3x',
        credibility=98,
        tags=[
            Tag(label='Top Contributor', color='purple'),
            Tag(label='Chef', color='blue'),
        ],
    ),
    User(
        id='t2_m4p2z',
        credibility=97,
        tags=[Tag(label='Parent', color='green'), Tag(label='Verified', color='blue')],
    ),
    User(
        id='t2_x8r9q',
        credibility=95,
        tags=[
            Tag(label='Tech Enthusiast', color='pink'),
            Tag(label='Early Adopter', color='purple'),
        ],
    ),
    User(
        id='t2_b5v1w',
        credibility=94,
        tags=[
            Tag(label='Eco-Activist', color='green'),
            Tag(label='Vegan', color='green'),
        ],
    ),
    User(
        id='t2_a1b2c',
        credibility=93,
        tags=[
            Tag(label='Student', color='orange'),
            Tag(label='Frugal', color='orange'),
        ],
    ),
    User(
        id='t2_h7n3m',
        credibility=91,
        tags=[Tag(label='Homeowner', color='blue'), Tag(label='DIYer', color='orange')],
    ),
    User(
        id='t2_q5w8r',
        credibility=89,
        tags=[
            Tag(label='Developer', color='pink'),
            Tag(label='Android User', color='green'),
        ],
    ),
    User(
        id='t2_k2l9p',
        credibility=88,
        tags=[
            Tag(label='Fitness Coach', color='purple'),
            Tag(label='Health Nut', color='green'),
        ],
    ),
    User(
        id='t2_z4x7y',
        credibility=86,
        tags=[
            Tag(label='Blogger', color='pink'),
            Tag(label='Influencer', color='purple'),
        ],
    ),
    User(
        id='t2_r3d5f',
        credibility=85,
        tags=[
            Tag(label='Parent', color='blue'),
            Tag(label='Deal Hunter', color='orange'),
        ],
    ),
    User(
        id='t2_y6u8i',
        credibility=83,
        tags=[Tag(label='Casual User', color='blue'), Tag(label='Gamer', color='pink')],
    ),
    User(
        id='t2_v7n9m',
        credibility=80,
        tags=[
            Tag(label='Student', color='orange'),
            Tag(label='Newbie Cook', color='green'),
        ],
    ),
    User(
        id='t2_c1o4l',
        credibility=79,
        tags=[Tag(label='Traveler', color='blue'), Tag(label='Foodie', color='purple')],
    ),
    User(
        id='t2_e9p6s',
        credibility=77,
        tags=[Tag(label='Retiree', color='blue'), Tag(label='Gardener', color='green')],
    ),
    User(
        id='t2_g8j2k',
        credibility=74,
        tags=[
            Tag(label='Lurker', color='orange'),
            Tag(label='Gadget Lover', color='purple'),
        ],
    ),
]

MOCK_COMMENTS = [
    Comment(
        id='c1',
        author='t2_j9k3x',
        text="Honestly, the hardest part of cooking isn't the technique, it's the inventory management. I end up throwing away so much produce because I forget it's in the crisper.",
        score=1450,
        isExpert=True,
    ),
    Comment(
        id='c2',
        author='t2_m4p2z',
        text="I'd pay a sub just to have something scan my receipts and tell me when my milk goes bad. My kids waste so much and groceries are insane rn.",
        score=890,
        isExpert=False,
    ),
    Comment(
        id='c3',
        author='t2_a1b2c',
        text='u guys know any app that compares prices across walmart vs target automatically? inflation is killing me lol',
        score=670,
        isExpert=False,
    ),
    Comment(
        id='c4',
        author='t2_q5w8r',
        text="The APIs for grocery stores are terrible. If someone cracks the code on real-time inventory syncing via OCR or email receipts, it's a unicorn startup.",
        score=520,
        isExpert=True,
    ),
    Comment(
        id='c5',
        author='t2_v7n9m',
        text='jus wanna know what to make with 3 eggs and a sad lemon tbh. i hate googling recipes and getting life stories.',
        score=340,
        isExpert=False,
    ),
    Comment(
        id='c6',
        author='t2_x8r9q',
        text='I tried doing this manually in Notion but it takes too much time. Needs to be automated. Scan and forget.',
        score=280,
        isExpert=False,
    ),
    Comment(
        id='c7',
        author='t2_b5v1w',
        text='Reducing food waste is the single biggest thing we can do for climate change at home. An app that tracks carbon footprint savings from rescued food would be huge.',
        score=210,
        isExpert=False,
    ),
    Comment(
        id='c8',
        author='t2_h7n3m',
        text="My fridge is a black hole. I buy stuff I already have. If I could share the inventory with my wife so we stop double buying milk, that'd be great.",
        score=195,
        isExpert=False,
    ),
    Comment(
        id='c9',
        author='t2_k2l9p',
        text='As a nutritionist, I see people buy veggies with good intentions and then rot. Suggesting recipes based on *expiring* items is the killer feature.',
        score=175,
        isExpert=True,
    ),
    Comment(
        id='c10',
        author='t2_z4x7y',
        text="aesthetic pantry organization is viral on tiktok rn. if the app interface is cute, it'll blow up.",
        score=150,
        isExpert=False,
    ),
    Comment(
        id='c11',
        author='t2_r3d5f',
        text='Need a way to filter out allergens. My son has a peanut allergy and generic recipe apps are risky.',
        score=130,
        isExpert=False,
    ),
    Comment(
        id='c12',
        author='t2_c1o4l',
        text="I travel a lot and hate coming home to a smelly fridge. Need a 'vacation mode' suggestion to use up perishables before I leave.",
        score=115,
        isExpert=False,
    ),
    Comment(
        id='c13',
        author='t2_e9p6s',
        text="I'm old school. Keep it simple. Big fonts, easy buttons. Don't need social media features in my fridge app.",
        score=90,
        isExpert=False,
    ),
    Comment(
        id='c14',
        author='t2_g8j2k',
        text="Gamify it. Give me points for not wasting food. I'm a sucker for achievements.",
        score=85,
        isExpert=False,
    ),
    Comment(
        id='c15',
        author='t2_y6u8i',
        text='make it open source pls',
        score=40,
        isExpert=False,
    ),
]

MOCK_FEATURES = [
    Feature(id='f1', title='OCR Receipt Scanning', category='Core'),
    Feature(id='f2', title='Expiration Push Notifications', category='Notifications'),
    Feature(id='f3', title='Pantry-based Recipe Engine', category='AI'),
    Feature(id='f4', title='Cross-store Price Comparison', category='Shopping'),
    Feature(id='f5', title='Manual Inventory Adjustment', category='Core'),
    Feature(id='f6', title='Dietary Restriction Filter', category='Settings'),
    Feature(id='f7', title='Family Sharing Sync', category='Social'),
    Feature(id='f8', title='Barcode Scanner', category='Core'),
    Feature(id='f9', title='Email Receipt Integration', category='Integrations'),
    Feature(id='f10', title='Food Waste Dashboard', category='Analytics'),
    Feature(id='f11', title='Vacation Mode Meal Planning', category='AI'),
    Feature(
        id='f12', title='Sustainability Score / Carbon Saver', category='Gamification'
    ),
    Feature(id='f13', title='Offline Mode Support', category='Technical'),
    Feature(id='f14', title='Local Grocery Flyer Aggregation', category='Shopping'),
    Feature(id='f15', title='Pantry Staples Auto-Refill List', category='Shopping'),
    Feature(id='f16', title='Voice Assistant Integration', category='Integrations'),
    Feature(id='f17', title='Community Recipe Sharing', category='Social'),
    Feature(id='f18', title='Dark Mode', category='UI/UX'),
    Feature(id='f19', title='Export to Instacart/Doordash', category='Integrations'),
    Feature(id='f20', title='Customizable Expiry Rules', category='Settings'),
]


# Helper to find comment by ID
def get_comment(cid):
    return next((c for c in MOCK_COMMENTS if c.id == cid), None)


MOCK_PRIORITIZED_FEATURES = [
    PrioritizedFeature(
        id='f3',
        title='Pantry-based Recipe Engine',
        category='AI',
        linkedComments=124,
        consensusWeight=96,
        description="An intelligent recommendation engine that prioritizes recipes based on ingredients currently in your inventory that are approaching their expiration date. This reverses the traditional 'what do I want to eat' model to a 'what do I need to use' model.",
        representativeComments=[
            get_comment('c5'),
            get_comment('c9'),
            get_comment('c1'),
        ],
    ),
    PrioritizedFeature(
        id='f1',
        title='OCR Receipt Scanning',
        category='Core',
        linkedComments=98,
        consensusWeight=94,
        description='Computer vision integration allowing users to photograph grocery receipts for automatic inventory population. The system parses items, quantities, and dates, mapping them to a standard ingredient database.',
        representativeComments=[
            get_comment('c2'),
            get_comment('c4'),
            get_comment('c6'),
        ],
    ),
    PrioritizedFeature(
        id='f4',
        title='Cross-store Price Comparison',
        category='Shopping',
        linkedComments=85,
        consensusWeight=91,
        description='Real-time aggregation of local grocery prices to suggest the optimal store for your generated shopping list. Identifies potential savings by splitting the list across multiple nearby vendors.',
        representativeComments=[get_comment('c3'), get_comment('c2')],
    ),
    PrioritizedFeature(
        id='f2',
        title='Expiration Notifications',
        category='Notifications',
        linkedComments=76,
        consensusWeight=88,
        description="Smart push notifications that alert users at optimal intervals (3 days, 24 hours) before specific items expire. Includes quick-action buttons to 'Find Recipe' or 'Add to Shopping List'.",
        representativeComments=[get_comment('c2'), get_comment('c9')],
    ),
    PrioritizedFeature(
        id='f8',
        title='Barcode Scanner',
        category='Core',
        linkedComments=65,
        consensusWeight=85,
        description='Quick-entry method for packaged goods. Scans UPC codes to instantly retrieve product metadata, including nutritional info and shelf-life estimates from a central database.',
        representativeComments=[get_comment('c6'), get_comment('c13')],
    ),
    PrioritizedFeature(
        id='f10',
        title='Food Waste Dashboard',
        category='Analytics',
        linkedComments=42,
        consensusWeight=78,
        description="Visual analytics tracking money saved and food waste prevented over time. Provides weekly reports and 'waste velocity' metrics to help users adjust buying habits.",
        representativeComments=[get_comment('c7'), get_comment('c14')],
    ),
    PrioritizedFeature(
        id='f7',
        title='Family Sharing Sync',
        category='Social',
        linkedComments=38,
        consensusWeight=72,
        description='Multi-user synchronization for a single household inventory. Allows one person to shop while another cooks, with updates reflected instantly on all devices to prevent double-buying.',
        representativeComments=[get_comment('c8')],
    ),
    PrioritizedFeature(
        id='f6',
        title='Dietary Restriction Filter',
        category='Settings',
        linkedComments=30,
        consensusWeight=68,
        description='Global safety filters that remove unsafe recipes from suggestions. Supports common allergens (nuts, dairy) and lifestyle choices (vegan, keto) applied to the entire recipe engine.',
        representativeComments=[get_comment('c11')],
    ),
    PrioritizedFeature(
        id='f12',
        title='Sustainability Score',
        category='Gamification',
        linkedComments=25,
        consensusWeight=60,
        description="Gamified metric converting saved food into carbon footprint equivalents. Users earn badges for 'Rescue Streaks' and hitting sustainability milestones.",
        representativeComments=[get_comment('c7'), get_comment('c14')],
    ),
    PrioritizedFeature(
        id='f11',
        title='Vacation Mode Meal Planning',
        category='AI',
        linkedComments=15,
        consensusWeight=55,
        description='Specialized planning algorithm designed to clear the fridge before a set departure date. Prioritizes highly perishable items in recipe suggestions leading up to a trip.',
        representativeComments=[get_comment('c12')],
    ),
    PrioritizedFeature(
        id='f9',
        title='Email Receipt Integration',
        category='Integrations',
        linkedComments=12,
        consensusWeight=52,
        description='Automated parsing of digital receipts forwarded from email. Connects with major grocery delivery services (Instacart, Amazon Fresh) to auto-populate inventory.',
        representativeComments=[get_comment('c4')],
    ),
    PrioritizedFeature(
        id='f14',
        title='Local Grocery Flyer Aggregation',
        category='Shopping',
        linkedComments=10,
        consensusWeight=48,
        description='Digitized versions of weekly local store flyers integrated into the shopping list builder, allowing users to clip coupons and spot deals directly within the app.',
        representativeComments=[get_comment('c3')],
    ),
    PrioritizedFeature(
        id='f15',
        title='Pantry Staples Auto-Refill',
        category='Shopping',
        linkedComments=8,
        consensusWeight=45,
        description='Predictive algorithm that learns consumption rates of staples (rice, oil, flour) and automatically suggests adding them to the shopping list before they run out.',
        representativeComments=[get_comment('c6')],
    ),
    PrioritizedFeature(
        id='f20',
        title='Customizable Expiry Rules',
        category='Settings',
        linkedComments=6,
        consensusWeight=40,
        description='Advanced settings allowing users to override default shelf-life estimates. Useful for produce stored in special conditions or users with different risk tolerances.',
        representativeComments=[get_comment('c9')],
    ),
    PrioritizedFeature(
        id='f16',
        title='Voice Assistant Integration',
        category='Integrations',
        linkedComments=5,
        consensusWeight=35,
        description='Hands-free operation via Alexa/Google Home. Allows users to add items to the pantry or shopping list via voice commands while their hands are dirty cooking.',
        representativeComments=[get_comment('c1')],
    ),
    PrioritizedFeature(
        id='f19',
        title='Export to Instacart',
        category='Integrations',
        linkedComments=4,
        consensusWeight=30,
        description='One-click checkout capability that transfers the generated shopping list directly to a third-party delivery service cart.',
        representativeComments=[get_comment('c4')],
    ),
    PrioritizedFeature(
        id='f17',
        title='Community Recipe Sharing',
        category='Social',
        linkedComments=3,
        consensusWeight=25,
        description="Social platform within the app for users to share 'rescue recipes'—creative ways they used up odd combinations of leftover ingredients.",
        representativeComments=[get_comment('c10')],
    ),
    PrioritizedFeature(
        id='f13',
        title='Offline Mode Support',
        category='Technical',
        linkedComments=2,
        consensusWeight=20,
        description='Local-first architecture ensuring the inventory and shopping list remain accessible and editable in grocery stores with poor cellular reception.',
        representativeComments=[get_comment('c1')],
    ),
    PrioritizedFeature(
        id='f18',
        title='Dark Mode',
        category='UI/UX',
        linkedComments=1,
        consensusWeight=15,
        description='Alternative color scheme optimized for low-light environments, reducing eye strain during late-night meal planning or snacking.',
        representativeComments=[get_comment('c10')],
    ),
    PrioritizedFeature(  # Note: f5 was in features but not in prioritized list in constants.ts snippet I saw?
        # Wait, f5 is in MOCK_FEATURES. Is it in MOCK_PRIORITIZED_FEATURES?
        # No, I missed f5 in the prioritized list in the `cat` output.
        # Ah, I see f5 at the very end of the `cat` output in step 65.
        id='f5',
        title='Manual Inventory Adjustment',
        category='Core',
        linkedComments=1,
        consensusWeight=10,
        description='Simple CRUD interface for manual entry and correction of inventory items, ensuring the digital twin matches physical reality when automation fails.',
        representativeComments=[get_comment('c6')],
    ),
]

MOCK_PMF_REPORT = PMFReport(
    score=94,
    summary=[
        'Strong alignment with high-frequency pain points (food waste & inflation).',
        'Technical feasibility confirmed by expert commentary regarding OCR viability.',
        'Target demographic (Parents, Budget-conscious) shows high willingness to pay.',
        "Clear gap in current market for 'Inventory-First' rather than 'Recipe-First' solutions.",
        'Viral potential in budget/frugal communities is extremely high.',
    ],
)
