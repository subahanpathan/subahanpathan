import json
import os
import urllib.request


USER = "subahanpathan"

README = "README.md"

START = "<!-- PROJECTS_START -->"
END = "<!-- PROJECTS_END -->"


request = urllib.request.Request(
    f"https://api.github.com/users/{USER}/repos"
    f"?per_page=100&sort=updated&direction=desc",

    headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {os.environ.get('GH_TOKEN', '')}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "profile-maintainer",
    },
)


with urllib.request.urlopen(
    request,
    timeout=30
) as response:

    repositories = json.load(response)


# Remove forks, archived repositories,
# and the profile repository itself.

repositories = [
    repo
    for repo in repositories

    if not repo.get("fork")
    and repo.get("name", "").lower() != USER.lower()
    and not repo.get("archived")
]


# Rank repositories by quality signals.

repositories.sort(
    key=lambda repo: (
        bool(repo.get("description")),
        repo.get("stargazers_count", 0),
        repo.get("forks_count", 0),
        repo.get("updated_at", ""),
    ),

    reverse=True,
)


# Select six projects.

selected_projects = repositories[:6]


project_sections = []


for repository in selected_projects:

    name = repository["name"]

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

        description = (
            description[:147]
            + "..."
        )


    language = (
        repository.get("language")
        or "Code"
    )


    stars = repository.get(
        "stargazers_count",
        0
    )


    project_sections.append(
        f"### [{name}]"
        f"(https://github.com/{USER}/{name})\n\n"
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


# Read README.

with open(
    README,
    "r",
    encoding="utf-8"
) as file:

    content = file.read()


# Find project section.

start_position = (
    content.index(START)
    + len(START)
)

end_position = content.index(
    END
)


# Replace project section.

updated_content = (
    content[:start_position]
    + "\n"
    + generated_projects
    + "\n"
    + content[end_position:]
)


# Save README.

with open(
    README,
    "w",
    encoding="utf-8"
) as file:

    file.write(updated_content)


print(
    f"Updated {len(selected_projects)} projects."
)
