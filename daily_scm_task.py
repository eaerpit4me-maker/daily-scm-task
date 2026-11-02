import os
import json
import datetime
import urllib.request
import urllib.error

SCM_TOPIC_CURRICULUM = [
    {"topic": "The Bullwhip Effect", "source": "MITx MicroMasters & ASCM Dictionary"},
    {"topic": "SCOR Model Architecture", "source": "ASCM / APICS Framework"},
    {"topic": "Economic Order Quantity (EOQ)", "source": "MITx SC0x Supply Chain Analytics"},
    {"topic": "Safety Stock & Reorder Point", "source": "ASCM Lexicon & SCMDOJO"},
    {"topic": "Demand Forecast Error (MAD vs MAPE)", "source": "MITx SC1x Supply Chain Fundamentals"},
    {"topic": "ABC Inventory Analysis (Pareto Rule)", "source": "CIPS Knowledge Hub"},
    {"topic": "Days of Inventory On Hand (DOH)", "source": "Supply Chain Brain Metrics"},
    {"topic": "Cycle Stock vs Buffer Stock", "source": "ASCM Technical Definitions"},
    {"topic": "Vendor-Managed Inventory (VMI)", "source": "CIPS Procurement Frameworks"},
    {"topic": "Consignment Inventory Rules", "source": "CSCMP Logistics Standards"},
    {"topic": "Kraljic Matrix Sourcing Strategy", "source": "CIPS Strategic Sourcing Hub"},
    {"topic": "Total Cost of Ownership (TCO)", "source": "CIPS & Supply Chain Dive"},
    {"topic": "Procure-to-Pay (P2P) Cycle", "source": "ASCM Procurement Certificate"},
    {"topic": "Supplier Relationship Management (SRM)", "source": "CIPS Practice Guides"},
    {"topic": "Material Requirements Planning (MRP)", "source": "MITx SC2x Design & Dynamics"},
    {"topic": "Just-In-Time (JIT) & Kanban Pull", "source": "Toyota Production System / ASCM"},
    {"topic": "Sales and Operations Planning (S&OP)", "source": "Oliver Wight / ASCM Standards"},
    {"topic": "Capacity Requirements Planning (CRP)", "source": "MITx SC2x Supply Chain Engineering"},
    {"topic": "Cross-Docking Logistics", "source": "FreightWaves Operational Guides"},
    {"topic": "Milk Run Routing Optimization", "source": "MITx SC3x Logistics Systems"},
    {"topic": "3PL vs 4PL Logistics Orchestration", "source": "CSCMP Supply Chain Quarterly"},
    {"topic": "Volumetric Weight & Freight Class", "source": "FreightWaves Market Intelligence"},
    {"topic": "Incoterms 2020 (FOB vs CIF vs DDP)", "source": "ICC & CIPS Global Trade"},
    {"topic": "Customs Tariff & HS Code Classification", "source": "WCO & Supply Chain Dive"},
    {"topic": "On-Time In-Full (OTIF) Delivery", "source": "Supply Chain Brain Benchmarks"},
    {"topic": "Cash-to-Cash Cycle Time", "source": "MITx Financial Analytics"},
    {"topic": "Electronic Data Interchange (EDI 850/856)", "source": "GS1 Standards Hub"},
    {"topic": "Supply Chain Control Towers", "source": "Supply Chain Dive Tech Reports"},
    {"topic": "Nearshoring & Dual-Sourcing Risk", "source": "FreightWaves Economic Analysis"},
    {"topic": "Reverse Logistics & Circular Flows", "source": "ASCM Sustainability Standards"}
]

def create_github_issue(title, body):
    """Creates a new Issue in the GitHub Repository (No email required)"""
    repo = os.environ.get("GITHUB_REPOSITORY")
    token = os.environ.get("GITHUB_TOKEN")
    
    if not repo or not token:
        print("ERROR: GITHUB_REPOSITORY or GITHUB_TOKEN environment variable not set.")
        return False
        
    url = f"https://api.github.com/repos/{repo}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json",
        "User-Agent": "DailySCMTaskScript/1.0"
    }
    data = json.dumps({"title": title, "body": body}).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"GitHub Issue created successfully! HTTP {resp.status}")
            return True
    except urllib.error.HTTPError as e:
        print(f"Failed to create GitHub Issue: HTTP {e.code} - {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"Failed to create GitHub Issue: {e}")
        return False

def send_telegram_message(title, content):
    """Optional: Sends message to Telegram Chat if bot token provided"""
    bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not bot_token or not chat_id:
        return
        
    text = f"📘 *{title}*\n\n{content[:3800]}"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as resp:
            print("Telegram message sent successfully!")
    except Exception as e:
        print(f"Telegram error: {e}")

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("ERROR: GEMINI_API_KEY is missing from environment variables.")
        return

    day_of_year = datetime.datetime.now().timetuple().tm_yday
    topic_obj = SCM_TOPIC_CURRICULUM[(day_of_year - 1) % len(SCM_TOPIC_CURRICULUM)]
    print(f"Generating content for topic: {topic_obj['topic']}...")

    prompt = f"""
Act as a Senior Supply Chain Technical Specialist.
Topic: "{topic_obj['topic']}"
Reference Resource: "{topic_obj['source']}"

Explain this topic strictly following ASD-STE100 (Simplified Technical English) rules:
1. Maximum 20 words per sentence.
2. Use active voice and simple verbs.
3. Write one action or concept per sentence.

You MUST structure your response into these 5 exact sections:

### /infographics
- Purpose: [Clear single sentence objective]
- Main Formula or Metric: [Formula or core calculation]
- Key Variable 1: [Short definition]
- Key Variable 2: [Short definition]

### /blueprint
1. [Step 1 imperative instruction]
2. [Step 2 imperative instruction]
3. [Step 3 imperative instruction]
4. [Step 4 imperative instruction]

### /decision-matrix
Create a clean markdown table comparing options across Order Size, Frequency, Holding Cost, and Operational Risk.

### /layers
- Layer 1 (Mathematical): [Description]
- Layer 2 (Operational): [Description]
- Layer 3 (Financial): [Description]
- Layer 4 (Strategic): [Description]

### /diagram
1. [Input Event] -> 2. [Process Action] -> 3. [Output Result]
"""

    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}"
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(gemini_url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            markdown_content = res_json["candidates"][0]["content"]["parts"][0]["text"]
            print("Successfully received content from Gemini API.")
    except urllib.error.HTTPError as e:
        print(f"Gemini API HTTP Error {e.code}: {e.read().decode('utf-8')}")
        return
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return

    issue_title = f"[Daily SCM Concept] {topic_obj['topic']}"
    issue_body = f"**Source Reference:** {topic_obj['source']}\n\n" + markdown_content

    # Deliver via GitHub Issue (Default)
    create_github_issue(issue_title, issue_body)

    # Deliver via Telegram (Optional if credentials provided)
    send_telegram_message(issue_title, markdown_content)

if __name__ == "__main__":
    main()
