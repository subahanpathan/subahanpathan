import json
import os
import urllib.error
import urllib.request


# ============================================================
# Configuration
# ============================================================

USER = "subahanpathan"
README = "README.md"

START = "<!-- PROJECTS_START -->"
END = "<!-- PROJECTS_END -->"

GITHUB_API = (
    f"https://api.github.com/users/{USER}/repos"
    "?per_page=100&sort=updated&direction=desc"
)


# ============================================================
# Fetch repositories from GitHub
# ============================================================

headers = {
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "profile-maintainer",
}

# Use token when available.
token = os.environ.get("GH_TOKEN")

if token:
    headers["Authorization"] = f"Bearer {token}"


request = urllib.request.Request(
    GITHUB_API,
    headers=headers,
)


try:
    with urllib.request.urlopen(
        request,
        timeout=30,
    ) as response:

        repositories = json.load(response)

except urllib.error.HTTPError as error:

    print(f"GitHub API error: {error.code}")
    print(error.read().decode("utf-8", errors="ignore"))
    raise

except urllib.error.URLError as error:

    print(f"Network error: {error}")
    raise


# ============================================================
# Filter repositories
# ============================================================

repositories = [
    repo
    for repo in repositories
    if not repo.get("fork")
    and not repo.get("archived")
    and repo.get("name", "").lower() != USER.lower()
]


# ============================================================
# Rank repositories
# ============================================================

repositories.sort(
    key=lambda repo: (
        bool(repo.get("description")),
        repo.get("stargazers_count", 0),
        repo.get("forks_count", 0),
        repo.get("updated_at", ""),
    ),
    reverse=True,
)


# ============================================================
# Select projects
# ============================================================

selected_projects = repositories[:6]


# ============================================================
# Generate project showcase
# ============================================================

project_sections = []


for repository in selected_projects:

    name = repository.get("name", "Project")

    description = (
        repository.get("description")
        or "Open-source engineering project."
    )

    description = (
        description
        .replace("\n", " ")
        .strip()
    )

    if len(description) > 150:
        description = description[:147] + "..."

    language = (
        repository.get("language")
        or "Code"
    )

    stars = repository.get(
        "stargazers_count",
        0,
    )

    project_url = (
        f"https://github.com/{USER}/{name}"
    )

    project_sections.append(
        f"### [{name}]({project_url})\n\n"
        f"{description}\n\n"
        f"`{language}` · ⭐ {stars}"
    )


if project_sections:

    generated_projects = "\n\n".join(
        project_sections
    )

else:

    generated_projects = (
        "_Public projects will appear here automatically._"
    )


# ============================================================
# Read README
# ============================================================

with open(
    README,
    "r",
    encoding="utf-8",
) as file:

    content = file.read()


# ============================================================
# Create markers automatically if missing
# ============================================================

if START not in content or END not in content:

    print("Project markers not found.")

    marker_block = (
        f"{START}\n"
        f"{generated_projects}\n"
        f"{END}"
    )

    # Prefer inserting before Engineering Metrics.
    target_heading = "## Engineering Metrics"

    if target_heading in content:

        content = content.replace(
            target_heading,
            marker_block
            + "\n\n"
            + target_heading,
            1,
        )

    else:

        # Fallback: append to README.
        content = (
            content.rstrip()
            + "\n\n"
            + marker_block
            + "\n"
        )

    print("Project markers created automatically.")


# ============================================================
# Replace project section
# ============================================================

start_position = (
    content.index(START)
    + len(START)
)

end_position = content.index(
    END,
    start_position,
)


updated_content = (
    content[:start_position]
    + "\n"
    + generated_projects
    + "\n"
    + content[end_position:]
)


# ============================================================
# Write README
# ============================================================

with open(
    README,
    "w",
    encoding="utf-8",
) as file:

    file.write(updated_content)


print(
    f"Updated {len(selected_projects)} projects."
)
