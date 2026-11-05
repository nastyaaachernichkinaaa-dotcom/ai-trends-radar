import requests
import feedparser

ARXIV_API_URL = "http://export.arxiv.org/api/query"
CATEGORIES = ["cs.AI", "cs.LG", "cs.CL"]

def fetch_papers(max_results=50):
    search_query = " OR ".join(f"cat:{c}" for c in CATEGORIES)
    params = {
        "search_query": search_query,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
        "max_results": max_results,
    }

    response = requests.get(ARXIV_API_URL, params=params, timeout=30)
    response.raise_for_status()

    feed = feedparser.parse(response.text)

    papers = []
    for entry in feed.entries:
        paper = {
            "arxiv_id": entry.id.split("/abs/")[-1],
            "title": " ".join(entry.title.split()),
            "summary": " ".join(entry.summary.split()),
            "authors": [author.name for author in entry.authors],
            "categories": [tag.term for tag in entry.tags],
            "published": entry.published,
            "url": entry.link,
        }
        papers.append(paper)
    return papers

if __name__ == "__main__":
    papers = fetch_papers(max_results=5)
    print(f"Получено статей: {len(papers)}")
    for p in papers:
        print("-" * 80)
        print(p["published"], p["arxiv_id"])
        print(p["title"])
        print(",".join(p["authors"][:3]))