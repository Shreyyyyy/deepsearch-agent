from duckduckgo_search import DDGS

ddgs = DDGS()
print("Starting search news...")
try:
    results = list(ddgs.news("AI engineers job market", max_results=5))
    print(f"Results: {len(results)}")
    for r in results:
        print(f"TITLE: {r.get('title')}")
except Exception as e:
    print(f"Error: {e}")
