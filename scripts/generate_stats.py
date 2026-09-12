import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from html import escape


# ============================================================
# Configuration
# ============================================================

USER = "subahanpathan"

TOKEN = os.environ.get("GH_TOKEN", "")

API_HEADERS = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "subahanpathan-profile",
}

if TOKEN:
    API_HEADERS["Authorization"] = f"Bearer {TOKEN}"


# ============================================================
# GitHub API helper
# ============================================================

def get(url):
    request = urllib.request.Request(
        url,
        headers=API_HEADERS,
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=30,
        ) as response:

            return json.load(response)

    except urllib.error.HTTPError as error:

        print(f"GitHub API error: {error.code}")
        print(
            error.read().decode(
                "utf-8",
                errors="ignore",
            )
        )
        raise


# ============================================================
# Get GitHub profile
# ============================================================

user = get(
    f"https://api.github.com/users/{USER}"
)


# ============================================================
# Get repositories
# ============================================================

repositories = []

for page in range(1, 5):

    batch = get(
        f"https://api.github.com/users/{USER}/repos"
        f"?per_page=100"
        f"&page={page}"
        f"&sort=updated"
        f"&direction=desc"
    )

    repositories.extend(batch)

    if len(batch) < 100:
        break


# ============================================================
# Filter repositories
# ============================================================

non_fork_repositories = [
    repo
    for repo in repositories
    if not repo.get("fork")
]


# ============================================================
# GitHub statistics
# ============================================================

public_repositories = len(
    non_fork_repositories
)

total_stars = sum(
    repo.get("stargazers_count", 0)
    for repo in non_fork_repositories
)

total_forks = sum(
    repo.get("forks_count", 0)
    for repo in non_fork_repositories
)


# ============================================================
# Calculate languages
# ============================================================

languages = {}


for repository in non_fork_repositories:

    languages_url = repository.get(
        "languages_url"
    )

    if not languages_url:
        continue

    try:

        repo_languages = get(
            languages_url
        )

        for language, amount in repo_languages.items():

            languages[language] = (
                languages.get(language, 0)
                + amount
            )

    except Exception as error:

        print(
            f"Could not read languages for "
            f"{repository.get('name')}: {error}"
        )

        continue


top_languages = sorted(
    languages.items(),
    key=lambda item: item[1],
    reverse=True,
)[:6]


total_language_bytes = (
    sum(languages.values()) or 1
)


# ============================================================
# SVG generator
# ============================================================

def create_svg(
    title,
    rows,
    width=700,
):

    height = max(
        245,
        82 + (len(rows) * 34),
    )

    background = "#0d1117"
    text = "#f0f6fc"
    muted = "#8b949e"
    border = "#30363d"

    svg = [

        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{width}" '
        f'height="{height}" '
        f'viewBox="0 0 {width} {height}">',

        f'<rect '
        f'width="100%" '
        f'height="100%" '
        f'rx="14" '
        f'fill="{background}"/>',

        f'<text '
        f'x="28" '
        f'y="42" '
        f'font-family="Arial, sans-serif" '
        f'font-size="22" '
        f'font-weight="700" '
        f'fill="{text}">'
        f'{escape(title)}'
        f'</text>',
    ]

    y = 82

    for label, value in rows:

        svg.extend([

            f'<text '
            f'x="30" '
            f'y="{y}" '
            f'font-family="Arial, sans-serif" '
            f'font-size="15" '
            f'fill="{muted}">'
            f'{escape(str(label))}'
            f'</text>',

            f'<text '
            f'x="{width - 30}" '
            f'y="{y}" '
            f'text-anchor="end" '
            f'font-family="Arial, sans-serif" '
            f'font-size="17" '
            f'font-weight="700" '
            f'fill="{text}">'
            f'{escape(str(value))}'
            f'</text>',

            f'<line '
            f'x1="30" '
            f'y1="{y + 15}" '
            f'x2="{width - 30}" '
            f'y2="{y + 15}" '
            f'stroke="{border}"/>',
        ])

        y += 34

    svg.append("</svg>")

    return "\n".join(svg)


# ============================================================
# Create output directory
# ============================================================

output_directory = Path(
    "dist/profile"
)

output_directory.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# Generate GitHub statistics
# ============================================================

stats_svg = create_svg(
    "GitHub Engineering Metrics",
    [
        (
            "Public repositories",
            public_repositories,
        ),
        (
            "Total stars",
            total_stars,
        ),
        (
            "Total forks",
            total_forks,
        ),
        (
            "Followers",
            user.get("followers", 0),
        ),
        (
            "Public gists",
            user.get("public_gists", 0),
        ),
    ],
)


stats_file = (
    output_directory
    / "stats.svg"
)

stats_file.write_text(
    stats_svg,
    encoding="utf-8",
)


# ============================================================
# Generate top languages
# ============================================================

language_rows = []

for language, amount in top_languages:

    percentage = (
        amount
        / total_language_bytes
    ) * 100

    language_rows.append(
        (
            language,
            f"{percentage:.1f}%",
        )
    )


if not language_rows:

    language_rows.append(
        (
            "No language data",
            "—",
        )
    )


languages_svg = create_svg(
    "Top Languages",
    language_rows,
)


languages_file = (
    output_directory
    / "languages.svg"
)

languages_file.write_text(
    languages_svg,
    encoding="utf-8",
)


# ============================================================
# Finish
# ============================================================

print(
    "Profile statistics generated successfully."
)

print(
    f"Created: {stats_file}"
)

print(
    f"Created: {languages_file}"
)
