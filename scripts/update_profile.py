import json
import os
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


USERNAME = "subahanpathan"
README_PATH = Path("README.md")
API_BASE = "https://api.github.com"

START_MARKER = "<!-- PROJECTS_START -->"
END_MARKER = "<!-- PROJECTS_END -->"


def github_request(endpoint):
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "github-profile-project-index",
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


def escape_markdown(value):
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("|", "\\|")
        .replace("\n", " ")
        .strip()
    )


def relative_time(iso_timestamp):
    if not iso_timestamp:
        return "—"

    try:
        updated = datetime.fromisoformat(
            iso_timestamp.replace("Z", "+00:00")
        )
    except ValueError:
        return "—"

    delta = datetime.now(timezone.utc) - updated

    if delta.days >= 365:
        years = delta.days // 365
        return f"{years}y ago"

    if delta.days >= 30:
        months = delta.days // 30
        return f"{months}mo ago"

    if delta.days >= 1:
        return f"{delta.days}d ago"

    hours = max(delta.seconds // 3600, 1)
    return f"{hours}h ago"


def score_repository(repository):
    description_bonus = 20 if repository.get("description") else 0
    stars = repository.get("stargazers_count", 0)
    forks = repository.get("forks_count", 0)

    updated_at = repository.get("updated_at", "")
    try:
        updated = datetime.fromisoformat(
            updated_at.replace("Z", "+00:00")
        ).timestamp()
    except ValueError:
        updated = 0

    return (
        description_bonus,
        stars * 10,
        forks * 5,
        updated,
    )


def select_repositories(repositories):
    candidates = []

    for repository in repositories:
        if repository.get("fork"):
            continue

        if repository.get("archived"):
            continue

        if repository.get("name") == USERNAME:
            continue

        candidates.append(repository)

    candidates.sort(
        key=score_repository,
        reverse=True,
    )

    return candidates[:10]


def build_project_index(repositories):
    lines = [
        START_MARKER,
        "## 11 · PROJECT INDEX",
        "",
        "_Automatically refreshed from GitHub repository activity._",
        "",
        "| Repository | Description | Stars | Updated |",
        "|---|---|---:|---:|",
    ]

    for repository in repositories:
        name = repository.get("name", "Repository")
        url = repository.get("html_url", "#")
        description = (
            repository.get("description")
            or "No repository description provided."
        )

        stars = repository.get("stargazers_count", 0)
        updated = relative_time(repository.get("updated_at"))

        lines.append(
            f"| [{escape_markdown(name)}]({url}) "
            f"| {escape_markdown(description)} "
            f"| {stars} "
            f"| {updated} |"
        )

    lines.extend(
        [
            "",
            "_Featured production projects are maintained separately above._",
            "",
            END_MARKER,
        ]
    )

    return "\n".join(lines)


def replace_project_index(readme, generated_section):
    if START_MARKER in readme and END_MARKER in readme:
        start = readme.index(START_MARKER)
        end = readme.index(END_MARKER) + len(END_MARKER)

        return (
            readme[:start]
            + generated_section
            + readme[end:]
        )

    metrics_heading = "## 05 · ENGINEERING METRICS"

    if metrics_heading in readme:
        return readme.replace(
            metrics_heading,
            generated_section + "\n\n---\n\n" + metrics_heading,
            1,
        )

    return readme.rstrip() + "\n\n" + generated_section + "\n"


def main():
    print("Refreshing automated GitHub project index...")

    if not README_PATH.exists():
        raise FileNotFoundError("README.md was not found.")

    repositories = get_repositories()
    selected = select_repositories(repositories)

    print(f"Repositories discovered: {len(repositories)}")
    print(f"Repositories selected for index: {len(selected)}")

    generated_section = build_project_index(selected)

    current_readme = README_PATH.read_text(encoding="utf-8")
    updated_readme = replace_project_index(
        current_readme,
        generated_section,
    )

    if updated_readme == current_readme:
        print("No README changes required.")
        return

    README_PATH.write_text(
        updated_readme,
        encoding="utf-8",
    )

    print("✓ README project index refreshed.")


if __name__ == "__main__":
    main()
