from duckduckgo_search import DDGS
import json
import time

ddgs = DDGS()
print("Starting search...")
try:
    results = list(ddgs.text("AI engineers jobs 2026", max_results=5))
    print(f"Results: {len(results)}")
    for r in results:
        print(f"TITLE: {r.get('title')}")
except Exception as e:
    print(f"Error: {e}")
