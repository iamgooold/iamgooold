import requests
import re
import os
from datetime import datetime

LEETCODE_USERNAME = "auamores"
README_PATH = "README.md"

START_MARKER = "<!-- LEETCODE:START -->"
END_MARKER = "<!-- LEETCODE:END -->"

def fetch_stats():
    url = f"https://alfa-leetcode-api.onrender.com/{LEETCODE_USERNAME}/solved"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()

def fetch_contest():
    url = f"https://alfa-leetcode-api.onrender.com/{LEETCODE_USERNAME}/contest"
    r = requests.get(url, timeout=15)
    r.raise_for_status()
    return r.json()

def build_section(stats, contest):
    easy = stats.get("easySolved", 0)
    easy_total = stats.get("totalEasy", 0)
    medium = stats.get("mediumSolved", 0)
    medium_total = stats.get("totalMedium", 0)
    hard = stats.get("hardSolved", 0)
    hard_total = stats.get("totalHard", 0)
    total = stats.get("solvedProblem", 0)
    total_all = stats.get("totalProblem", 0)

    rating = contest.get("contestRating", "N/A")
    if isinstance(rating, float):
        rating = round(rating, 2)
    rank = contest.get("contestGlobalRanking", "N/A")

    updated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    section = f"""<!-- LEETCODE:START -->
### 🧩 LeetCode Stats
| Difficulty | Solved | Total |
|:----------:|:------:|:-----:|
| 🟢 Easy    | {easy} | {easy_total} |
| 🟡 Medium  | {medium} | {medium_total} |
| 🔴 Hard    | {hard} | {hard_total} |
| **Total**  | **{total}** | **{total_all}** |

> 🏆 Contest Rating: `{rating}` · Global Rank: `#{rank}`
>
> 🔄 *Auto-updated: {updated}*
<!-- LEETCODE:END -->"""
    return section

def update_readme(section):
    if not os.path.exists(README_PATH):
        print(f"README not found at {README_PATH}")
        return False

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    if START_MARKER not in content or END_MARKER not in content:
        print("Markers not found in README.")
        return False

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL
    )
    new_content = pattern.sub(section, content)

    if new_content == content:
        print("No changes detected.")
        return False

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print("README updated.")
    return True

if __name__ == "__main__":
    print("Fetching LeetCode stats...")
    stats = fetch_stats()
    contest = fetch_contest()
    section = build_section(stats, contest)
    update_readme(section)
    print("Done.")
