import json
import os
import urllib.error
import urllib.request
from collections import defaultdict
from pathlib import Path


USERNAME = "subahanpathan"
OUTPUT_DIR = Path("dist/profile")
API_BASE = "https://api.github.com"

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

FALLBACK_COLORS = [
    "#60A5FA",
    "#A78BFA",
    "#22D3EE",
    "#34D399",
    "#F59E0B",
    "#FB7185",
    "#94A3B8",
]


def github_request(endpoint):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-metrics",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    token = os.getenv("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(
        f"{API_BASE}{endpoint}",
        headers=headers,
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        print(f"GitHub API error {error.code}: {endpoint}")
        raise


def get_profile():
    return github_request(f"/users/{USERNAME}")


def get_repositories():
    repositories = []
    page = 1

    while True:
        data = github_request(
            f"/users/{USERNAME}/repos"
            f"?per_page=100"
            f"&page={page}"
            f"&type=all"
            f"&sort=updated"
            f"&direction=desc"
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
    except Exception as error:
        print(
            f"Unable to fetch languages for "
            f"{owner}/{name}: {error}"
        )
        return {}


def collect_language_statistics(repositories):
    totals = defaultdict(int)

    for repository in repositories:
        if repository.get("fork"):
            continue

        if repository.get("archived"):
            continue

        print(
            f"Fetching languages: "
            f"{repository.get('name')}"
        )

        languages = get_languages(repository)

        for language, byte_count in languages.items():
            totals[language] += byte_count

    total_bytes = sum(totals.values())

    if total_bytes == 0:
        return []

    languages = [
        {
            "name": language,
            "bytes": byte_count,
            "percentage": (byte_count / total_bytes) * 100,
        }
        for language, byte_count in totals.items()
    ]

    languages.sort(
        key=lambda item: item["bytes"],
        reverse=True,
    )

    top_languages = languages[:7]

    other_bytes = sum(
        item["bytes"]
        for item in languages[7:]
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
    return (
        str(value)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def color_for(language, index):
    if language in LANGUAGE_COLORS:
        return LANGUAGE_COLORS[language]

    return FALLBACK_COLORS[
        index % len(FALLBACK_COLORS)
    ]


def metric_card(x, y, width, height, label, value, subtitle, accent):
    return f"""
    <g>
      <rect
        x="{x}" y="{y}"
        width="{width}" height="{height}"
        rx="16"
        fill="#0B1220"
        stroke="#26364D"
        stroke-width="1"
      />

      <rect
        x="{x + 20}" y="{y + 20}"
        width="4" height="44"
        rx="2"
        fill="{accent}"
      />

      <text
        x="{x + 38}" y="{y + 36}"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="14"
        font-weight="600"
        fill="#94A3B8"
      >{esc(label)}</text>

      <text
        x="{x + 20}" y="{y + 96}"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="34"
        font-weight="800"
        fill="{accent}"
      >{esc(value)}</text>

      <text
        x="{x + 20}" y="{y + 124}"
        font-family="Segoe UI, Arial, sans-serif"
        font-size="12"
        fill="#64748B"
      >{esc(subtitle)}</text>
    </g>
    """


def donut_segments(languages, cx, cy, radius):
    circumference = 2 * 3.14159265359 * radius
    segments = []
    offset = 0

    for index, language in enumerate(languages):
        percentage = language["percentage"]
        length = (percentage / 100) * circumference
        color = color_for(language["name"], index)

        segments.append(
            f"""
            <circle
              cx="{cx}"
              cy="{cy}"
              r="{radius}"
              fill="none"
              stroke="{color}"
              stroke-width="30"
              stroke-linecap="butt"
              stroke-dasharray="{length:.2f} {circumference:.2f}"
              stroke-dashoffset="{-offset:.2f}"
              transform="rotate(-90 {cx} {cy})"
            />
            """
        )

        offset += length

    return "\n".join(segments)


def generate_svg(profile, repositories, languages):
    width = 1600
    height = 900

    own_repositories = [
        repository
        for repository in repositories
        if not repository.get("fork")
    ]

    active_repositories = [
        repository
        for repository in own_repositories
        if not repository.get("archived")
    ]

    public_repositories = profile.get("public_repos", 0)
    followers = profile.get("followers", 0)
    public_gists = profile.get("public_gists", 0)

    total_stars = sum(
        repository.get("stargazers_count", 0)
        for repository in own_repositories
    )

    total_forks = sum(
        repository.get("forks_count", 0)
        for repository in own_repositories
    )

    active_count = len(active_repositories)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg
  xmlns="http://www.w3.org/2000/svg"
  width="{width}"
  height="{height}"
  viewBox="0 0 {width} {height}"
>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#050A14"/>
      <stop offset="100%" stop-color="#0B1220"/>
    </linearGradient>

    <linearGradient id="accent" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#60A5FA"/>
      <stop offset="50%" stop-color="#A78BFA"/>
      <stop offset="100%" stop-color="#22D3EE"/>
    </linearGradient>
  </defs>

  <rect width="{width}" height="{height}" fill="url(#bg)"/>

  <text
    x="44" y="58"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="36"
    font-weight="800"
    fill="#F8FAFC"
  >05 · ENGINEERING METRICS</text>

  <text
    x="46" y="90"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="17"
    fill="#94A3B8"
  >Live repository signals generated from GitHub activity.</text>

  <rect
    x="46" y="110"
    width="1508" height="3"
    rx="1.5"
    fill="url(#accent)"
  />

  <rect
    x="44" y="138"
    width="1512" height="270"
    rx="18"
    fill="#08101E"
    stroke="#26364D"
    stroke-width="1"
  />

  <text
    x="70" y="180"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="23"
    font-weight="700"
    fill="#F8FAFC"
  >GitHub Engineering Metrics</text>

  {metric_card(68, 205, 275, 155, "PUBLIC REPOSITORIES", public_repositories, "Repositories visible publicly", "#22C55E")}
  {metric_card(365, 205, 275, 155, "TOTAL STARS", total_stars, "Stars across your projects", "#60A5FA")}
  {metric_card(662, 205, 275, 155, "TOTAL FORKS", total_forks, "Forks across your projects", "#A78BFA")}
  {metric_card(959, 205, 275, 155, "FOLLOWERS", followers, "People following you", "#22D3EE")}
  {metric_card(1256, 205, 275, 155, "ACTIVE REPOSITORIES", active_count, "Non-archived own repos", "#F59E0B")}

  <rect
    x="44" y="430"
    width="1512" height="390"
    rx="18"
    fill="#08101E"
    stroke="#26364D"
    stroke-width="1"
  />

  <text
    x="70" y="476"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="23"
    font-weight="700"
    fill="#F8FAFC"
  >Language Profile</text>

  <text
    x="70" y="503"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="15"
    fill="#94A3B8"
  >Aggregated by bytes across active, non-fork repositories.</text>
"""

    visible = languages[:7]

    bar_x = 235
    bar_width = 520
    percentage_x = 790
    label_x = 70
    start_y = 548
    row_height = 39

    for index, language in enumerate(visible):
        y = start_y + index * row_height
        name = language["name"]
        percentage = language["percentage"]
        color = color_for(name, index)

        fill_width = max(
            8,
            bar_width * min(percentage / 100, 1),
        )

        svg += f"""
        <text
          x="{label_x}" y="{y + 5}"
          font-family="Segoe UI, Arial, sans-serif"
          font-size="15"
          font-weight="600"
          fill="#E2E8F0"
        >{esc(name)}</text>

        <rect
          x="{bar_x}" y="{y - 12}"
          width="{bar_width}" height="14"
          rx="7"
          fill="#142238"
        />

        <rect
          x="{bar_x}" y="{y - 12}"
          width="{fill_width:.2f}" height="14"
          rx="7"
          fill="{color}"
        />

        <text
          x="{percentage_x}" y="{y + 5}"
          font-family="Segoe UI, Arial, sans-serif"
          font-size="15"
          font-weight="700"
          fill="#E2E8F0"
        >{percentage:.1f}%</text>
        """

    svg += """
  <line
    x1="900" y1="520"
    x2="900" y2="785"
    stroke="#26364D"
    stroke-width="1"
  />
  """

    donut_cx = 1060
    donut_cy = 648
    donut_radius = 84

    svg += f"""
  <circle
    cx="{donut_cx}" cy="{donut_cy}" r="{donut_radius}"
    fill="none"
    stroke="#142238"
    stroke-width="30"
  />

  {donut_segments(
      visible,
      donut_cx,
      donut_cy,
      donut_radius,
  )}

  <circle
    cx="{donut_cx}" cy="{donut_cy}" r="59"
    fill="#08101E"
  />

  <text
    x="{donut_cx}" y="{donut_cy - 2}"
    text-anchor="middle"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="23"
    font-weight="800"
    fill="#F8FAFC"
  >100%</text>

  <text
    x="{donut_cx}" y="{donut_cy + 20}"
    text-anchor="middle"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="12"
    fill="#94A3B8"
  >LANGUAGE MIX</text>
    """

    legend_x = 1190
    legend_y = 565

    for index, language in enumerate(visible):
        y = legend_y + index * 31
        name = language["name"]
        percentage = language["percentage"]
        color = color_for(name, index)

        svg += f"""
  <circle
    cx="{legend_x}" cy="{y - 4}"
    r="7"
    fill="{color}"
  />

  <text
    x="{legend_x + 20}" y="{y}"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="14"
    font-weight="600"
    fill="#E2E8F0"
  >{esc(name)}</text>

  <text
    x="1490" y="{y}"
    text-anchor="end"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="14"
    font-weight="700"
    fill="#E2E8F0"
  >{percentage:.1f}%</text>
        """

    svg += """
  <text
    x="46" y="860"
    font-family="Segoe UI, Arial, sans-serif"
    font-size="14"
    fill="#64748B"
  >Automatically generated with GitHub Actions · No manual edits required.</text>
</svg>
"""

    return svg


def main():
    print("=" * 64)
    print(" GitHub Profile Metrics Generator")
    print("=" * 64)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    profile = get_profile()
    repositories = get_repositories()

    print(
        f"Repositories discovered: "
        f"{len(repositories)}"
    )

    languages = collect_language_statistics(
        repositories
    )

    svg = generate_svg(
        profile,
        repositories,
        languages,
    )

    for filename in (
        "stats.svg",
        "languages.svg",
    ):
        path = OUTPUT_DIR / filename
        path.write_text(
            svg,
            encoding="utf-8",
        )
        print(f"✓ Generated {path}")

    print("Generation completed successfully.")


if __name__ == "__main__":
    main()
