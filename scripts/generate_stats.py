import json
import os
import urllib.request
import urllib.error
from pathlib import Path
from collections import defaultdict


USERNAME = "subahanpathan"
OUTPUT_DIR = Path("dist/profile")

API_BASE = "https://api.github.com"

COLORS = [
    "#3178C6",  # TypeScript
    "#F7DF1E",  # JavaScript
    "#E34F26",  # HTML
    "#3776AB",  # Python
    "#1572B6",  # CSS
    "#22C55E",  # Shell
    "#A855F7",
    "#06B6D4",
    "#F97316",
    "#94A3B8",
]

LANGUAGE_COLORS = {
    "TypeScript": "#3178C6",
    "JavaScript": "#F7DF1E",
    "HTML": "#E34F26",
    "CSS": "#1572B6",
    "Python": "#3776AB",
    "Shell": "#22C55E",
    "Java": "#B07219",
    "C": "#555555",
    "C++": "#F34B7D",
    "C#": "#178600",
    "Go": "#00ADD8",
    "Rust": "#DEA584",
    "PHP": "#4F5D95",
    "Ruby": "#701516",
    "Kotlin": "#A97BFF",
    "Dart": "#00B4AB",
    "Swift": "#F05138",
    "Jupyter Notebook": "#DA5B0B",
}


def github_request(endpoint):
    url = f"{API_BASE}{endpoint}"

    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-metrics",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    token = os.getenv("GH_TOKEN")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        url,
        headers=headers,
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    except urllib.error.HTTPError as error:
        print(f"GitHub API error {error.code}: {url}")

        if error.code == 403:
            print("GitHub API rate limit may have been exceeded.")

        raise

    except Exception as error:
        print(f"Request failed: {error}")
        raise


def get_profile():
    print(f"Fetching GitHub profile: {USERNAME}")

    return github_request(
        f"/users/{USERNAME}"
    )


def get_repositories():
    repositories = []

    page = 1

    while True:
        print(f"Fetching repositories page {page}")

        data = github_request(
            f"/users/{USERNAME}/repos"
            f"?per_page=100"
            f"&page={page}"
            f"&type=all"
            f"&sort=updated"
        )

        if not data:
            break

        repositories.extend(data)

        if len(data) < 100:
            break

        page += 1

    return repositories


def get_languages(repository):
    owner = repository["owner"]["login"]
    name = repository["name"]

    try:
        return github_request(
            f"/repos/{owner}/{name}/languages"
        )

    except Exception:
        print(
            f"Unable to fetch languages for {owner}/{name}"
        )
        return {}


def collect_language_statistics(repositories):
    totals = defaultdict(int)

    for repository in repositories:

        # Skip forks so the profile reflects the user's
        # own engineering work more accurately.
        if repository.get("fork"):
            continue

        name = repository.get("name")

        print(f"Fetching languages: {name}")

        languages = get_languages(repository)

        for language, bytes_count in languages.items():
            totals[language] += bytes_count

    total_bytes = sum(totals.values())

    if total_bytes == 0:
        return []

    languages = []

    for language, bytes_count in totals.items():

        percentage = (
            bytes_count / total_bytes
        ) * 100

        languages.append(
            {
                "name": language,
                "bytes": bytes_count,
                "percentage": percentage,
            }
        )

    languages.sort(
        key=lambda item: item["bytes"],
        reverse=True,
    )

    # Keep the dashboard readable.
    # Combine everything below the sixth language
    # into "Other".
    top_languages = languages[:6]

    other_bytes = sum(
        item["bytes"]
        for item in languages[6:]
    )

    if other_bytes > 0:
        top_languages.append(
            {
                "name": "Other",
                "bytes": other_bytes,
                "percentage": (
                    other_bytes / total_bytes
                ) * 100,
            }
        )

    return top_languages


def esc(value):
    """Escape text safely for SVG."""

    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def language_color(language, index):
    return LANGUAGE_COLORS.get(
        language,
        COLORS[index % len(COLORS)],
    )


def donut_segments(languages, cx, cy, radius):
    circumference = 2 * 3.14159265359 * radius

    segments = []

    offset = 0

    for index, language in enumerate(languages):

        percentage = language["percentage"]

        length = (
            percentage / 100
        ) * circumference

        color = language_color(
            language["name"],
            index,
        )

        segments.append(
            f"""
            <circle
                cx="{cx}"
                cy="{cy}"
                r="{radius}"
                fill="none"
                stroke="{color}"
                stroke-width="32"
                stroke-linecap="butt"
                stroke-dasharray="{length:.2f} {circumference:.2f}"
                stroke-dashoffset="{-offset:.2f}"
                transform="rotate(-90 {cx} {cy})"
            />
            """
        )

        offset += length

    return "\n".join(segments)


def metric_card(
    x,
    y,
    width,
    height,
    title,
    value,
    subtitle,
    accent,
    icon,
):
    return f"""
    <g>

        <rect
            x="{x}"
            y="{y}"
            width="{width}"
            height="{height}"
            rx="16"
            fill="#0B1220"
            stroke="{accent}"
            stroke-opacity="0.65"
            stroke-width="1.4"
        />

        <rect
            x="{x + 20}"
            y="{y + 20}"
            width="48"
            height="48"
            rx="14"
            fill="{accent}"
            fill-opacity="0.18"
        />

        <text
            x="{x + 44}"
            y="{y + 51}"
            text-anchor="middle"
            font-family="Segoe UI, Arial, sans-serif"
            font-size="22"
            font-weight="700"
            fill="{accent}"
        >{esc(icon)}</text>

        <text
            x="{x + 84}"
            y="{y + 41}"
            font-family="Segoe UI, Arial, sans-serif"
            font-size="16"
            font-weight="600"
            fill="#E5E7EB"
        >{esc(title)}</text>

        <text
            x="{x + 24}"
            y="{y + 94}"
            font-family="Segoe UI, Arial, sans-serif"
            font-size="34"
            font-weight="800"
            fill="{accent}"
        >{esc(value)}</text>

        <text
            x="{x + 24}"
            y="{y + 122}"
            font-family="Segoe UI, Arial, sans-serif"
            font-size="13"
            fill="#94A3B8"
        >{esc(subtitle)}</text>

    </g>
    """


def generate_svg(profile, repositories, languages):
    width = 1600
    height = 870

    public_repositories = profile.get(
        "public_repos",
        0,
    )

    followers = profile.get(
        "followers",
        0,
    )

    public_gists = profile.get(
        "public_gists",
        0,
    )

    total_stars = sum(
        repository.get("stargazers_count", 0)
        for repository in repositories
        if not repository.get("fork")
    )

    total_forks = sum(
        repository.get("forks_count", 0)
        for repository in repositories
        if not repository.get("fork")
    )

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="{height}"
    viewBox="0 0 {width} {height}"
>

    <defs>

        <linearGradient
            id="background"
            x1="0"
            y1="0"
            x2="1"
            y2="1"
        >
            <stop
                offset="0%"
                stop-color="#050A14"
            />

            <stop
                offset="100%"
                stop-color="#0B1220"
            />
        </linearGradient>

        <linearGradient
            id="headerGlow"
            x1="0"
            y1="0"
            x2="1"
            y2="0"
        >
            <stop
                offset="0%"
                stop-color="#60A5FA"
            />

            <stop
                offset="50%"
                stop-color="#A78BFA"
            />

            <stop
                offset="100%"
                stop-color="#22D3EE"
            />
        </linearGradient>

        <filter
            id="shadow"
            x="-20%"
            y="-20%"
            width="140%"
            height="140%"
        >
            <feDropShadow
                dx="0"
                dy="8"
                stdDeviation="12"
                flood-color="#000000"
                flood-opacity="0.35"
            />
        </filter>

    </defs>


    <!-- Background -->

    <rect
        width="{width}"
        height="{height}"
        fill="url(#background)"
    />


    <!-- Header -->

    <text
        x="44"
        y="58"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="36"
        font-weight="800"
        fill="#F8FAFC"
    >
        05 · ENGINEERING METRICS
    </text>

    <text
        x="46"
        y="90"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="17"
        fill="#94A3B8"
    >
        Real activity. Real contributions. Real progress.
    </text>

    <line
        x1="46"
        y1="112"
        x2="1554"
        y2="112"
        stroke="#334155"
        stroke-width="1"
    />


    <!-- GitHub Metrics Panel -->

    <rect
        x="44"
        y="138"
        width="1512"
        height="278"
        rx="18"
        fill="#08101E"
        stroke="#26364D"
        stroke-width="1"
        filter="url(#shadow)"
    />

    <text
        x="70"
        y="182"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="23"
        font-weight="700"
        fill="#F8FAFC"
    >
        GitHub Engineering Metrics
    </text>


    <!-- Metric Cards -->

    {metric_card(
        68,
        208,
        275,
        160,
        "Public repositories",
        public_repositories,
        "Total repositories",
        "#22C55E",
        "▣",
    )}

    {metric_card(
        365,
        208,
        275,
        160,
        "Total stars",
        total_stars,
        "Stars across your projects",
        "#3B82F6",
        "☆",
    )}

    {metric_card(
        662,
        208,
        275,
        160,
        "Total forks",
        total_forks,
        "Repositories forked",
        "#A855F7",
        "⑂",
    )}

    {metric_card(
        959,
        208,
        275,
        160,
        "Followers",
        followers,
        "People following you",
        "#06B6D4",
        "♙",
    )}

    {metric_card(
        1256,
        208,
        275,
        160,
        "Public gists",
        public_gists,
        "Gists you've created",
        "#F59E0B",
        "</>",
    )}


    <!-- Languages Panel -->

    <rect
        x="44"
        y="438"
        width="1512"
        height="360"
        rx="18"
        fill="#08101E"
        stroke="#26364D"
        stroke-width="1"
        filter="url(#shadow)"
    />


    <text
        x="70"
        y="485"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="23"
        font-weight="700"
        fill="#F8FAFC"
    >
        Top Languages
    </text>

    <text
        x="70"
        y="512"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="15"
        fill="#94A3B8"
    >
        Languages you use most across your repositories.
    </text>


    <!-- Language bars -->

"""

    bar_x = 240
    bar_width = 545
    label_x = 70
    percentage_x = 820

    start_y = 550
    row_height = 39

    max_languages = min(
        len(languages),
        6,
    )

    visible_languages = languages[
        :max_languages
    ]

    for index, language in enumerate(
        visible_languages
    ):

        y = start_y + (
            index * row_height
        )

        name = language["name"]
        percentage = language["percentage"]

        color = language_color(
            name,
            index,
        )

        display_percentage = (
            f"{percentage:.1f}%"
        )

        bar_fill_width = (
            bar_width
            * min(
                percentage / 100,
                1,
            )
        )

        # Keep very small languages visible.
        if percentage > 0:
            bar_fill_width = max(
                bar_fill_width,
                8,
            )

        svg += f"""
        <text
            x="{label_x}"
            y="{y + 5}"
            font-family="Segoe UI, Arial, sans-serif"
            font-size="15"
            font-weight="600"
            fill="#E2E8F0"
        >
            {esc(name)}
        </text>

        <rect
            x="{bar_x}"
            y="{y - 12}"
            width="{bar_width}"
            height="14"
            rx="7"
            fill="#142238"
        />

        <rect
            x="{bar_x}"
            y="{y - 12}"
            width="{bar_fill_width:.2f}"
            height="14"
            rx="7"
            fill="{color}"
        />

        <text
            x="{percentage_x}"
            y="{y + 5}"
            font-family="Segoe UI, Arial, sans-serif"
            font-size="15"
            font-weight="700"
            fill="#E2E8F0"
        >
            {display_percentage}
        </text>
        """


    # Divider

    svg += """
    <line
        x1="900"
        y1="530"
        x2="900"
        y2="758"
        stroke="#26364D"
        stroke-width="1"
    />
    """


    # Donut chart

    donut_cx = 1060
    donut_cy = 645
    donut_radius = 82

    svg += f"""
    <circle
        cx="{donut_cx}"
        cy="{donut_cy}"
        r="{donut_radius}"
        fill="none"
        stroke="#142238"
        stroke-width="32"
    />

    {donut_segments(
        visible_languages,
        donut_cx,
        donut_cy,
        donut_radius,
    )}

    <circle
        cx="{donut_cx}"
        cy="{donut_cy}"
        r="58"
        fill="#08101E"
    />

    <text
        x="{donut_cx}"
        y="{donut_cy - 2}"
        text-anchor="middle"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="22"
        font-weight="800"
        fill="#F8FAFC"
    >
        100%
    </text>

    <text
        x="{donut_cx}"
        y="{donut_cy + 21}"
        text-anchor="middle"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="12"
        fill="#94A3B8"
    >
        Total Languages
    </text>
    """


    # Donut legend

    legend_x = 1190
    legend_y = 565

    for index, language in enumerate(
        visible_languages
    ):

        y = (
            legend_y
            + index * 35
        )

        name = language["name"]
        percentage = language["percentage"]

        color = language_color(
            name,
            index,
        )

        svg += f"""
        <circle
            cx="{legend_x}"
            cy="{y - 5}"
            r="9"
            fill="{color}"
        />

        <text
            x="{legend_x + 24}"
            y="{y}"
            font-family="Segoe UI, Arial, sans-serif"
            font-size="14"
            font-weight="600"
            fill="#E2E8F0"
        >
            {esc(name)}
        </text>

        <text
            x="1490"
            y="{y}"
            text-anchor="end"
            font-family="Segoe UI, Arial, sans-serif"
            font-size="14"
            font-weight="700"
            fill="#E2E8F0"
        >
            {percentage:.1f}%
        </text>
        """


    # Footer

    svg += """
    <text
        x="46"
        y="835"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="14"
        fill="#94A3B8"
    >
        ◉  Automatically generated from GitHub activity using GitHub Actions.
    </text>
    """


    svg += """
</svg>
"""

    return svg


def main():
    print("")
    print("=" * 60)
    print(" GitHub Profile Metrics Generator")
    print("=" * 60)
    print("")

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    profile = get_profile()

    repositories = get_repositories()

    print(
        f"Repositories discovered: {len(repositories)}"
    )

    languages = collect_language_statistics(
        repositories
    )

    print("")
    print("Top languages:")

    for language in languages:
        print(
            f"  {language['name']}: "
            f"{language['percentage']:.2f}%"
        )

    svg = generate_svg(
        profile,
        repositories,
        languages,
    )

    stats_path = (
        OUTPUT_DIR
        / "stats.svg"
    )

    stats_path.write_text(
        svg,
        encoding="utf-8",
    )

    # Keep the existing languages.svg path
    # available for compatibility with older
    # README references.
    languages_path = (
        OUTPUT_DIR
        / "languages.svg"
    )

    languages_path.write_text(
        svg,
        encoding="utf-8",
    )

    print("")
    print(
        f"✓ Generated: {stats_path}"
    )

    print(
        f"✓ Generated: {languages_path}"
    )

    print("")
    print("Generation completed successfully.")


if __name__ == "__main__":
    main()
