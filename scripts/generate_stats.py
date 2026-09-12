import json
import os
import urllib.request
from pathlib import Path
from html import escape

USER = "subahanpathan"
TOKEN = os.environ["GH_TOKEN"]


def get(url):
    request = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "subahanpathan-profile",
        },
    )

    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


# Get GitHub profile
user = get(f"https://api.github.com/users/{USER}")


# Get repositories
repositories = []

for page in range(1, 5):
    batch = get(
        f"https://api.github.com/users/{USER}/repos"
        f"?per_page=100&page={page}"
    )

    repositories.extend(batch)

    if len(batch) < 100:
        break


# Count repositories
public_repositories = len(
    [repo for repo in repositories if not repo.get("fork")]
)


# Count stars and forks
total_stars = sum(
    repo.get("stargazers_count", 0)
    for repo in repositories
)

total_forks = sum(
    repo.get("forks_count", 0)
    for repo in repositories
)


# Calculate languages
languages = {}

for repository in repositories:

    try:
        repo_languages = get(repository["languages_url"])

        for language, amount in repo_languages.items():
            languages[language] = (
                languages.get(language, 0) + amount
            )

    except Exception:
        continue


top_languages = sorted(
    languages.items(),
    key=lambda item: item[1],
    reverse=True
)[:6]


total_language_bytes = sum(languages.values()) or 1


def create_svg(title, rows, width=700):

    height = max(
        245,
        82 + (len(rows) * 34)
    )

    background = "#0d1117"
    text = "#f0f6fc"
    muted = "#8b949e"
    border = "#30363d"

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}">',

        f'<rect width="100%" height="100%" '
        f'rx="14" fill="{background}"/>',

        f'<text x="28" y="42" '
        f'font-family="Arial, sans-serif" '
        f'font-size="22" font-weight="700" '
        f'fill="{text}">{escape(title)}</text>'
    ]

    y = 82

    for label, value in rows:

        svg.extend([
            f'<text x="30" y="{y}" '
            f'font-family="Arial, sans-serif" '
            f'font-size="15" fill="{muted}">'
            f'{escape(label)}</text>',

            f'<text x="{width - 30}" y="{y}" '
            f'text-anchor="end" '
            f'font-family="Arial, sans-serif" '
            f'font-size="17" font-weight="700" '
            f'fill="{text}">{escape(str(value))}</text>',

            f'<line x1="30" y1="{y + 15}" '
            f'x2="{width - 30}" y2="{y + 15}" '
            f'stroke="{border}"/>'
        ])

        y += 34

    svg.append("</svg>")

    return "\n".join(svg)


# Create output directory
Path("dist").mkdir(exist_ok=True)


# GitHub statistics
stats_svg = create_svg(
    "GitHub Engineering Metrics",
    [
        ("Public repositories", public_repositories),
        ("Total stars", total_stars),
        ("Total forks", total_forks),
        ("Followers", user.get("followers", 0)),
        ("Public gists", user.get("public_gists", 0)),
    ]
)


Path("dist/github-stats.svg").write_text(
    stats_svg,
    encoding="utf-8"
)


# Top languages
language_rows = []

for language, amount in top_languages:

    percentage = (
        amount / total_language_bytes
    ) * 100

    language_rows.append(
        (
            language,
            f"{percentage:.1f}%"
        )
    )


languages_svg = create_svg(
    "Top Languages",
    language_rows
)


Path("dist/top-languages.svg").write_text(
    languages_svg,
    encoding="utf-8"
)


print("Profile statistics generated successfully.")
