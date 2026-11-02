import os
import json
import datetime
import urllib.request

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

def format_markdown_to_html(md_text):
    html = md_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    lines = html.split('\n')
    formatted = []
    for line in lines:
        if line.startswith("### "):
            formatted.append(f'<h3 style="color:#0f766e; border-bottom: 2px solid #e2e8f0; padding-bottom: 4px; margin-top: 18px;">{line[4:]}</h3>')
        elif line.startswith("## "):
            formatted.append(f'<h2 style="color:#0f172a; margin-top: 20px;">{line[3:]}</h2>')
        elif line.startswith("- "):
            formatted.append(f'<li style="margin-bottom: 4px;">{line[2:]}</li>')
        else:
            formatted.append(f'<p style="margin: 6px 0;">{line}</p>')
    
    body = "".join(formatted)
    body = body.replace("**", "<strong>").replace("**", "建筑")
    return body

def main():
    gemini_key = os.environ.get("GEMINI_API_KEY")
    resend_key = os.environ.get("RESEND_API_KEY")
    target_email = os.environ.get("NOTIFICATION_EMAIL")

    if not all([gemini_key, resend_key, target_email]):
        print("ERROR: Missing required environment variables.")
        return

    day_of_year = datetime.datetime.now().timetuple().tm_yday
    topic_obj = SCM_TOPIC_CURRICULUM[(day_of_year - 1) % len(SCM_TOPIC_CURRICULUM)]

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

    gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={gemini_key}"
    payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
    req = urllib.request.Request(gemini_url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req) as response:
            res_json = json.loads(response.read().decode("utf-8"))
            markdown_content = res_json["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return

    content_html = format_markdown_to_html(markdown_content)

    full_email_html = f"""
    <div style="font-family: Arial, sans-serif; color: #1e293b; max-width: 650px; margin: 0 auto; padding: 20px; border: 1px solid #cbd5e1; border-radius: 8px;">
      <div style="background-color: #0f172a; color: #ffffff; padding: 14px 18px; border-radius: 6px; margin-bottom: 16px;">
        <span style="font-size: 11px; font-weight: bold; color: #38bdf8; text-transform: uppercase;">ASD-STE100 Technical Daily Concept</span>
        <h2 style="margin: 4px 0 0 0; font-size: 22px;">{topic_obj['topic']}</h2>
        <p style="margin: 4px 0 0 0; font-size: 12px; color: #94a3b8;">Source Resource: {topic_obj['source']}</p>
      </div>
      <div>{content_html}</div>
      <hr style="border: 0; border-top: 1px solid #e2e8f0; margin-top: 24px;" />
      <p style="font-size: 11px; color: #64748b; text-align: center;">Automated Daily Task via GitHub Actions & Gemini API.</p>
    </div>
    """

    resend_url = "https://api.resend.com/emails"
    email_payload = json.dumps({
        "from": "Daily SCM Concept <onboarding@resend.dev>",
        "to": [target_email],
        "subject": f"[Daily SCM] Concept: {topic_obj['topic']} (ASD-STE100)",
        "html": full_email_html
    }).encode("utf-8")

    email_req = urllib.request.Request(
        resend_url,
        data=email_payload,
        headers={
            "Authorization": f"Bearer {resend_key}",
            "Content-Type": "application/json"
        }
    )

    try:
        with urllib.request.urlopen(email_req) as resend_resp:
            print("Email delivered successfully:", resend_resp.read().decode("utf-8"))
    except Exception as e:
        print(f"Resend Email Error: {e}")

if __name__ == "__main__":
    main()
