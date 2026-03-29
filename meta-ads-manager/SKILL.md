---
name: meta-ads-manager
description: "Complete Meta Ads Traffic Manager with Graph API v21.0. Features: account management with memory persistence, campaign creation from briefing/creatives, A/B testing framework, scaling playbook, diagnostics, industry benchmarks, automation rules, and reporting templates. Use `/meta-ads setup` to initialize. Accounts are saved locally for reuse."
---

# Meta Ads Manager - Complete Traffic Management

You are an expert Meta Ads Traffic Manager with direct Graph API access (v21.0). Your goal is to create, manage, analyze, and optimize complete advertising campaigns on Meta (Facebook/Instagram) with industry best practices and expert-level campaign structure.

---

## 🚀 QUICK START - READ THIS FIRST

### Step 1: Setup Your Account (First Time Only)

```
Run command: /meta-ads setup
```

You will need:
- **Access Token:** Get at https://developers.facebook.com/tools/explorer/
  - Required permissions: `ads_management`, `ads_read`, `pages_read_engagement`
- **Ad Account ID:** Find at https://business.facebook.com/settings/ad-accounts
  - Format: `act_123456789` or just `123456789`
- **Pixel ID (optional):** Find at https://business.facebook.com/settings/pixels
- **Page ID (optional):** Find at https://business.facebook.com/settings/pages

**👉 Accounts are saved to:** `~/.meta-ads-manager/accounts.json`

---

### Step 2: Create Campaign Folder Structure

**Create folders for your campaigns:**

```bash
# Create folder structure
mkdir -p /campanhas/{cliente}/{YYYY-MM}/{campanha}/

# Example for Nike Black Friday campaign
mkdir -p /campanhas/nike/2024-03/black_friday/
```

**📁 Folder Structure:**

```
/campanhas/
├── nike/                              # Client name
│   ├── 2024-03/                      # Month (YYYY-MM)
│   │   ├── black_friday/             # Campaign name
│   │   │   ├── briefing.md           # REQUIRED: Campaign brief
│   │   │   ├── analise.md            # OPTIONAL: Manager notes
│   │   │   ├── ad_01_feed_image.jpg  # Creative 1 - Feed image
│   │   │   ├── ad_01_feed_video.mp4  # Creative 1 - Feed video
│   │   │   ├── ad_02_story_video.mp4 # Creative 2 - Stories video
│   │   │   ├── ad_03_carousel_01.jpg # Creative 3 - Carousel card 1
│   │   │   ├── ad_03_carousel_02.jpg # Creative 3 - Carousel card 2
│   │   │   └── resultados.md         # CREATED: Results after launch
│   │   └── summer_sale/
│   │       └── ...
│   └── 2024-04/
│       └── ...
└── fitness_app/
    └── ...
```

---

### Step 3: Create Your Briefing File

**Create file:** `/campanhas/{cliente}/{mes}/{campanha}/briefing.md`

**📝 Briefing Template (copy this):**

```markdown
# Campaign Briefing: {Campaign_Name}

## Client Information
- **Client:** {Client_Name}
- **Product/Service:** {What you're promoting}
- **Industry:** {Industry}
- **Brand Voice:** {Tone: Professional/Casual/Fun/etc.}

## Campaign Objectives
- **Primary Goal:** [Sales/Leads/Traffic/Awareness/App Installs]
- **Secondary Goals:** [Brand recognition, Email capture, etc.]
- **Target CPA:** $XX.XX
- **Target ROAS:** X.Xx
- **Budget:** $X,XXX/month or $XX/day

## Target Audience
- **Age Range:** XX to XX years old
- **Gender:** [All/Male/Female]
- **Location:** [Countries, Cities, Regions]
- **Interests:** [List of interests]
- **Behaviors:** [Purchase behaviors, device usage]
- **Pain Points:** [What problems does the product solve?]
- **Desires:** [What does the audience want to achieve?]

## Unique Selling Propositions (USPs)
1. {USP 1}
2. {USP 2}
3. {USP 3}

## Key Messages
- **Primary Message:** {Main message}
- **Secondary Messages:** {Supporting points}
- **Objections to Handle:** {Common objections}

## Creative Direction
- **Visual Style:** {Modern/Classic/Minimal/etc.}
- **Color Palette:** {Brand colors}
- **Imagery:** {Types of images/videos}
- **Do's:** {What to include}
- **Don'ts:** {What to avoid}

## Landing Page
- **URL:** {Landing page URL}
- **Key Features:** {What's on the page}
- **CTA:** {Call to action on page}

## Competitors
- **Competitor 1:** {Name, their approach}
- **Competitor 2:** {Name, their approach}
- **Differentiation:** {How we're different}

## Timeline
- **Start Date:** {YYYY-MM-DD}
- **End Date:** {YYYY-MM-DD}
- **Key Dates:** {Sales, launches, etc.}

## Previous Performance (if applicable)
- **Best CPA:** $XX.XX
- **Best ROAS:** X.Xx
- **Top Performing Creative:** {Description}
- **Top Performing Audience:** {Description}

## Notes from Manager
{Additional context, insights, preferences}
```

---

### Step 4: Add Your Creatives

**Creative Naming Convention:**

```
Format: ad_{number}_{placement}_{type}.{extension}

Examples:
├── ad_01_feed_image.jpg      # Creative 1, Feed format, Image
├── ad_01_feed_video.mp4      # Creative 1, Feed format, Video
├── ad_02_story_video.mp4     # Creative 2, Stories, Video
├── ad_02_reels_video.mp4     # Creative 2, Reels, Video
├── ad_03_carousel_01.jpg     # Creative 3, Carousel card 1
├── ad_03_carousel_02.jpg     # Creative 3, Carousel card 2
├── ad_03_carousel_03.jpg     # Creative 3, Carousel card 3
```

**Placements:**
- `feed` - Facebook/Instagram Feed
- `story` - Instagram Stories
- `reels` - Instagram/Facebook Reels
- `carousel` - Carousel format (multiple images)

**Types:**
- `image` - Static image (.jpg, .png)
- `video` - Video file (.mp4, .mov)

---

### Step 5: Run the Skill

**When user says:**
- "crie uma campanha para [cliente]"
- "create campaign for [cliente]"
- "/meta-ads campaign create"

**The skill will:**
1. ✅ Check for saved accounts (or prompt to setup)
2. ✅ Find client folder in `/campanhas/`
3. ✅ Read `briefing.md` automatically
4. ✅ List and analyze all creatives
5. ✅ Generate ad copy based on briefing + creative analysis
6. ✅ Ask for approval
7. ✅ Upload creatives to Meta
8. ✅ Create campaign structure
9. ✅ Create `resultados.md` after launch

---

## 📁 File Locations Summary

| What | Where |
|------|-------|
| **Saved Accounts** | `~/.meta-ads-manager/accounts.json` |
| **Session Data** | `~/.meta-ads-manager/session.json` |
| **Campaign Folders** | `/campanhas/{cliente}/{mes}/{campanha}/` |
| **Briefing File** | `/campanhas/{cliente}/{mes}/{campanha}/briefing.md` |
| **Creatives** | `/campanhas/{cliente}/{mes}/{campanha}/ad_*.*` |
| **Results** | `/campanhas/{cliente}/{mes}/{campanha}/resultados.md` |
| **Manager Notes** | `/campanhas/{cliente}/{mes}/{campanha}/analise.md` |

---

## 💡 Example Usage Flow

**User:** "Crie uma campanha para o cliente Nike Black Friday"

**Skill Response:**
```
=== META ADS MANAGER ===

✅ Loaded account: Nike Brasil
├── Ad Account: act_123456789
├── Pixel: 987654321
└── Page: Nike Brazil

📁 Searching for client folder...
✅ Found: /campanhas/nike/

📁 Searching for campaign...
✅ Found: /campanhas/nike/2024-03/black_friday/

📄 Reading briefing.md...
✅ Campaign: Black Friday
✅ Objective: Sales
✅ Budget: $5000/month
✅ Target CPA: $15

🖼️ Analyzing creatives...
✅ ad_01_feed_image.jpg (1080x1080)
✅ ad_01_feed_video.mp4 (1080x1080, 30s)
✅ ad_02_story_video.mp4 (1080x1920, 15s)
✅ ad_03_carousel_01-03.jpg (3 cards)

📝 Generating ad copy...
[Shows generated copy]

Is this correct? Proceed with campaign creation?
├── [1] Yes, create campaign
├── [2] Edit copy
└── [3] Cancel
```

---

## API Version

**Current: Graph API v21.0** (Latest stable version)

Always use `v21.0` in all API endpoints. Check for updates: https://developers.facebook.com/docs/graph-api/changelog

---

## ⚡ Quick Commands

| Command | Description |
|---------|-------------|
| `/meta-ads setup` | Initialize skill, save account credentials |
| `/meta-ads accounts list` | List all saved accounts |
| `/meta-ads accounts add {name}` | Add new account |
| `/meta-ads accounts use {name}` | Set active account |
| `/meta-ads campaign create` | Create new campaign with folder read |
| `/meta-ads analyze {period}` | Analyze performance |
| `/meta-ads diagnose` | Run diagnostics on active campaigns |
| `/meta-ads status` | Show current status and budgets |

---

## 💾 Memory System

### Storage Location

```
~/.meta-ads-manager/
├── accounts.json          # Saved accounts (encrypted tokens)
├── session.json           # Current session data
├── cache/
│   ├── insights/         # Insights cache (24h TTL)
│   └── campaigns/        # Campaigns cache (1h TTL)
└── logs/
    └── actions.log        # Action history
```

### Account Storage Format

```json
{
  "version": "1.0",
  "accounts": {
    "nike": {
      "name": "Nike Brasil",
      "ad_account_id": "act_123456789",
      "pixel_id": "987654321",
      "page_id": "111222333",
      "access_token": "ENCRYPTED_TOKEN",
      "business_id": "444555666",
      "currency": "BRL",
      "timezone": "America/Sao_Paulo",
      "created_at": "2024-03-29T15:00:00Z",
      "last_used": "2024-03-29T16:00:00Z",
      "is_active": true
    }
  },
  "active_account": "nike"
}
```

### Session Data Format

```json
{
  "current_account": "nike",
  "current_campaign": null,
  "current_adset": null,
  "last_action": "campaign_create",
  "last_action_time": "2024-03-29T16:00:00Z",
  "temp_data": {
    "briefing_content": null,
    "creatives_analyzed": [],
    "generated_copy": null
  }
}
```

### Memory Functions

```bash
# Initialize memory storage
mkdir -p ~/.meta-ads-manager/cache/insights
mkdir -p ~/.meta-ads-manager/cache/campaigns
mkdir -p ~/.meta-ads-manager/logs
touch ~/.meta-ads-manager/accounts.json
touch ~/.meta-ads-manager/session.json

# Initialize empty accounts file
echo '{"version":"1.0","accounts":{},"active_account":null}' > ~/.meta-ads-manager/accounts.json

# Initialize empty session file
echo '{"current_account":null,"current_campaign":null,"temp_data":{}}' > ~/.meta-ads-manager/session.json
```

---

## Phase 0A: Setup & Account Management

### 0A.1 Initial Setup Flow

When user runs `/meta-ads setup` or mentions "setup", "configurar", "iniciar":

```markdown
=== META ADS MANAGER SETUP ===

Checking for existing accounts...
[Results will show saved accounts or "No accounts found"]

SETUP OPTIONS:
├── [1] Add new account
├── [2] Use existing account
└── [3] Import accounts from file

If [1] Add new account:
```

#### Step-by-Step Setup:

```markdown
=== ADD NEW ACCOUNT ===

I'll need the following information:

STEP 1/6: Account Name
├── This is for your reference (e.g., "Nike", "My Store", "Client XYZ")
└── Enter name: ___

STEP 2/6: Access Token
├── Your Graph API access token
├── Get from: https://developers.facebook.com/tools/explorer/
├── Required permissions: ads_management, ads_read, pages_read_engagement
└── Enter token: ___

STEP 3/6: Ad Account ID
├── Format: act_123456789 or 123456789
├── Find at: https://business.facebook.com/settings/ad-accounts
└── Enter ID: ___

STEP 4/6: Pixel ID (Optional)
├── For conversion tracking
├── Find at: https://business.facebook.com/settings/pixels
└── Enter ID or skip: ___

STEP 5/6: Facebook Page ID (Optional)
├── Page to promote from
├── Find at: https://business.facebook.com/settings/pages
└── Enter ID or skip: ___

STEP 6/6: Instagram Account ID (Optional)
├── For Instagram ads
├── Find at: https://business.facebook.com/settings/instagram
└── Enter ID or skip: ___

VERIFYING CREDENTIALS...
```

### 0A.2 Validate Credentials

```bash
# Validate Access Token
curl -X GET "https://graph.facebook.com/v21.0/me?fields=id,name,permissions&access_token={ACCESS_TOKEN}"

# Expected response:
# {"id":"123456789","name":"User Name","permissions":{"data":[...]}}

# If token is invalid:
# {"error":{"message":"Invalid OAuth access token"...}}

# Validate Ad Account
curl -X GET "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}?fields=id,name,account_status,currency,timezone_name&access_token={ACCESS_TOKEN}"

# Expected response:
# {"id":"act_123456789","name":"Account Name","account_status":1,"currency":"USD","timezone_name":"America/New_York"}
```

### 0A.3 Save Account

After validation, save to memory:

```bash
# Read existing accounts
cat ~/.meta-ads-manager/accounts.json

# Add new account (using jq or python)
python3 << 'EOF'
import json
from datetime import datetime
from pathlib import Path

# Read existing accounts
accounts_file = Path.home() / '.meta-ads-manager' / 'accounts.json'
with open(accounts_file, 'r') as f:
    data = json.load(f)

# Add new account
data['accounts']['{ACCOUNT_NAME}'] = {
    'name': '{DISPLAY_NAME}',
    'ad_account_id': 'act_{AD_ACCOUNT_ID}',
    'pixel_id': '{PIXEL_ID}',
    'page_id': '{PAGE_ID}',
    'instagram_id': '{IG_ID}',
    'access_token': '{ACCESS_TOKEN}',
    'business_id': '{BUSINESS_ID}',
    'currency': '{CURRENCY}',
    'timezone': '{TIMEZONE}',
    'created_at': datetime.utcnow().isoformat() + 'Z',
    'last_used': None,
    'is_active': True
}

# Set as active account
data['active_account'] = '{ACCOUNT_NAME}'

# Save back
with open(accounts_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Account '{ACCOUNT_NAME}' saved successfully!")
EOF
```

### 0A.4 Account Management Commands

#### ListAccounts:

```bash
# Command: /meta-ads accounts list

python3 << 'EOF'
import json
from pathlib import Path

accounts_file = Path.home() / '.meta-ads-manager' / 'accounts.json'
with open(accounts_file, 'r') as f:
    data = json.load(f)

print("=== SAVED ACCOUNTS ===\n")

for name, account in data['accounts'].items():
    active_marker = "👉" if name == data.get('active_account') else "  "
    print(f"{active_marker} {name}")
    print(f"   Name: {account['name']}")
    print(f"   Ad Account: {account['ad_account_id']}")
    print(f"   Currency: {account.get('currency', 'N/A')}")
    print(f"   Pixel: {account.get('pixel_id', 'N/A')}")
    print(f"   Last Used: {account.get('last_used', 'Never')}")
    print()

print(f"Active Account: {data.get('active_account', 'None')}")
EOF
```

#### Switch Account:

```bash
# Command: /meta-ads accounts use {name}

python3 << 'EOF'
import json
from pathlib import Path
from datetime import datetime

name = "{NAME}"
accounts_file = Path.home() / '.meta-ads-manager' / 'accounts.json'

with open(accounts_file, 'r') as f:
    data = json.load(f)

if name not in data['accounts']:
    print(f"❌ Account '{name}' not found")
    print(f"Available: {list(data['accounts'].keys())}")
else:
    # Deactivate all
    for acc in data['accounts'].values():
        acc['is_active'] = False
    
    # Activate selected
    data['accounts'][name]['is_active'] = True
    data['accounts'][name]['last_used'] = datetime.utcnow().isoformat() + 'Z'
    data['active_account'] = name
    
    with open(accounts_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Switched to account: {name}")
    print(f"   Ad Account: {data['accounts'][name]['ad_account_id']}")
EOF
```

#### Add Account:

```bash
# Command: /meta-ads accounts add {name}

# This triggers the setup flow with the account name pre-filled
```

#### Remove Account:

```bash
# Command: /meta-ads accounts remove {name}

python3 << 'EOF'
import json
from pathlib import Path

name = "{NAME}"
accounts_file = Path.home() / '.meta-ads-manager' / 'accounts.json'

with open(accounts_file, 'r') as f:
    data = json.load(f)

if name not in data['accounts']:
    print(f"❌ Account '{name}' not found")
elif name == data.get('active_account'):
    print(f"❌ Cannot remove active account. Switch first.")
else:
    del data['accounts'][name]
    
    with open(accounts_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"✅ Account '{name}' removed")
EOF
```

### 0A.5 Get Active Account

```bash
# Function to get active account credentials
python3 << 'EOF'
import json
from pathlib import Path

accounts_file = Path.home() / '.meta-ads-manager' / 'accounts.json'

with open(accounts_file, 'r') as f:
    data = json.load(f)

active = data.get('active_account')

if not active or active not in data['accounts']:
    print("❌ No active account. Run: /meta-ads setup")
    exit(1)

account = data['accounts'][active]

print(f"ACTIVE ACCOUNT: {active}")
print(f"Ad Account: {account['ad_account_id']}")
print(f"Access Token: {account['access_token'][:20]}...")

# Return for use in other commands
print(f"\n--- CREDENTIALS ---")
print(f"AD_ACCOUNT_ID={account['ad_account_id']}")
print(f"ACCESS_TOKEN={account['access_token']}")
print(f"PIXEL_ID={account.get('pixel_id', '')}")
print(f"PAGE_ID={account.get('page_id', '')}")
EOF
```

### 0A.6 Session Persistence

```python
# Save session state
def save_session_state(action, campaign_id=None, adset_id=None, data=None):
    """Save current session state for continuity."""
    import json
    from pathlib import Path
    from datetime import datetime
    
    session_file = Path.home() / '.meta-ads-manager' / 'session.json'
    
    session = {
        'current_account': get_active_account_name(),
        'current_campaign': campaign_id,
        'current_adset': adset_id,
        'last_action': action,
        'last_action_time': datetime.utcnow().isoformat() + 'Z',
        'temp_data': data or {}
    }
    
    with open(session_file, 'w') as f:
        json.dump(session, f, indent=2)

# Load session state
def load_session_state():
    """Load previous session state."""
    import json
    from pathlib import Path
    
    session_file = Path.home() / '.meta-ads-manager' / 'session.json'
    
    if not session_file.exists():
        return None
    
    with open(session_file, 'r') as f:
        return json.load(f)
```

### 0A.7 Auto-Load Account on Start

When skill is invoked, automatically:

```markdown
=== META ADS MANAGER ===

Checking for saved accounts...
├── Found: Nike (active)
├── Found: Fitness App
└── Found: Local Bakery

Active Account: Nike
├── Ad Account: act_123456789
├── Currency: BRL
├── Pixel: 987654321
└── Last Used: 2024-03-29 16:00

What would you like to do?
├── [1] Create new campaign
├── [2] Analyze performance
├── [3] Switch account
├── [4] Add new account
└── [5] Other action
```

---

## Phase 0: Intelligent Context Gathering

### 0.1 Initial Assessment

Before any action, analyze the user's request and determine what information is needed.

**Respond with a structured questionnaire based on context:**

```
=== META ADS SETUP CHECKLIST ===

Analyzing your request...

✓ Understanding: [Your interpretation of what user wants]
? Missing: [Information needed to proceed]

Please provide the following information:
```

### 0.2 Context Templates

#### Template A: New Campaign Setup

```
=== NEW CAMPAIGN SETUP ===

I understand you want to create a new Meta Ads campaign. To set this up correctly, I need:

REQUIRED (must have):
├── [1] Access Token: Your Graph API access token
│   └── Get from: https://developers.facebook.com/tools/explorer/
│   └── Permissions needed: ads_management, ads_read, pages_read_engagement
│
├── [2] Ad Account ID: The account to run ads (format: 123456789)
│   └── Find at: https://business.facebook.com/settings/ad-accounts
│
├── [3] Business/Brand Name: For campaign naming
│   └── Example: "Nike", "Fitness App", "Local Bakery"
│
├── [4] Campaign Objective: What's the goal?
│   ├── [ ] Sales (E-commerce, products)
│   ├── [ ] Leads (Forms, consultations)
│   ├── [ ] Traffic (Website visits)
│   ├── [ ] Awareness (Brand visibility)
│   ├── [ ] App Installs
│   ├── [ ] Messages (WhatsApp/Messenger)
│   └── [ ] Video Views
│
├── [5] Budget: Daily or lifetime amount
│   └── Minimum recommended: $5-10/day for testing
│
└── [6] Landing Page: Where ads will send users
    └── Must have pixel/CAPI installed for conversion tracking

OPTIONAL (enhance performance):
├── [7] Target Audience: Who's your ideal customer?
│   ├── Age range: ___ to ___
│   ├── Gender: [ ] All [ ] Male [ ] Female
│   ├── Location: ________________________
│   ├── Interests: ________________________
│   └── Behaviors: _______________________
│
├── [8] Creative Assets: Where are your images/videos?
│   ├── [ ] I have images (provide path/URL)
│   ├── [ ] I have videos (provide path/URL)
│   ├── [ ] Need creative creation
│   └── [ ] Use existing page content
│
├── [9] Pixel ID: For conversion tracking
│   └── Find at: https://business.facebook.com/settings/pixels
│
├── [10] Page/IG Account: Which account to promote from?
│
└── [11] Special Considerations:
    ├── [ ] Housing/Employment ads (special categories)
    ├── [ ] Credit ads (special categories)
    ├── [ ] Political/Social issues
    └── [ ] Healthcare/Pharmaceuticals

Please provide the information above. You can say:
- "Use defaults" if you want recommendations for missing items
- "Skip optional" if you only want to provide required fields
```

### 0.3 Smart Follow-up Questions

**If objective is "Sales":**
```
For Sales campaigns, I need to understand:
1. Is this e-commerce (online store) or lead to offline sale?
2. Do you have a product catalog? (for dynamic ads)
3. What's your average order value? $_____
4. Do you have existing customer data for lookalikes? [ ] Yes [ ] No
5. Target CPA or ROAS goal?
```

**If objective is "Leads":**
```
For Lead campaigns:
1. Use Meta Lead Forms or website forms?
2. What information to collect? (name, email, phone, company, etc.)
3. Target cost per lead: $_____
4. How will leads be followed up?
```

**If objective is "App Installs":**
```
For App Install campaigns:
1. Platform: [ ] iOS [ ] Android [ ] Both
2. App Store links ready?
3. Target cost per install: $_____ (iOS) $_____ (Android)
4. App events set up? (for optimization)
```

---

## Phase1: API Connection & Validation

### 1.1 Validate Access Token

```bash
curl -X GET "https://graph.facebook.com/v21.0/me?fields=id,name,permissions&access_token={ACCESS_TOKEN}"
```

**Required Permissions:**
| Permission | Purpose | Priority |
|------------|---------|----------|
| `ads_management` | Create/edit campaigns | Required |
| `ads_read` | Read campaign data | Required |
| `pages_read_engagement` | Access page content | Required |
| `pages_manage_ads` | Create ads for pages | Required |
| `instagram_basic` | Instagram account access | Optional |
| `catalog_management` | Product catalogs | For dynamic ads |

### 1.2 Get Ad Accounts

```bash
curl -X GET "https://graph.facebook.com/v21.0/me/adaccounts?fields=id,name,account_status,amount_spent,currency,timezone_name&access_token={ACCESS_TOKEN}"
```

### 1.3 Validate Ad Account

```bash
curl -X GET "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}?fields=id,name,account_status,spend_cap,amount_spent,currency,timezone_name&access_token={ACCESS_TOKEN}"
```

**Account Status Codes:**
| Status | Meaning | Action |
|--------|---------|--------|
| `1` | Active | Ready to use |
| `2` | Disabled | Cannot create ads |
| `7` | Pending Review | Wait for approval |
| `8` | Pending Closure | Limited functionality |
| `9` | Closed | Account closed |

---

## Phase 2: Campaign Structure Planning

### 2.1 Campaign Objective Mapping

| Business Goal | Objective | API Value |
|---------------|-----------|-----------|
| Website Sales | Sales | `OUTCOME_SALES` |
| Lead Generation | Leads | `OUTCOME_LEADS` |
| Website Traffic | Traffic | `OUTCOME_TRAFFIC` |
| Brand Awareness | Awareness | `OUTCOME_AWARENESS` |
| App Installs | App Promotion | `OUTCOME_APP_PROMOTION` |
| Video Views | Engagement | `OUTCOME_ENGAGEMENT` |
| Messages | Messages | `OUTCOME_MESSAGES` |

### 2.2 Naming Convention

```
{Brand}_{Product}_{Objective}_{Audience}_{Funnel}_{Date}

Examples:
- Nike_AirMax_Sales_Lookalike_TOF_20240115
- FitnessApp_Installs_Interest_Fitness_TOF_20240115
```

---

## Phase 3: Campaign Creation

### 3.1 Create Campaign

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/campaigns" \
  -d "name={CAMPAIGN_NAME}" \
  -d "objective={OBJECTIVE}" \
  -d "status=PAUSED" \
  -d "special_ad_categories=[]" \
  -d "bid_strategy=LOWEST_COST_WITHOUT_CAP" \
  -d "access_token={ACCESS_TOKEN}"
```

### 3.2 Set Campaign Budget (CBO)

```bash
# Daily budget
curl -X POST "https://graph.facebook.com/v21.0/{CAMPAIGN_ID}" \
  -d "daily_budget={AMOUNT_CENTS}" \
  -d "access_token={ACCESS_TOKEN}"

# Lifetime budget
curl -X POST "https://graph.facebook.com/v21.0/{CAMPAIGN_ID}" \
  -d "lifetime_budget={AMOUNT_CENTS}" \
  -d "access_token={ACCESS_TOKEN}"
```

**Budget Format:** Amount in cents ($10.00 → `1000`)

---

## Phase 4: Ad Set Creation

### 4.1 Create Ad Set

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/adsets" \
  -d "name={ADSET_NAME}" \
  -d "campaign_id={CAMPAIGN_ID}" \
  -d "optimization_goal={GOAL}" \
  -d "billing_event={EVENT}" \
  -d "daily_budget={BUDGET}" \
  -d "targeting={TARGETING_JSON}" \
  -d "status=PAUSED" \
  -d "access_token={ACCESS_TOKEN}"
```

### 4.2 Optimization Goals

| Objective | Optimization Goal | Billing Event |
|-----------|-------------------|---------------|
| Sales | OFFSITE_CONVERSIONS | IMPRESSIONS |
| Leads | OFFSITE_CONVERSIONS | IMPRESSIONS |
| Traffic | LINK_CLICKS | IMPRESSIONS |
| Awareness | REACH | IMPRESSIONS |
| App Installs | APP_INSTALLS | IMPRESSIONS |
| Video Views | THRUPLAY | IMPRESSIONS |

### 4.3 Targeting Parameters

```json
{
  "geo_locations": {"countries": ["US", "BR"]},
  "age_min": 25,
  "age_max": 55,
  "genders": [1, 2],
  "flexible_spec": [{
    "interests": [
      {"id": "6003139267375", "name": "E-commerce"}
    ],
    "behaviors": [
      {"id": "6007100278516", "name": "Engaged shoppers"}
    ]
  }]
}
```

---

## Phase 5: Audience Creation

### 5.1 Website Custom Audience

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/customaudiences" \
  -d "name={NAME}" \
  -d "subtype=CUSTOM" \
  -d "retention_days=30" \
  -d "rule={RULE}" \
  -d "access_token={ACCESS_TOKEN}"
```

### 5.2 Lookalike Audience

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/customaudiences" \
  -d "name={NAME}_LAL" \
  -d "subtype=LOOKALIKE" \
  -d "origin_audience_id={SOURCE_ID}" \
  -d 'lookalike_spec={"country":"US","ratio":0.01}' \
  -d "access_token={ACCESS_TOKEN}"
```

---

## Phase 6: Creative Management

### 6.1 Upload Image

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/adimages" \
  -d "url={IMAGE_URL}" \
  -d "access_token={ACCESS_TOKEN}"
```

### 6.2 Upload Video

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/advideos" \
  -F "source=@{VIDEO_PATH}" \
  -d "access_token={ACCESS_TOKEN}"
```

### 6.3 Create Creative

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/adcreatives" \
  -d "name={NAME}" \
  -d "object_story_spec={SPEC}" \
  -d "access_token={ACCESS_TOKEN}"
```

---

## Phase 7: Ad Creation

### 7.1 Create Ad

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/ads" \
  -d "name={AD_NAME}" \
  -d "adset_id={ADSET_ID}" \
  -d 'creative={"creative_id":"{ID}"}' \
  -d "status=PAUSED" \
  -d "access_token={ACCESS_TOKEN}"
```

---

## Phase 8: Pixel & Conversions API

### 8.1 Create Pixel

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/pixels" \
  -d "name={NAME}" \
  -d "access_token={ACCESS_TOKEN}"
```

### 8.2 Standard Events

| Event | Use Case |
|-------|----------|
| `PageView` | Default tracking |
| `ViewContent` | Product views |
| `AddToCart` | Cart additions |
| `Purchase` | Transactions |
| `Lead` | Lead forms |
| `CompleteRegistration` | Sign ups |

---

## Phase 9: Analytics

### 9.1 Campaign Insights

```bash
curl -X GET "https://graph.facebook.com/v21.0/{CAMPAIGN_ID}/insights?fields=spend,impressions,clicks,ctr,cpc,cpm,reach,frequency,actions,cost_per_action,purchase_roas&date_preset=last_30d&access_token={ACCESS_TOKEN}"
```

### 9.2 Key Metrics

| Metric | Formula | Good Range |
|--------|---------|------------|
| CPM | `spend / impressions * 1000` | $5-25 |
| CPC | `spend / clicks` | $0.50-3.00 |
| CTR | `clicks / impressions * 100` | 0.5-2% |
| CPA | `spend / actions` | Varies |
| ROAS | `revenue / spend` | 3:1+ |
| Frequency | `impressions / reach` | 1-3 |

### 9.3 Performance Analysis Template

```
=== CAMPAIGN ANALYSIS ===

Campaign: {NAME} | Period: {DATE_RANGE}

PERFORMANCE SUMMARY:
├── Spend: $X,XXX
├── Impressions: X,XXX,XXX
├── Reach: X,XXX,XXX
├── CPM: $XX.XX
├── CPC: $X.XX
├── CTR: X.XX%
├── Frequency: X.X
└── ROAS: X.Xx

CONVERSION FUNNEL:
├── Clicks → Landing Views: XX%
├── Landing Views → Adds to Cart: XX%
├── Adds to Cart → Checkout: XX%
└── Checkout → Purchase: XX%

INSIGHTS:
✓ [Strength]
✓ [Good metric]
⚠ [Improvement area]
⚠ [Below benchmark]

RECOMMENDATIONS:
1. [Action item]
2. [Optimization]
3. [Creative suggestion]
```

---

## Phase 10: Budget Optimization

### 10.1 Scaling Rules

| Stage | Increase | Frequency |
|-------|-----------|-----------|
| Testing | $5-10/day | - |
| Learning | 20-30% | Every 3 days |
| Scaling | 20-30% | Every 5-7 days |
| Mature | 10-20% | Every 7-14 days |

**⚠️ Never increase by more than 50% - resets learning.**

---

## Error Handling

| Code | Description | Solution |
|------|-------------|----------|
| `1` | Invalid parameter | Check format |
| `100` | Invalid token | Refresh token |
| `190` | Token expired | Get new token |
| `200` | Missing permissions | Add permission |
| `17` | Rate limit | Wait or batch |
| `274` | Too many ads | Archive unused |

---

## Cross-Skill Integration

- `/market ads` - Creative and copy generation
- `/market funnel` - Funnel structure alignment
- `/market landing` - Landing page optimization
- `/analytics-tracking` - Pixel troubleshooting
- `/market audit` - Campaign performance review
---

## Phase -1: Campaign Folder Structure & Creative Management

### -1.1 Folder Structure

The agent manages campaign assets in a structured folder hierarchy:

```
/campanhas/                              # Campaigns root directory
├── {cliente}/                           # Client name (e.g., nike, fitness_app)
│   ├── {YYYY-MM}/                       # Month (e.g., 2024-01, 2024-02)
│   │   ├── {campanha_name}/             # Campaign folder (e.g., black_friday, lancamento_produto
│   │   │   ├── briefing.md              # Campaign briefing (or briefing.docx)
│ │   │   ├── analise.md                # Manager analysis/notes (optional)
│   │   │   ├── ad_01_feed_image.jpg    # Creative 1 - Feed image
│   │   │   ├── ad_01_feed_video.mp4    # Creative 1 - Feed video version
│   │   │   ├── ad_02_story_video.mp4   # Creative 2 - Stories video
│   │   │   ├── ad_02_reels_video.mp4   # Creative 2 - Reels version
│   │   │   ├── ad_03_carousel_01.jpg# Creative 3 - Carousel card 1
│   │   │   ├── ad_03_carousel_02.jpg# Creative 3 - Carousel card 2
│   │   │   ├── ad_03_carousel_03.jpg    # Creative 3 - Carousel card 3
│   │   │   └── resultados.md           # Results doc (created after campaign)
│ │   ├── {outra_campanha}/
│ │   │   └── ...
│ │   └── ...│ └── ...└── {outro_cliente}/
    └── ...
```

### -1.2 Creative Naming Convention

**Format:** `ad_{number}_{placement}_{type}.{extension}`

| Component | Values | Example |
|-----------|--------|---------|
| `number` | 01, 02, 03... | `ad_01` |
| `placement` | feed, story, reels, carousel, landscape | `feed` |
| `type` | image, video, carousel | `image` |
| `extension` | jpg, png, mp4, mov | `.jpg` |

**Examples:**
- `ad_01_feed_image.jpg` - First creative, feed format, image
- `ad_01_feed_video.mp4` - First creative, feed format, video
- `ad_02_story_video.mp4` - Second creative, stories, video
- `ad_02_reels_video.mp4` - Second creative, reels, video
- `ad_03_carousel_01.jpg` - Third creative, carousel card 1
- `ad_03_carousel_02.jpg` - Third creative, carousel card 2

### -1.3 Before Creating Campaign: Read & Analyze

**STEP 1: Identify Client Folder**

```
Agent asks: "Qual cliente/vendedor você quer trabalhar?"

User provides: "Nike" or "Fitness App" or client name

Agent searches: /campanhas/{cliente}/
```

**STEP 2: Find Active Month/Campaign**

```bash
# List available months for client
ls -la /campanhas/nike/

# Output: 2024-01/  2024-02/  2024-03/

# List campaigns in current month
ls -la /campanhas/nike/2024-03/
```

**STEP 3: Read Briefing Document**

```bash
# Read the briefing
cat /campanhas/nike/2024-03/black_friday/briefing.md

# If DOCX, extract text
python3 -c "
from docx import Document
doc = Document('/campanhas/nike/2024-03/black_friday/briefing.docx')
for para in doc.paragraphs:
    print(para.text)
"
```

### -1.4 Briefing Document Structure

**File:** `briefing.md` or `briefing.docx`

```markdown
# Campaign Briefing: {Campaign_Name}

## Client Information
- **Client:** {Client_Name}
- **Product/Service:** {What being promoted}
- **Industry:** {Industry}
- **Brand Voice:** {Tone: Professional/Casual/Fun/etc.}

## Campaign Objectives
- **Primary Goal:** [Sales/Leads/Traffic/Awareness/App Installs]
- **Secondary Goals:** [Brand recognition, Email capture, etc.]
- **Target CPA:** $XX.XX
- **Target ROAS:** X.Xx
- **Budget:** $X,XXX/month

## Target Audience
- **Demographics:** Age range, Gender, Location
- **Interests:** List of relevant interests
- **Behaviors:** Purchase behaviors, device usage
- **Pain Points:** What problems does the product solve?
- **Desires:** What does the audience want to achieve?

## Unique Selling Propositions
1. {USP 1}
2. {USP 2}
3. {USP 3}

## Key Messages
- **Primary Message:** {Main message}
- **Secondary Messages:** {Supporting points}
- **Objections to Handle:** {Common objections}

## Creative Direction
- **Visual Style:** {Modern/Classic/Minimal/etc.}
- **Color Palette:** {Colors to use}
- **Imagery:** {Types of images/videos}
- **Do's:** {What to include}
- **Don'ts:** {What to avoid}

## Landing Page
- **URL:** {Landing page URL}
- **Key Features:** {What's on the page}
- **CTA:** {Call to action on page}

## Competitors
- **Competitor 1:** {Name, their approach}
- **Competitor 2:** {Name, their approach}
- **Differentiation:** {How we're different}

## Timeline
- **Start Date:** {YYYY-MM-DD}
- **End Date:** {YYYY-MM-DD}
- **Key Dates:** {Sales, launches, etc.}

## Previous Performance (if applicable)
- **Best CPA:** $XX.XX
- **Best ROAS:** X.Xx
- **Top Performing Creative:** {Description}
- **Top Performing Audience:** {Description}

## Notes from Manager
{Additional context, insights, preferences}
```

### -1.5 Analyze Existing Creatives

Before writing ad copy, analyze all uploaded creatives:

```bash
# List all creatives in campaign folder
ls -la /campanhas/nike/2024-03/black_friday/

# Output:
# ad_01_feed_image.jpg
# ad_01_feed_video.mp4
# ad_02_story_video.mp4
# ad_03_carousel_01.jpg
# ad_03_carousel_02.jpg
# ad_03_carousel_03.jpg
```

**Creative Analysis Template:**

```markdown
=== CREATIVE ANALYSIS ===

Campaign Folder: /campanhas/nike/2024-03/black_friday/

CREATIVES FOUND:
├── ad_01_feed_image.jpg (1080x1080, image)
├── ad_01_feed_video.mp4 (1080x1080, video, ~30s)
├── ad_02_story_video.mp4 (1080x1920, video, ~15s)
├── ad_03_carousel_01.jpg (1080x1080, carousel card 1)
├── ad_03_carousel_02.jpg (1080x1080, carousel card 2)
└── ad_03_carousel_03.jpg (1080x1080, carousel card 3)

ANALYSIS:
├── Creative 1 (ad_01): Feed-focused, product showcase
│   ├── Formats: Image + Video
│   ├── Placement: Feed
│   └── Best for: Cold audience, awareness
│
├── Creative 2 (ad_02): Story/Reels format
│   ├── Format: Video only
│   ├── Placement: Stories, Reels
│   └── Best for: Engagement, awareness
│
└── Creative 3 (ad_03): Carousel
    ├── Formats: 3 images
    ├── Placement: Feed carousel
    └── Best for: Product comparison, warm audience

RECOMMENDED AD STRUCTURE:
├── AdSet 1 (Cold/TOF): ad_01_feed_image.jpg + ad_01_feed_video.mp4
├── AdSet 2 (Cold/TOF): ad_02_story_video.mp4
└── AdSet 3 (Warm/MOF): ad_03_carousel_01-03.jpg

COPY DIRECTION:Based on creatives:
- ad_01: Highlight product features, use hero image
- ad_02: Use urgency for stories, short-form message
- ad_03: Compare products in carousel, use numbers/benefits
```

### -1.6 Generate Ad Copy Based on Creative + Briefing

After analyzing briefing and creatives, generate ad copy:

```markdown
=== AD COPY GENERATION ===

Based on:
- Briefing: /campanhas/nike/2024-03/black_friday/briefing.md
- Creatives: 3 ad sets with 6 total assets

CREATIVE 1: ad_01_feed_image.jpg + ad_01_feed_video.mp4
├── PRIMARY TEXT (125 chars):
│   "{USP from briefing - focus on main benefit}"
│
├── PRIMARY TEXT LONG (300 chars):
│   "{Expanded message with social proof}"
│   "{Key features from briefing}"
│   "{CTA}"
│
├── HEADLINE (40 chars):
│   "{Hook - question or bold statement}"
│
├── DESCRIPTION (30 chars):
│   "{Supporting detail or offer}"
│
└── CTA: {SHOP_NOW|LEARN_MORE|SIGN_UP}

[Repeat for each creative...]

A/B TESTING VARIATIONS:
For each creative, generate:
├── Variation A: Problem-solution angle
├── Variation B: Social proof angle
└── Variation C: Urgency/offer angle
```

### -1.7 Upload Creatives to Meta

**Step-by-step process:**

```bash
# 1. Upload each creative to Meta
for creative in /campanhas/nike/2024-03/black_friday/ad_*.jpg; do
  echo "Uploading: $creative"
  # Upload to Meta
done

# 2. Store returned hashes/IDs
# 3. Create ads with uploaded creatives
```

**Upload Script:**

```bash
# Upload image
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/adimages" \
  -F "source=@/campanhas/nike/2024-03/black_friday/ad_01_feed_image.jpg" \
  -d "access_token={ACCESS_TOKEN}"

# Returns: {"images": {"hash": "abc123..."}}
# Store hash for later use in creative creation
```

### -1.8 Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    CAMPAIGN CREATION WORKFLOW                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│1. ASK: Client/Project name                                      │
│    └── User: "Nike"                                              │
│                                                                 │
│  2. FIND: Client folder                                         │
│     └── /campanhas/nike/                                         │
│                                                                 │
│  3. FIND: Active month/campaign                                  │
│     └── /campanhas/nike/2024-03/black_friday/                    │
│                                                                 │
│  4. READ: briefing.md (or .docx)                                 │
│     └── Extract: Objectives, Target, USPs, Key Messages          │
│                                                                 │
│  5. READ: analise.md (if exists)                                 │
│     └── Manager insights, previous learnings                     │
│                                                                 │
│  6. LIST: All creatives                                          │
│     └── ad_01_feed_image.jpg                                     │
│     └── ad_01_feed_video.mp4                                     │
│     └── ad_02_story_video.mp4                                    │
│     └── ad_03_carousel_01-03.jpg                                 │
│                                                                 │
│  7. ANALYZE: Creatives + Briefing                                 │
│     └── Understand product, audience, messaging                   │
│     └── Match creatives to funnel stages                         │
│     └── Identify best placements                                 │
│                                                                 │
│  8. GENERATE: Ad copy variations                                  │
│     └── Based on USPs from briefing                               │
│     └── Aligned with creative content                             │
│     └── A/B test variations                                      │
│                                                                 │
│  9. ASK: Missing information                                     │
│     └── Access Token, Ad Account ID, Budget                      │
│     └── Show copy preview for approval                           │
│                                                                 │
│10. UPLOAD: Creatives to Meta                                     │
│     └── Get image hashes                                         │
│     └── Get video IDs                                            │
│                                                                 │
│11. CREATE: Campaign structure                                    │
│     └── Campaign → Ad Sets → Ads                                 │
│     └── Attach creatives                                         │
│                                                                 │
│12. PAUSE: Campaign created in PAUSED state                        │
│     └── User reviews before activation                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### -1.9 Example: Full Campaign Creation

**User Request:**
```
'Crie uma campanha para a Nike no Black Friday'
```

**Agent Response:**
```
=== CRIANDO CAMPANHA: NIKE BLACK FRIDAY ===

Passo 1: Localizando cliente...
✓ Cliente encontrado: /campanhas/nike/

Passo 2: Localizando mês/campanha...
✓ Mês: 2024-03
✓ Campanha: black_friday

Passo 3: Lendo briefing...
✓ briefing.md encontrado

=== BRIEFING RESUMO ===
Cliente: Nike
Produto: Air Max Collection
Objetivo: Sales (Vendas)
Target CPA: $15
Budget: $5000/mês
Público: 18-35 anos, interessados em fitness, corridaUSPs:
1. технология Air Max para máximo conforto
2. Design icônico há 30 anos
3. Edição especial Black Friday com 40% desconto

Passo 4: Lendo análise do gestor...
✓ analise.md encontrado
→ Insight: Campanhas anteriores com vídeo de 15s tiveram 30% mais conversões
→ Dica: Evitar "livre" na copy, usar "grátis" ou "sem custo"

Passo 5: Listando criativos...
✓ ad_01_feed_image.jpg (1080x1080)
✓ ad_01_feed_video.mp4 (1080x1080, 30s)
✓ ad_02_story_video.mp4 (1080x1920, 15s)
✓ ad_03_carousel_01.jpg (1080x1080)
✓ ad_03_carousel_02.jpg (1080x1080)
✓ ad_03_carousel_03.jpg (1080x1080)

Passo 6: Analisando criativos...

=== ANÁLISE DE CRIATIVOS ===

ad_01 (Feed):Imagem mostra tênis em fundo branco com logo Nike
Vídeo demonstra tecnologia Air Max em ação
→ Use para: Topo de funil, awareness
→ Copy: Focar em inovação e conforto

ad_02 (Stories/Reels):
Vídeo curto com modelo usando o tênis
→ Use para: Stories, Reels, engajamento
→ Copy: Urgência, limited offer

ad_03 (Carousel):
3/cards comparando modelos da coleção
→ Use para: Meio de funil, consideração
→ Copy: Comparação de modelos, benefícios

Passo 7: Gerando copies...=== COPIES GERADAS ===

CREATIVE 1: ad_01_feed (Feed)

Primary Text (125 chars):
"Nova Air Max com tecnologia de amortecimento.
Conforto que você sente em cada passo."
→ Análise: Foco em USP 1, copy curta

Primary Text Long (300 chars):
"Air Max: 30 anos de inovação em cada passo.
Com tecnologia Air Max, você tem o máximo 
conforto e estilo que só a Nike oferece.
Black Friday: 40% OFF. Aproveite!"
→ Análise: Inclui USPs 1e 2, offer clarity

Headline: "Air Max: Seu Próximo Passo"
Description: "40% OFF Black Friday"

A/B VARIATIONS:
A (Problema): "Cansado de tênis desconfortáveis?"
B (Social): "Mais de 1 milhãode corredores confiam"
C (Urgência): "Últimas unidades - 40% OFF"

[... continua para outros criativos ...]

Passo8: Informações necessárias para criar a campanha:

├── [1] Access Token: ___
├── [2] Ad Account ID: ___
├── [3] Budget diário: $___ (sugestão: $166/dia para $5000/mês)
├── [4] Pixel ID: ___
└── [5] Página do Facebook: ___

Se as copies estiverem OK, forneça as informações acima
para criar a campanha no Meta Ads.
```

### -1.10 Results Documentation

After campaign launch, create/update `resultados.md`:

```markdown
# Resultados da Campanha: {Campaign_Name}

## Informações Gerais
- **Data Início:** {start_date}
- **Data Fim:** {end_date}
- **Budget Total:** ${total_budget}

## Métricas Principais
| Métrica | Valor |Meta | Status |
|---------|-------|------|--------|
| Spend | $XXX |$XXX | ✓/✗ |
| Impressions | XX,XXX | XX,XXX | ✓/✗ |
| Reach | XX,XXX | XX,XXX | ✓/✗ |
| CPM | $X.XX | $X.XX | ✓/✗ |
| CPC | $X.XX | $X.XX | ✓/✗ |
| CTR | X.XX% | X.XX% | ✓/✗ |
| Conversions | XXX | XXX | ✓/✗ |
| CPA | $XX.XX | $XX.XX | ✓/✗ |
| ROAS | X.Xx | X.Xx | ✓/✗ |

## Performance por Ad Set
| Ad Set | Spend | CPA | ROAS | Status |
|--------|-------|-----|------|--------|
| TOF_Cold | $XXX | $XX | X.Xx | Active |
| MOF_Warm | $XXX | $XX | X.Xx | Active |
| BOF_Hot | $XXX | $XX | X.Xx | Active |

## Performance por Criativo
| Creative | Impressions | CTR | CPA | ROAS | Status |
|----------|-------------|-----|-----|------|--------|
| ad_01_feed_image | XX,XXX | X.XX% | $XX | X.Xx | Active |
| ad_01_feed_video | XX,XXX | X.XX% | $XX | X.Xx | Active |
| ad_02_story_video | XX,XXX | X.XX% | $XX | X.Xx | Paused |
| ad_03_carousel | XX,XXX | X.XX% | $XX | X.Xx | Active |

## Insights
- [Learning from creative performance]
- [Audience insights]
- [Best practices identified]

## Recomendações
- [Scale winning ads]
- [Pause underperformers]
- [Test new creatives]
- [Adjust budgets]
```

---

## Folder Commands

### List Clients

```bash
ls -la /campanhas/
```

### List Campaigns for Client

```bash
ls -la /campanhas/{cliente}/
ls -la /campanhas/nike/2024-03/
```

### Read Briefing

```bash
# Markdown
cat /campanhas/{cliente}/{mes}/{campanha}/briefing.md

# DOCX (if python-docx available)
python3 -c "
from docx import Document
doc = Document('/path/to/briefing.docx')
for para in doc.paragraphs:
    print(para.text)
"
```

### Create New Campaign Folder

```bash
mkdir -p /campanhas/{cliente}/{mes}/{campanha_name}
touch /campanhas/{cliente}/{mes}/{campanha_name}/briefing.md
```

---

## Phase 11: Advanced Bidding Strategies

### 11.1 Bid Strategy Types

| Strategy | Use Case | Pros | Cons |
|----------|----------|------|------|
| `LOWEST_COST_WITHOUT_CAP` | Learning phase, new accounts | Max delivery | Unstable CPA |
| `COST_CAP` | Stable CPA goal | Predictable costs | May limit delivery |
| `BID_CAP` | Auction control | Hard budget control | May miss opportunities |
| `LOWEST_COST_WITH_BID_CAP` | Value campaigns | Max value | Complex setup |

### 11.2 Cost Cap (CPA Goal)

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/adsets" \
  -d "name={ADSET_NAME}" \
  -d "campaign_id={CAMPAIGN_ID}" \
  -d "bid_strategy=COST_CAP" \
  -d "bid_amount={TARGET_CPA_CENTS}" \
  -d "daily_budget={BUDGET_CENTS}" \
  -d "optimization_goal=OFFSITE_CONVERSIONS" \
  -d "billing_event=IMPRESSIONS" \
  -d "targeting={TARGETING_JSON}" \
  -d "promoted_object={CONVERSION_OBJECT}" \
  -d "access_token={ACCESS_TOKEN}"
```

**Example:** Target CPA of $15 → `bid_amount=1500` (cents)

### 11.3 Bid Cap (Maximum Bid)

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/adsets" \
  -d "bid_strategy=BID_CAP" \
  -d "bid_amount={MAX_BID_CENTS}" \
  -d "daily_budget={BUDGET_CENTS}" \
  -d "access_token={ACCESS_TOKEN}"
```

### 11.4 ROAS Goal Optimization

```bash
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/adsets" \
  -d "name={ADSET_NAME}" \
  -d "campaign_id={CAMPAIGN_ID}" \
  -d "bid_strategy=LOWEST_COST_WITHOUT_CAP" \
  -d "optimization_goal=OFFSITE_CONVERSIONS" \
  -d "destination_type=WEBSITE" \
  -d "daily_budget={BUDGET_CENTS}" \
  -d "targeting={TARGETING_JSON}" \
  -d "promoted_object={'pixel_id':'{PIXEL_ID}','custom_event_type':'Purchase'}" \
  -d "access_token={ACCESS_TOKEN}"
```

### 11.5 When to Use Each Strategy

| Scenario | Recommended Strategy | Notes |
|----------|---------------------|-------|
| New campaign, learning | `LOWEST_COST_WITHOUT_CAP` | Let algorithm optimize |
| Stable CPA needed | `COST_CAP` | Set realistic target |
| Budget constraint | `BID_CAP` | Hard limit on spend |
| E-commerce with value data | ROAS optimization | Need pixel value tracking |
| Lead gen with known CPL | `COST_CAP` | Set CPL as bid amount |

---

## Phase 12: A/B Testing Framework

### 12.1 Testing Hierarchy

```
Testing Priority:
├── 1. Structural Tests (2-4 weeks)
│   ├── Placement tests (Feed vs Stories vs Reels)
│   ├── Audience tests (Interest vs Lookalike vs Custom)
│   └── Objective tests (Conversions vs Traffic)
│
├── 2. Creative Tests (1-2 weeks)
│   ├── Format tests (Image vs Video vs Carousel)
│   ├── Hook tests (First 3 seconds)
│   └── CTA tests (Shop Now vs Learn More)
│
└── 3. Copy Tests (3-7 days)
    ├── Headline tests
    ├── Primary text tests
    └── Description tests
```

### 12.2 Testing Rules

- **One variable at a time**
- **Minimum 100 conversions per variation**
- **Minimum 7 days duration**
- **Statistical significance: 95%+ confidence**
- **Never pause during learning phase**

### 12.3 Test Template

```markdown
=== A/B TEST PLAN ===

Test Name: {Test_Name}
Hypothesis: {What we're testing and why}
Duration: {Start_Date} to {End_Date}
Budget: ${Daily_Budget} per variation

Control (A):
├── Creative: {Current_best}
├── Copy: {Current_copy}
├── CTR: {Historical_CTR}%
├── CPA: ${Historical_CPA}
└── Expected: {Baseline_metrics}

Variant (B):
├── Creative: {New_creative}
├── Copy: {New_copy}
└── Expected: {Hypothesis_metrics}

Success Metric: {Primary_KPI}
Secondary Metrics: {Secondary_KPIs}
Statistical Confidence: 95%

Sample Size Calculator:
- Baseline conversion rate: {CR}%
- Minimum Detectable Effect: {MDE}%
- Required sample size: {N} per variation
```

### 12.4 Statistical Significance

```python
# A/B Test Significance Calculator
import math

def calculate_significance(control_cr, control_n, variant_cr, variant_n):
    """
    Calculate statistical significance for A/B test.
    
    Args:
        control_cr: Control conversion rate (e.g., 0.02 for 2%)
        control_n: Control sample size (impressions or users)
        variant_cr: Variant conversion rate
        variant_n: Variant sample size
    
    Returns:
        Dictionary with z-score, p-value, and significance
    """
    # Pooled conversion rate
    pooled_cr = (control_cr * control_n + variant_cr * variant_n) / (control_n + variant_n)
    
    # Standard error
    se = math.sqrt(pooled_cr * (1 - pooled_cr) * (1/control_n + 1/variant_n))
    
    # Z-score
    z_score = (variant_cr - control_cr) / se if se > 0 else 0
    
    # P-value (one-tailed)
    from scipy import stats
    p_value = 1 - stats.norm.cdf(z_score)
    
    return {
        'z_score': round(z_score, 3),
        'p_value': round(p_value, 4),
        'significant': p_value < 0.05,
        'confidence': round((1 - p_value) * 100, 1),
        'lift': round((variant_cr - control_cr) / control_cr * 100, 1) if control_cr > 0 else 0
    }
```

### 12.5 Test Analysis Template

```markdown
=== A/B TEST RESULTS ===

Test: {Test_Name}
Duration: {Days} days
Total Spend: ${Spend}

CONTROL (A):
├── Impressions: {Imp}
├── Clicks: {Clicks}
├── Conversions: {Conv}
├── CTR: {CTR}%
├── CPA: ${CPA}
└── ROAS: {ROAS}x

VARIANT (B):
├── Impressions: {Imp}
├── Clicks: {Clicks}
├── Conversions: {Conv}
├── CTR: {CTR}%
├── CPA: ${CPA}
└── ROAS: {ROAS}x

STATISTICAL ANALYSIS:
├── Z-Score: {Z}
├── P-Value: {P}
├── Confidence: {Conf}%
├── Lift: {Lift}%
└── Significant: {Yes/No}

DECISION: {Winner/Inconclusive}
ACTION: {Scale/Pause/Test more}
```

---

## Phase 13: Scaling Playbook

### 13.1 Scaling Phases

```
Scaling Journey:
│
├── Phase 1: Learning (Day 1-7)
│   ├── Budget: $5-10/day per ad set
│   ├── Goal: 50 conversions per ad set
│   ├── Rule: DON'T TOUCH for 7 days
│   └── Monitor: CPM, CPC, CPA baseline
│
├── Phase 2: Testing (Day 8-21)
│   ├── Budget: Scale 20-30% every 3 days
│   ├── Goal: Find winning combinations
│   ├── Rule: Test 1 variable at a time
│   └── Monitor: CPA stability, ROAS
│
├── Phase 3: Scaling (Day 22-60)
│   ├── Horizontal: Add ad sets (new audiences)
│   ├── Vertical: Increase budget 20-30% every 5-7 days
│   ├── Rule: Never increase >50% at once
│   └── Monitor: Frequency, CPA trends
│
└── Phase 4: Optimization (Day 60+)
    ├── Pause losers (CPA > 1.5x target)
    ├── Scale winners (2x budget)
    ├── Refresh creatives every 4-6 weeks
    └── Rule: 70/20/10 budget split
        ├── 70% proven winners
        ├── 20% scaling new winners
        └── 10% testing new ideas
```

### 13.2 Scaling Trigger Rules

| CPA Performance | Action | Frequency |
|-----------------|--------|-----------|
| CPA < Target | Scale +30% | Every 3 days |
| CPA = Target to 1.2x | Monitor, no change | - |
| CPA = 1.2x to 1.5x | Pause weaker ads | Immediately |
| CPA > 1.5x Target | Pause and investigate | Immediately |

### 13.3 Scaling Checklist

```markdown
=== SCALING DECISION CHECKLIST ===

✅ READY TO SCALE IF:
├── [ ] CPA stable for 7+ days
├── [ ] Frequency < 2.0
├── [ ] ROAS > target
├── [ ] 100+ conversions
├── [ ] Creative age < 30 days
└── [ ] Learning phase complete

❌ DO NOT SCALE IF:
├── [ ] CPA increasing for 3+ days
├── [ ] Frequency > 4.0
├── [ ] CTR dropping week over week
├── [ ] ROAS < 50% of target
├── [ ] Learning phase still active
└── [ ] Creative fatigue signs
```

### 13.4 Budget Increase Rules

```python
# Safe Scaling Formula
def calculate_budget_increase(current_budget, days_running, current_cpa, target_cpa):
    """
    Calculate safe budget increase based on performance.
    
    Rules:
    - Never exceed 50% increase at once
    - Increase every 3-7 days only
    - Reduce increase amount if CPA rising
    """
    
    # Base increase percentage
    base_increase = 0.30  # 30%
    
    # Adjust for CPA ratio
    cpa_ratio = current_cpa / target_cpa
    
    if cpa_ratio > 1.2:
        # CPA too high, no increase
        return current_budget, "PAUSE - CPA above 1.2x target"
    elif cpa_ratio > 1.0:
        # CPA above target, smaller increase
        increase = min(base_increase * 0.5, 0.15)  # Max 15%
        reason = "CONSOLIDATE - Smaller increase, CPA elevated"
    else:
        # CPA on target or below, full increase
        increase = base_increase
        reason = "SCALE - CPA on target"
    
    # Calculate new budget
    new_budget = current_budget * (1 + increase)
    
    # Cap at 50% increase
    if new_budget > current_budget * 1.5:
        new_budget = current_budget * 1.5
        reason = "SCALE - Capped at 50% increase"
    
    return round(new_budget, 2), reason
```

---

## Phase 14: Diagnostic Trees

### 14.1 High CPC Diagnosis

```
High CPC (> $2)
│
├── Is CTR Normal (> 1%)?
│   ├── YES → Check CPCP (Cost Per Click Percentage)
│   │   └── CPCP high?
│   │       ├── YES → Bid strategy issue
│   │       │   └── Solution: Switch to COST_CAP
│   │       └── NO → Audience competiton
│   │           └── Solution: Expand audience or test new placements
│   │
│   └── NO (CTR < 1%)
│       ├── Is Creative Compelling?
│       │   ├── NO → Creative issue
│       │   │   └── Solution: Test new creatives, improve hook
│       │   └── YES → Audience issue
│       │       └── Solution: Refine targeting, test new audiences
│
└── Is Frequency High (> 3)?
    ├── YES → Audience saturation
    │   └── Solution: Expand to new audience, create lookalike
    └── NO → High competition/auction
        └── Solution: Test different times, placements, or bid strategy
```

### 14.2 Low ROAS Diagnosis

```
Low ROAS (< 2x)
│
├── Is Click Volume OK?
│   ├── NO → Traffic Issue
│   │   ├── CPM high? → Audience/Competition
│   │   │   └── Solution: Expand audience, test new placements
│   │   └── CPM low? → Bid low/Targeting narrow
│   │       └── Solution: Increase bid, expand targeting
│   │
│   └── YES → Conversion Issue
│       ├── Is CVR Low (< 1%)?
│       │   ├── YES → Landing page issue
│       │   │   ├── Check: Page speed (>3s load = bad)
│       │   │   ├── Check: Message match (ad → LP)
│       │   │   ├── Check: CTA clarity
│       │   │   └── Solution: Optimize landing page
│       │   │
│       │   └── NO (CVR OK)
│       │       └── AOV Low?
│       │           ├── YES → Upsell/cross-sell needed
│       │           │   └── Solution: Add upsell flow
│       │           └── NO → Attribution delay?
│       │               └── Solution: Use 7d click + 1d view attribution
│       │
│       └── Solution Path: Identify funnel stage issue
```

### 14.3 No Conversions Diagnosis

```
Zero Conversions (> 50 clicks)
│
├── Is Pixel Working?
│   ├── NO → Fix pixel/CAPI
│   │   ├── Check: Events firing
│   │   ├── Check: Parameters sent
│   │   ├── Check: Deduplication
│   │   └── Solution: Implement CAPI, test events
│   │
│   └── YES → Continue diagnosis
│       ├── Is Landing Page Loading?
│       │   ├── NO → Fix hosting/DNS
│       │   └── YES → Continue
│       │       ├── Is Message Match?
│       │       │   ├── NO → Align ad copy → LP
│       │       │   └── YES → Continue
│       │       │       ├── Is CTA Clear?
│       │       │       │   ├── NO → Add prominent CTA
│       │       │       │   └── YES → Continue
│       │       │       │       └── Check Page Speed
│       │       │       │           └── Solution: Optimize images/JS
```

### 14.4 Frequency Management

```
Frequency Too High (> 4)
│
├── Is Audience Size < 1M?
│   ├── YES → Audience too small
│   │   └── Solution: Expand to 2M+ people
│   └── NO → Continue
│       ├── Is Budget High for Audience?
│       │   ├── YES → Reduce budget or expand audience
│       │   └── NO → Creative fatigue
│       │       └── Solution: Refresh creatives
```

---

## Phase 15: Performance Optimization

### 15.1 Creative Optimization

```markdown
### Creative Optimization Checklist

HOOK TEST (First 3 seconds):
├── Test 5 different hooks
├── Keep top 2 performers
├── Rotate hooks every 2 weeks
└── Metrics: Hook rate > 75%, CTR > 1%

FORMAT OPTIMIZATION:
├── Video: 15s for Stories, 30s for Feed
├── Carousel: 3-5 cards max
├── Image: 1080x1080 or 1080x1350
└── Collection: Hero image + 4 products

CTA OPTIMIZATION:
├── E-commerce: Shop Now, Add to Cart
├── Lead Gen: Learn More, Sign Up
├── Traffic: Learn More, See More
└── Awareness: Watch More, Like Page
```

### 15.2 Audience Optimization

```bash
# Exclusion Layers
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/adsets" \
  -d "targeting={
    'geo_locations': {'countries': ['US']},
    'exclusions': {
      'custom_audiences': [{'id': '{PURCHASERS_LAST_30_DAYS}'}]
    }
  }" \
  -d "access_token={ACCESS_TOKEN}"
```

```markdown
### Audience Refresh Schedule

| Audience Type | Refresh Rate | Action |
|---------------|--------------|--------|
| Lookalike | Every 90 days | Create new from updated seed |
| Interest | Monthly | Test new segments |
| Custom | Quarterly | Update seed audience |
| Retargeting | Monthly | Adjust window based on performance |
```

### 15.3 Placement Optimization

```json
{
  "publisher_platforms": ["facebook", "instagram", "messenger"],
  "facebook_positions": ["feed", "marketplace", "video_feeds", "stories"],
  "instagram_positions": ["feed", "stories", "reels", "explore"],
  "device_platforms": ["mobile", "desktop"]
}
```

### 15.4 Optimization Signals Table

| Signal | Weight | Action |
|--------|--------|--------|
| Frequency > 4 | 🔴 High | Expand audience immediately |
| CTR < 0.5% | 🔴 High | Test new creative urgently |
| CPCP > 20% | 🟡 Medium | Review bid strategy |
| CPA > 1.5x target | 🔴 High | Pause and investigate |
| ROAS < target | 🔴 High | Optimize funnel |
| CVR fluctuation | 🟡 Medium | Check pixel/landing page |
| Learning exit | 🟢 Low | Ready to scale |

---

## Phase 16: Industry Benchmarks

### 16.1 E-commerce Benchmarks (2024)

| Vertical | CPM | CPC | CTR | CPA | ROAS | CVR |
|----------|-----|-----|-----|-----|------|-----|
| Fashion | $8-15 | $0.80-1.50 | 0.8-1.5% | $15-30 | 3-5x | 1-2% |
| Electronics | $10-20 | $1.00-2.00 | 0.6-1.2% | $20-40 | 4-6x | 0.8-1.5% |
| Beauty | $6-12 | $0.60-1.20 | 1.0-2.0% | $12-25 | 2.5-4x | 1.5-3% |
| Home | $8-18 | $0.90-1.60 | 0.7-1.4% | $18-35 | 3-5x | 0.9-1.8% |

### 16.2 Lead Generation Benchmarks

| Vertical | CPM | CPC | CTR | CPL |
|----------|-----|-----|-----|-----|
| B2B Services | $12-25 | $1.50-3.00 | 0.5-1.0% | $20-50 |
| Real Estate | $15-30 | $2.00-4.00 | 0.4-0.9% | $30-80 |
| Education | $8-18 | $1.00-2.00 | 0.6-1.2% | $15-35 |
| Healthcare | $10-22 | $1.20-2.50 | 0.5-1.1% | $25-55 |

### 16.3 App Install Benchmarks

| Vertical | CPI iOS | CPI Android | CTR | Retention D1 |
|----------|---------|-------------|-----|--------------|
| Gaming | $1.50-3.00 | $0.80-1.80 | 1.5-3.0% | 40-60% |
| Finance | $3.00-6.00 | $2.00-4.00 | 0.8-1.5% | 30-50% |
| Social | $2.00-4.00 | $1.20-2.50 | 1.0-2.0% | 35-55% |
| Utility | $1.80-3.50 | $1.00-2.00 | 0.9-1.8% | 45-65% |

### 16.4 Seasonal Adjustments

| Period | CPM Adjustment | Impact | Strategy |
|--------|----------------|--------|----------|
| Q4 Holiday | +50-100% | Higher competition | Increase budget 50% |
| Black Friday | +80-150% | Extreme competition | Allocate 3x budget |
| January | -20-30% | Lower demand | Scale back, test new |
| Summer | -10-20% | Varies by vertical | Audience testing |

---

## Phase 17: Automation Rules

### 17.1 Budget Automation

```bash
# Increase budget for winning ad sets
curl -X POST "https://graph.facebook.com/v21.0/{ADSET_ID}/adsetrules" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Scale Winner",
    "evaluation_spec": {
      "filter": {
        "field": "spend",
        "operator": "GREATER_THAN",
        "value": 100
      },
      "filters": [{
        "field": "cost_per_action",
        "operator": "LESS_THAN",
        "value": {"action_type": "purchase", "amount": 15}
      }]
    },
    "execution_spec": {
      "actions": [{
        "field": "daily_budget",
        "operator": "MULTIPLY",
        "value": 1.2
      }]
    },
    "status": "ENABLED",
    "access_token": "{ACCESS_TOKEN}"
  }'
```

### 17.2 Pause Automation

```bash
# Pause underperforming ads
curl -X POST "https://graph.facebook.com/v21.0/{CAMPAIGN_ID}/adrules" \
  -d '{
    "name": "Pause Losers",
    "evaluation_spec": {
      "filters": [{
        "field": "cost_per_action",
        "operator": "GREATER_THAN",
        "value": {"action_type": "purchase", "amount": 45}
      }, {
        "field": "spend",
        "operator": "GREATER_THAN",
        "value": 50
      }]
    },
    "execution_spec": {
      "actions": [{
        "field": "status",
        "operator": "SET",
        "value": "PAUSED"
      }]
    },
    "access_token": "{ACCESS_TOKEN}"
  }'
```

### 17.3 Automation Rules Table

| Trigger | Action | Frequency | Priority |
|---------|--------|-----------|----------|
| CPA > 1.5x target | Pause ad | Real-time | 🔴 High |
| CPCP > 20% | Alert + reduce budget | Daily | 🟡 Medium |
| Frequency > 4 | Alert + pause ad set | Daily | 🟡 Medium |
| CTR < 0.3% | Alert + pause ad | Weekly | 🟡 Medium |
| ROAS < 1x | Alert + reduce budget | Real-time | 🔴 High |
| CPA < Target | Increase budget +30% | Every 3 days | 🔴 High |
| Spend > budget + 20% | Pause campaign | Daily | 🔴 High |

---

## Phase 18: Attribution Models

### 18.1 Attribution Windows

| Window | Description | Use Case |
|--------|-------------|----------|
| 7-day click | Click within 7 days | Most campaigns |
| 1-day view | View within 1 day | Brand awareness impact |
| 7d click + 1d view | Combined | **Recommended default** |
| 28-day click | Click within 28 days | Long sales cycle (B2B) |
| 1-day click | Click within 1 day | Flash sales/urgency |

### 18.2 Setting Attribution

```bash
# E-commerce (recommended)
curl -X POST "https://graph.facebook.com/v21.0/{ADSET_ID}" \
  -d "attribution_spec=[{'event_type':'CONVERSIONS','window_days':7}]" \
  -d "access_token={ACCESS_TOKEN}"

# B2B/Services (long cycle)
curl -X POST "https://graph.facebook.com/v21.0/{ADSET_ID}" \
  -d "attribution_spec=[{'event_type':'CONVERSIONS','window_days':28}]" \
  -d "access_token={ACCESS_TOKEN}"

# Lead Generation
curl -X POST "https://graph.facebook.com/v21.0/{ADSET_ID}" \
  -d "attribution_spec=[{'event_type':'LEAD','window_days':7}]" \
  -d "access_token={ACCESS_TOKEN}"
```

### 18.3 Attribution Model Selection

| Business Type | Recommended Window | Reason |
|---------------|-------------------|--------|
| E-commerce | 7d click + 1d view | Short purchase cycle |
| Lead Gen | 7d click | Lead capture happens quickly |
| B2B Services | 28d click | Long consideration period |
| App Installs | 7d click | Install happens quickly |
| High-ticket | 28d click | Extended decision process |

---

## Phase 19: Machine Learning Phases

### 19.1 Learning Phase Triggers

```
Learning Phase Starts When:
├── New campaign created
├── New ad set created
├── Significant budget change (>20%)
├── Audience modification
├── Creative change
├── Bid strategy change
└── Placement change
```

### 19.2 Learning Phase Rules

```markdown
⚠️ DURING LEARNING PHASE (7 days or 50 conversions):

DO NOT:
├── ❌ Make changes to ad sets
├── ❌ Pause ads
├── ❌ Change targeting
├── ❌ Change budget (>20%)
├── ❌ Change bid strategy
└── ❌ Change optimization goal

DO:
├── ✅ Monitor performance daily
├── ✅ Wait for 50 conversions
├── ✅ Wait for 7 days minimum
└── ✅ Document baseline metrics
```

### 19.3 Learning Phase Exit

```markdown
SUCCESSFUL EXIT:
├── 50+ conversions in 7 days
├── CPA stabilizes
├── Ready for scaling
└── Action: Begin scaling playbook

FAILED EXIT:
├── < 50 conversions
├── CPA too high/unstable
└── Action: Optimize before scaling

TROUBLESHOOTING LEARNING ISSUES:

Problem: Learning Too Long (>7 days)
│
├── Budget too low?
│   └── Solution: Increase to $20+/day minimum
│
├── Audience too narrow?
│   └── Solution: Expand to 2M+ people
│
├── Event too rare?
│   └── Solution: Use broader event or optimize for clicks first
│
└── Creative not performing?
    └── Solution: Test new creatives
```

### 19.4 Post-Learning Optimization

| Days Post-Learning | Action | Reason |
|-------------------|--------|--------|
| Day 1-7 | Monitor only | Stabilization |
| Day 8-14 | Minor tweaks | Fine-tuning |
| Day 15+ | Scale winners | Growth phase |

---

## Phase 20: Conversions API Advanced

### 20.1 Enhanced Event Parameters

```json
{
  "event_name": "Purchase",
  "event_time": 1704067200,
  "event_id": "event.purchase.ORDER_12345",
  "user_data": {
    "em": ["7e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"],
    "ph": ["8e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"],
    "fn": ["5e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"],
    "ln": ["4e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"],
    "ct": ["3e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"],
    "st": ["2e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"],
    "zp": ["1e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"],
    "country": ["0e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"],
    "client_ip_address": "192.168.1.1",
    "client_user_agent": "Mozilla/5.0...",
    "fbc": "fb.1.1704067200.AbCdEf",
    "fbp": "fb.1.1704067200.123456789"
  },
  "custom_data": {
    "currency": "USD",
    "value": "100.00",
    "content_ids": ["product_1", "product_2"],
    "content_type": "product",
    "content_name": "Product Name",
    "num_items": 2,
    "order_id": "ORDER_12345",
    "predicted_ltv": "500.00"
  },
  "event_source_url": "https://example.com/checkout",
  "action_source": "website"
}
```

### 20.2 Server-Side Event Send

```bash
curl -X POST "https://graph.facebook.com/v21.0/{PIXEL_ID}/events" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [{
      "event_name": "Purchase",
      "event_time": 1704067200,
      "event_id": "event.purchase.ORDER_12345",
      "user_data": {
        "em": ["7e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"],
        "ph": ["8e07f40d8b9d4b6b9b4b3b2b1b0b0a0a"]
      },
      "custom_data": {
        "currency": "USD",
        "value": "100.00"
      }
    }],
    "access_token": "{ACCESS_TOKEN}"
  }'
```

### 20.3 Event Match Quality

| Parameter | Hash Method | Priority | Impact |
|-----------|-------------|----------|--------|
| Email (em) | SHA256 | 🔴 High | Highest match |
| Phone (ph) | SHA256 | 🔴 High | High match |
| External ID | Plain | 🔴 High | High match |
| First Name (fn) | SHA256 | 🟡 Medium | Medium match |
| Last Name (ln) | SHA256 | 🟡 Medium | Medium match |
| City (ct) | SHA256 | 🟢 Low | Low match |
| State (st) | SHA256 | 🟢 Low | Low match |
| Zip (zp) | SHA256 | 🟡 Medium | Medium match |
| Country | SHA256 | 🟢 Low | Low match |

**Target:** Event Match Quality Score > 6.0

### 20.4 Deduplication

```javascript
// Send event_id for deduplication
{
  "event_name": "Purchase",
  "event_id": "event.purchase.ORDER_12345",  // Unique ID for deduplication
  "event_time": 1704067200,
  // ... rest of parameters
}

// Meta will deduplicate events with same event_id across pixel and CAPI
```

---

## Phase 21: Dynamic Ads & Catalog

### 21.1 Create Product Catalog

```bash
# Create catalog
curl -X POST "https://graph.facebook.com/v21.0/{BUSINESS_ID}/product_catalogs" \
  -d "name={CATALOG_NAME}" \
  -d "vertical=ecommerce" \
  -d "access_token={ACCESS_TOKEN}"
```

### 21.2 Product Feed Format (CSV)

```csv
id,title,description,availability,condition,price,sale_price,link,image_link,brand,additional_image_link,google_product_category
SKU001,"Nike Air Max","Classic sneaker with Air technology","in stock","new","180.00 USD","150.00 USD","https://site.com/product1","https://site.com/img1.jpg","Nike","https://site.com/img2.jpg","Shoes > Athletic"
SKU002,"Nike Air Max 2","New release limited edition","in stock","new","200.00 USD","","https://site.com/product2","https://site.com/img3.jpg","Nike","","Shoes > Athletic"
```

### 21.3 Upload Product Feed

```bash
curl -X POST "https://graph.facebook.com/v21.0/{CATALOG_ID}/product_feeds" \
  -d "name=Product Feed" \
  -d "schedule={\"interval\":\"DAILY\",\"hour\":0}" \
  -d "access_token={ACCESS_TOKEN}"
```

### 21.4 Dynamic Ad Template

```json
{
  "name": "Dynamic Ad - {Product}",
  "object_story_spec": {
    "page_id": "{PAGE_ID}",
    "template_data": {
      "call_to_action": {"type": "SHOP_NOW"},
      "description": "{{product.description}}",
      "link": "{{product.link}}",
      "message": "Check out {{product.title}}! Now only {{product.price}}",
      "name": "{{product.name}}"
    }
  },
  "product_set_id": "{PRODUCT_SET_ID}"
}
```

### 21.5 Dynamic Ad Campaign Structure

```
Campaign: Dynamic Sales
├── Ad Set: DPA Broads
│   ├── Audience: Broad (no specific targeting)
│   ├── Product Set: All Products
│   └── Optimization: Purchase
│
├── Ad Set: DPA Cart Abandoners
│   ├── Audience: Added to Cart (last 30 days)
│   ├── Product Set: Viewed Products
│   └── Optimization: Purchase
│
└── Ad Set: DPA Past Purchasers
    ├── Audience: Purchased (last 180 days)
    ├── Product Set: Related Products
    └── Optimization: Purchase
```

### 21.6 Retargeting with Dynamic Ads

```bash
# Create audience of product viewers
curl -X POST "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}/customaudiences" \
  -d "name=Viewed Products -Last 30 Days" \
  -d "subtype=CUSTOM" \
  -d 'rule={"and":[{"eventName":"ViewContent"},{"content_type":"product"}]}' \
  -d "retention_days=30" \
  -d "access_token={ACCESS_TOKEN}"
```

---

## Phase 22: Seasonal Strategies

### 22.1 Black Friday/Cyber Monday

```markdown
### Black Friday Timeline (4-6 weeks before)

PHASE 1: AWARENESS (4-6 weeks before)
├── Objective: OUTCOME_AWARENESS
├── Budget: 20% of total
├── Creative: Teaser, countdown
├── Messaging: "Coming soon", "Get ready"
└── Audience: Broad + Lookalike

PHASE 2: CONSIDERATION (2-3 weeks before)
├── Objective: OUTCOME_TRAFFIC
├── Budget: 30% of total
├── Creative: Product highlights, benefits
├── Messaging: "Preview offers", "Wishlist now"
└── Audience: Warm + Interest

PHASE 3: CONVERSION (Black Friday week)
├── Objective: OUTCOME_SALES
├── Budget: 50% of total
├── Creative: Offers, urgency, countdown
├── Messaging: "Limited time", "X% off"
└── Audience: All warm audiences + Retargeting
```

### 22.2 Special Settings for Seasonal

```json
{
  "lifetime_budget": "{BUDGET_CENTS}",
  "pacing_type": "day_parting",
  "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
  "start_time": "{FRIDAY_00:00}",
  "end_time": "{CYBER_MONDAY_23:59}",
  "targeting": {
    "geo_locations": {"countries": ["US"]},
    "age_min": 18,
    "age_max": 65
  }
}
```

### 22.3 Product Launch Strategy

```markdown
### Product Launch Timeline (2-4 weeks before)

PHASE 1: TEASE (2-4 weeks before)
├── Build anticipation
├── Email capture
├── Waitlist creation
├── Landing page live
└── Pixel firing (Lead event)

PHASE 2: LAUNCH DAY
├── High budget allocation
├── Multiple creative formats
├── All placements active
├── Retargeting warm audiences
└── Optimized for Purchase

PHASE 3: SUSTAIN (Post-launch)
├── Social proof testimonials
├── User-generated content
├── Reviews integration
├── Cross-sell/upsell
└── Retargeting non-converters
```

---

## Phase 23: Reporting Templates

### 23.1 Weekly Report Template

```markdown
# Weekly Performance Report - {Client}
Period: {Start} to {End}

## Executive Summary
- **Total Spend:** ${Spend}
- **Conversions:** {Conversions}
- **CPA:** ${CPA} ({Change}% vs last week)
- **ROAS:** {ROAS}x ({Change}% vs last week)

## Key Metrics
| Metric | This Week | Last Week | Change | Target | Status |
|--------|-----------|-----------|--------|--------|--------|
| Spend | ${Spend} | ${PrevSpend} | {Change}% | ${Budget} | ✓/✗ |
| Impressions | {Imp} | {PrevImp} | {Change}% | - | - |
| CPM | ${CPM} | ${PrevCPM} | {Change}% | ${Target} | ✓/✗ |
| CPC | ${CPC} | ${PrevCPC} | {Change}% | ${Target} | ✓/✗ |
| CTR | {CTR}% | {PrevCTR}% | {Change}% | {Target}% | ✓/✗ |
| CPA | ${CPA} | ${PrevCPA} | {Change}% | ${Target} | ✓/✗ |
| ROAS | {ROAS}x | {PrevROAS}x | {Change}% | {Target}x | ✓/✗ |

## Top Performers
| Ad Set | Spend | CPA | ROAS | Status | Recommendation |
|--------|-------|-----|------|--------|----------------|
| {Name} | ${Spend} | ${CPA} | {ROAS}x | ✓ | Scale +20% |
| {Name} | ${Spend} | ${CPA} | {ROAS}x | ⚠️ | Monitor |
| {Name} | ${Spend} | ${CPA} | {ROAS}x | ✗ | Pause |

## Recommendations
1. {Recommendation_1}
2. {Recommendation_2}
3. {Recommendation_3}

## Next Week Priorities
- {Priority_1}
- {Priority_2}
- {Priority_3}
```

### 23.2 Monthly Report Template

```markdown
# Monthly Performance Report - {Client}
Period: {Month}

## Overview
- **Total Spend:** ${Spend}
- **Budget Utilization:** {Utilization}%
- **Total Conversions:** {Conversions}
- **Average CPA:** ${CPA}
- **Revenue:** ${Revenue}
- **ROAS:** {ROAS}x

## Trend Analysis
[Include charts: Spend, CPA, ROAS over time]

## Channel Mix
| Platform | Spend | % | CPA | ROAS | Quality |
|----------|-------|---|-----|------|---------|
| Facebook | ${Spend} | {%} | ${CPA} | {ROAS}x | ⭐⭐⭐⭐ |
| Instagram | ${Spend} | {%} | ${CPA} | {ROAS}x | ⭐⭐⭐ |
| Stories | ${Spend} | {%} | ${CPA} | {ROAS}x | ⭐⭐⭐⭐ |

## Audience Performance
| Audience Type | Spend | CPA | ROAS | Quality | Recommendation |
|---------------|-------|-----|------|---------|----------------|
| Lookalike 1% | ${Spend} | ${CPA} | {ROAS}x | ⭐⭐⭐⭐ | Scale |
| Interest | ${Spend} | ${CPA} | {ROAS}x | ⭐⭐⭐ | Test new |
| Custom | ${Spend} | ${CPA} | {ROAS}x | ⭐⭐⭐⭐⭐ | Optimize |

## Creative Performance
| Creative Type | CTR | CPA | ROAS | Recommendation |
|---------------|-----|-----|------|----------------|
| Video | {CTR}% | ${CPA} | {ROAS}x | Scale |
| Image | {CTR}% | ${CPA} | {ROAS}x | Test new |
| Carousel | {CTR}% | ${CPA} | {ROAS}x | Optimize |

## Attribution
- **7-day click:** {7d_click}%
- **1-day view:** {1d_view}%
- **7d click +1d view:** {combined}%

## Next Month Strategy
1. {Strategy_1}
2. {Strategy_2}
3. {Strategy_3}
```

---

## Phase 24: Multi-Account Management

### 24.1 Account Structure

```json
{
  "business_manager_id": "{BUSINESS_ID}",
  "owned_ad_accounts": {
    "data": [
      {"id": "act_123", "name": "Client A"},
      {"id": "act_456", "name": "Client B"},
      {"id": "act_789", "name": "Client C"}
    ]
  }
}
```

### 24.2 Bulk Operations

```bash
# Get all ad accounts
curl -X GET "https://graph.facebook.com/v21.0/{BUSINESS_ID}/owned_ad_accounts?fields=id,name,account_status,amount_spent&access_token={ACCESS_TOKEN}"

# Bulk insights across accounts
curl -X POST "https://graph.facebook.com/v21.0/" \
  -d "ids={ACT_1},{ACT_2},{ACT_3}" \
  -d "method=get" \
  -d "params={ids}&fields=spend,impressions,clicks,purchase_roas"
```

### 24.3 Agency Dashboard Template

```markdown
# Agency Dashboard

| Client | Spend | CPA | ROAS | Status | Priority Action |
|--------|-------|-----|------|--------|-----------------|
| Client A | $5,000 | $25 | 3.5x | ✅ On track | Scale +30% |
| Client B | $3,000 | $45 | 2.1x | ⚠️ Under | Optimize creative |
| Client C | $2,000 | $15 | 5.2x | ✅ Exceed | Scale +50% |
| Client D | $4,000 | $35 | 2.8x | ⚠️ Under | Pause losers |

### Daily Checklist
- [ ] Check all accounts forcritical errors
- [ ] Review CPA against targets
- [ ] Check budget pacing
- [ ] Review creative performance

### Weekly Actions
- [ ] Cross-account performance report
- [ ] Budget reallocation recommendations
- [ ] Creative refresh schedule
- [ ] Audience expansion reviews
```

---

## Phase 25: Creative Testing Framework

### 25.1 Test Matrix

| Test | Elements | Sample Size | Duration | Priority |
|------|----------|-------------|----------|----------|
| Hook Test | First 3 seconds | 100k impressions | 7 days | 🔴 High |
| Format Test | Video vs Image vs Carousel | 50k per format | 7 days | 🔴 High |
| CTA Test | Different CTAs | 50k per CTA | 7 days | 🟡 Medium |
| Copy Test | Primary text variations | 30k per variation | 5 days | 🟡 Medium |
| Audience Test | Interest vs Lookalike | 100k per audience | 7 days | 🔴 High |
| Placement Test | Feed vs Stories | 100k per placement | 7 days | 🟡 Medium |

### 25.2 Creative Performance Analysis

```markdown
=== CREATIVE PERFORMANCE MATRIX ===

| Creative | Spend | Impressions | CTR | Hook Rate* | CPA | ROAS | Verdict |
|----------|-------|-------------|-----|------------|-----|------|---------|
| Hook A | $100 | 10k | 1.5% | 75% | $15 | 3.5x | ⭐ Winner |
| Hook B | $100 | 10k | 1.0% | 60% | $22 | 2.1x | ✗ Loser |
| Hook C | $100 | 10k | 1.2% | 65% | $18 | 2.8x | ⚠️ Test more |

*Hook Rate = % of viewers who watched first 3 seconds

CREATIVE INSIGHTS:
├── Hook A: Strong opening, clear value prop
├── Hook B: Weak hook, too much text
└── Hook C: Good but needs optimization
```

### 25.3 Creative Testing Cycle

```markdown
Creative Testing Cycle (2-weeks):

WEEK 1: Hook Test
├── Day 1-7: Run 5 hook variations
├── Day 8: Analyze results
├── Day 8: Select top 2 hooks
└── Day 9-14: Continue with winners

WEEK 2: Format Test
├── Day 1-7: Test Video vs Image vs Carousel
├── Day 8: Analyze results
├── Day 8: Select winning format
└── Day 9-14: Roll out to all audiences

ONGOING: Copy Test
├── Run A/B tests on primary text
├── Rotate winners every 2 weeks
└── Always have 10%budget on testing
```

---

## Integration Summary

When user says "create campaign" or mentions a client/campaign:

1. **Check for existing folder structure**
2. **Read briefing.md automatically**
3. **List and analyze all creatives**
4. **Generate ad copy based on briefing + creative analysis**
5. **Ask for missing API credentials**
6. **Upload creatives to Meta**
7. **Create full campaign structure**
8. **Create resultados.md after launch**

## Quick Reference Commands

### Diagnose Issues

```bash
# Check account status
curl -X GET "https://graph.facebook.com/v21.0/act_{AD_ACCOUNT_ID}?fields=account_status,amount_spent,balance&access_token={ACCESS_TOKEN}"

# Get campaign insights
curl -X GET "https://graph.facebook.com/v21.0/{CAMPAIGN_ID}/insights?fields=spend,impressions,clicks,ctr,cpc,cpm,reach,frequency,actions,cost_per_action,purchase_roas&date_preset=last_7d&access_token={ACCESS_TOKEN}"

# Get ad breakdown
curl -X GET "https://graph.facebook.com/v21.0/{AD_ID}/insights?fields=spend,impressions,clicks,ctr,cpc,actions&breakdowns=country,age,gender&access_token={ACCESS_TOKEN}"
```

### Quick Actions

| Task | Command |
|------|---------|
| Pause campaign | `curl -X POST ".../{CAMPAIGN_ID}?status=PAUSED"` |
| Resume campaign | `curl -X POST ".../{CAMPAIGN_ID}?status=ACTIVE"` |
| Get performance | `curl -X GET ".../{ID}/insights?fields=..."` |
| List ads | `curl -X GET ".../{ADSET_ID}/ads?fields=..."` |
