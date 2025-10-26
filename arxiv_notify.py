import feedparser, requests, json, os, datetime
from urllib.parse import quote_plus

QUERY_FILE = "queries.json"
LOG_FILE = "notified_ids.json"

# --- Load previously notified arXiv IDs ---
if os.path.exists(LOG_FILE):
    with open(LOG_FILE) as f:
        notified_ids = set(json.load(f))
else:
    notified_ids = set()

# --- Load query list ---
with open(QUERY_FILE) as f:
    queries = json.load(f)

new_ids = set()
max_results = 10

for item in queries:
    query = item["query"]
    webhook = item["webhook"]

    webhook = os.getenv(webhook)
    encoded_query = quote_plus(query, safe="'")
    if not webhook:
        print(f"⚠️ Webhook '{webhook}' not found in environment variables. Skipping.")
        continue
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{encoded_query}&start=0&max_results={max_results}"
        "&sortBy=submittedDate&sortOrder=descending"
    )
    feed = feedparser.parse(url)

    text = f"**arXiv Daily Update — {query} ({datetime.date.today()})**\n"
    new_papers = []

    for entry in feed.entries:
        paper_id = entry.id.split("/")[-1]  # e.g., 2501.01234v1
        if paper_id in notified_ids:
            continue  # Skip duplicates

        title = entry.title.strip()
        authors = ", ".join(a.name for a in entry.authors)
        summary = entry.summary.strip().replace("\n", " ")
        link = entry.link
        if hasattr(entry, "tags"):
            categories = [t["term"] for t in entry.tags]
            categories_str = ", ".join(categories)
        else:
            categories_str = "N/A"

        new_papers.append(paper_id)
        text += f"\n**{title}**\n_{authors}_\n{categories_str}_\n{summary}...\n{link}\n"
        requests.post(webhook, json={"content": text})
        text = ""  # Clear text after first post to avoid duplicates

    if new_papers:
        # requests.post(webhook, json={"content": text})
        print(f"✅ Sent {len(new_papers)} new papers for query: {query}")
        new_ids.update(new_papers)
    else:
        # 通知（新規論文なし）
        no_update_msg = f"📭 **arXiv Daily Update — {query} ({datetime.date.today()})**\n 新着論文はなかったよ."
        requests.post(webhook, json={"content": no_update_msg})
        print(f"ℹ️ No new papers for query: {query} — sent 'no update' notice")

# --- Save updated ID list ---
if new_ids:
    notified_ids.update(new_ids)
    with open(LOG_FILE, "w") as f:
        json.dump(list(notified_ids), f, indent=2)
