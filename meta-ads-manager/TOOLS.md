# Meta Ads Manager - Tools & Commands

## Quick Reference

### File Locations

| What | Where |
|------|-------|
| Saved Accounts | `~/.meta-ads-manager/accounts.json` |
| Session Data | `~/.meta-ads-manager/session.json` |
| Campaign Folders | `/campanhas/{cliente}/{mes}/{campanha}/` |
| Briefing File | `/campanhas/{cliente}/{mes}/{campanha}/briefing.md` |
| Creatives | `/campanhas/{cliente}/{mes}/{campanha}/ad_XX_XX.XXX` |
| Results | `/campanhas/{cliente}/{mes}/{campanha}/resultados.md` |

---

## First Time Setup

### 1. Initialize Memory Storage

```bash
# Create memory directories
mkdir -p ~/.meta-ads-manager/cache/insights
mkdir -p ~/.meta-ads-manager/cache/campaigns
mkdir -p ~/.meta-ads-manager/logs

# Initialize accounts file
echo '{"version":"1.0","accounts":{},"active_account":null}' > ~/.meta-ads-manager/accounts.json

# Initialize session file
echo '{"current_account":null,"current_campaign":null,"temp_data":{}}' > ~/.meta-ads-manager/session.json
```

### 2. Setup Your Account

```
Run: /meta-ads setup
```

You will need:
- Access Token (from https://developers.facebook.com/tools/explorer/)
- Ad Account ID (from https://business.facebook.com/settings/ad-accounts)
- Pixel ID (optional)
- Page ID (optional)

---

## Campaign Folder Setup

### Create Folder Structure

```bash
# Syntax
mkdir -p /campanhas/{cliente}/{YYYY-MM}/{campanha}/

# Examples
mkdir -p /campanhas/nike/2024-03/black_friday/
mkdir -p /campanhas/fitness_app/2024-03/launch/
mkdir -p /campanhas/local_bakery/2024-03/easter_promo/
```

### Folder Structure

```
/campanhas/
├── {cliente}/                      # Client name (lowercase, underscores)
│   └── {YYYY-MM}/                   # Year-Month
│       └── {campanha}/              # Campaign name (lowercase, underscores)
│           ├── briefing.md          # REQUIRED: Campaign brief
│           ├── analise.md           # OPTIONAL: Manager notes
│           ├── ad_01_feed_image.jpg # Creative 1 - Feed image
│           ├── ad_01_feed_video.mp4 # Creative 1 - Feed video
│           ├── ad_02_story_video.mp4 # Creative 2 - Stories
│           ├── ad_03_carousel_01.jpg # Creative 3 - Carousel card 1
│           ├── ad_03_carousel_02.jpg # Creative 3 - Carousel card 2
│           └── resultados.md        # CREATED: Results after launch
```

### Creative Naming Convention

```
Format: ad_{number}_{placement}_{type}.{extension}

Examples:
ad_01_feed_image.jpg      # Creative 1, Feed, Image
ad_01_feed_video.mp4      # Creative 1, Feed, Video
ad_02_story_video.mp4     # Creative 2, Stories, Video
ad_02_reels_video.mp4     # Creative 2, Reels, Video
ad_03_carousel_01.jpg     # Creative 3, Carousel card 1
ad_03_carousel_02.jpg     # Creative 3, Carousel card 2
```

**Placements:**
- `feed` - Facebook/Instagram Feed
- `story` - Instagram/Facebook Stories
- `reels` - Instagram/Facebook Reels
- `carousel` - Carousel (multiple images)

**Types:**
- `image` - Static image (.jpg, .png)
- `video` - Video file (.mp4, .mov)

---

## Briefing Template

### Create briefing.md

```bash
# Create briefing file
nano /campanhas/nike/2024-03/black_friday/briefing.md

# Or use any text editor
code /campanhas/nike/2024-03/black_friday/briefing.md
```

### Template Content

```markdown
# Campaign Briefing: {Campaign_Name}

## Client Information
- **Client:** {Client_Name}
- **Product/Service:** {What you're promoting}
- **Industry:** {Industry}
- **Brand Voice:** {Tone}

## Campaign Objectives
- **Primary Goal:** [Sales/Leads/Traffic/Awareness/App Installs]
- **Target CPA:** $XX.XX
- **Target ROAS:** X.Xx
- **Budget:** $X,XXX/month

## Target Audience
- **Age Range:** XX to XX
- **Gender:** [All/Male/Female]
- **Location:** [Countries, Cities]
- **Interests:** [Interest 1, Interest 2, ...]
- **Behaviors:** [Behavior 1, Behavior 2, ...]

## Unique Selling Propositions
1. {USP 1}
2. {USP 2}
3. {USP 3}

## Key Messages
- **Primary:** {Main message}
- **Secondary:** {Supporting points}

## Creative Direction
- **Visual Style:** {Modern/Classic/Minimal}
- **Colors:** {Brand colors}
- **Imagery:** {Types of images}

## Landing Page
- **URL:** {Landing page URL}
- **CTA:** {Call to action}

## Timeline
- **Start:** {YYYY-MM-DD}
- **End:** {YYYY-MM-DD}
```

---

## Commands

### Account Management

| Command | Description |
|---------|-------------|
| `/meta-ads setup` | Initialize skill, save account credentials |
| `/meta-ads accounts list` | List all saved accounts |
| `/meta-ads accounts add {name}` | Add new account |
| `/meta-ads accounts use {name}` | Set active account |
| `/meta-ads accounts remove {name}` | Remove account |
| `/meta-ads accounts export` | Export settings for backup |
| `/meta-ads accounts import` | Import settings from backup |

### Campaign Management

| Command | Description |
|---------|-------------|
| `/meta-ads campaign create` | Create new campaign with folder read |
| `/meta-ads analyze {period}` | Analyze performance |
| `/meta-ads diagnose` | Run diagnostics on active campaigns |
| `/meta-ads scale {id}` | Scale campaign safely |
| `/meta-ads pause {id}` | Pause campaign |
| `/meta-ads resume {id}` | Resume campaign |
| `/meta-ads status` | Show current status |

### Folder Commands

| Command | Description |
|---------|-------------|
| `/meta-ads clients` | List all clients |
| `/meta-ads campaigns {client}` | List campaigns for client |
| `/meta-ads folder create {client} {name}` | Create campaign folder |
| `/meta-ads briefing {client} {campaign}` | Read briefing |

### Analysis Periods

| Period | Description |
|--------|-------------|
| `today` | Today's data |
| `yesterday` | Yesterday's data |
| `last7d` | Last 7 days |
| `last14d` | Last 14 days |
| `last30d` | Last 30 days |
| `last90d` | Last 90 days |
| `this_month` | Current month |
| `last_month` | Previous month |

---

## Example Workflow

### Step 1: Setup (First Time)

```bash
# Initialize storage
mkdir -p ~/.meta-ads-manager/cache/insights
mkdir -p ~/.meta-ads-manager/cache/campaigns
echo '{"version":"1.0","accounts":{}}' > ~/.meta-ads-manager/accounts.json
```

### Step 2: Create Campaign Folder

```bash
mkdir -p /campanhas/nike/2024-03/black_friday/
```

### Step 3: Add Briefing

```bash
# Create and edit briefing.md
nano /campanhas/nike/2024-03/black_friday/briefing.md

# Paste briefing template and fill in details
```

### Step 4: Add Creatives

```bash
# Copy your creatives
cp ~/Downloads/nike_ad1.jpg /campanhas/nike/2024-03/black_friday/ad_01_feed_image.jpg
cp ~/Downloads/nike_video.mp4 /campanhas/nike/2024-03/black_friday/ad_01_feed_video.mp4
cp ~/Downloads/nike_story.mp4 /campanhas/nike/2024-03/black_friday/ad_02_story_video.mp4
```

### Step 5: Run Skill

```
User: "crie uma campanha para o Nike Black Friday"

Skill will:
1. Check saved accounts
2. Find /campanhas/nike/2024-03/black_friday/
3. Read briefing.md
4. List creatives (ad_01_*, ad_02_*)
5. Analyze creatives + briefing
6. Generate ad copy
7. Ask for approval
8. Create campaign in Meta
```

---

## Storage Files

### accounts.json

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

### session.json

```json
{
  "current_account": "nike",
  "current_campaign": null,
  "last_action": "campaign_create",
  "last_action_time": "2024-03-29T16:00:00Z",
  "temp_data": {
    "briefing_content": null,
    "creatives_analyzed": [],
    "generated_copy": null
  }
}
```

---

## Troubleshooting

### Account Not Found

```bash
# Check if accounts file exists
ls -la ~/.meta-ads-manager/accounts.json

# If missing, initialize
echo '{"version":"1.0","accounts":{},"active_account":null}' > ~/.meta-ads-manager/accounts.json
```

### Campaign Folder Not Found

```bash
# List available clients
ls -la /campanhas/

# List campaigns for client
ls -la /campanhas/nike/

# Create missing folder
mkdir -p /campanhas/nike/2024-03/black_friday/
```

### Briefing Not Found

```bash
# Create briefing.md
touch /campanhas/nike/2024-03/black_friday/briefing.md

# Edit with template
nano /campanhas/nike/2024-03/black_friday/briefing.md
```

### No Creatives Found

```bash
# List creatives
ls -la /campanhas/nike/2024-03/black_friday/ad_*

# Add creatives with correct naming
cp ~/Downloads/creative.jpg /campanhas/nike/2024-03/black_friday/ad_01_feed_image.jpg
```