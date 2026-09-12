#!/usr/bin/env python3
"""Refresh the Projects section of the profile README.

Uses the GitHub REST API and GITHUB_TOKEN supplied by GitHub Actions.
"""

import json
import os
import urllib.request
from datetime import datetime, timezone

USER = "subahanpathan"
README = "README.md"
START = "<!-- PROJECTS_START -->"
END = "<!-- PROJECTS_END -->"

def github(url):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {os.environ.get('GH_TOKEN', '')}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "profile-maintainer",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)

repos = github(
    f"https://api.github.com/users/{USER}/repos?per_page=100&sort=updated&direction=desc"
)

# Keep the profile repository out of the project showcase.
repos = [
    r for r in repos
    if not r.get("fork")
    and r.get("name", "").lower() != USER.lower()
    and not r.get("archived")
]

# Prefer repositories with a description, stars, or recent activity.
repos.sort(
    key=lambda r: (
        bool(r.get("description")),
        r.get("stargazers_count", 0),
        r.get("forks_count", 0),
        r.get("updated_at", ""),
    ),
    reverse=True,
)

featured = repos[:6]

if featured:
    cards = []
    for r in featured:
        name = r["name"]
        desc = (r.get("description") or "Open-source engineering project.").strip()
        desc = desc.replace("\n", " ")
        if len(desc) > 150:
            desc = desc[:147] + "..."
        language = r.get("language") or "Code"
        stars = r.get("stargazers_count", 0)
        cards.append(
            f'### [{name}](https://github.com/{USER}/{name})\n'
            f'{desc}\n\n'
            f'`{language}` · ⭐ {stars}'
        )
    generated = "\n\n".join(cards)
else:
    generated = "_Public projects will appear here automatically as repositories are created._"

with open(README, "r", encoding="utf-8") as f:
    content = f.read()

start = content.index(START) + len(START)
end = content.index(END)

new_content = content[:start] + "\n" + generated + "\n" + content[end:]

with open(README, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"Updated {len(featured)} project entries at {datetime.now(timezone.utc).isoformat()}")
