from duckduckgo_search import DDGS
import json

try:
    with DDGS() as ddgs:
        results = [r for r in ddgs.text("AI engineers job market 2026", max_results=5)]
        print(f"Results found: {len(results)}")
        for r in results:
            print(f"- {r['title']} ({r['href']})")
except Exception as e:
    print(f"Error during search: {e}")
