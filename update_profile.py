import json, os, urllib.request

USER="subahanpathan"
README="README.md"
START="<!-- PROJECTS_START -->"
END="<!-- PROJECTS_END -->"

req=urllib.request.Request(
    f"https://api.github.com/users/{USER}/repos?per_page=100&sort=updated&direction=desc",
    headers={
        "Accept":"application/vnd.github+json",
        "Authorization":f"Bearer {os.environ.get('GH_TOKEN','')}",
        "X-GitHub-Api-Version":"2022-11-28",
        "User-Agent":"profile-maintainer"
    })
with urllib.request.urlopen(req,timeout=30) as r:
    repos=json.load(r)

repos=[r for r in repos if not r.get("fork") and r.get("name","").lower()!=USER.lower() and not r.get("archived")]
repos.sort(key=lambda r:(bool(r.get("description")),r.get("stargazers_count",0),r.get("forks_count",0),r.get("updated_at","")),reverse=True)

items=[]
for r in repos[:6]:
    name=r["name"]
    desc=(r.get("description") or "Open-source engineering project.").replace("\n"," ").strip()
    if len(desc)>150: desc=desc[:147]+"..."
    lang=r.get("language") or "Code"
    items.append(f'### [{name}](https://github.com/{USER}/{name})\n{desc}\n\n`{lang}` · ⭐ {r.get("stargazers_count",0)}')

generated="\n\n".join(items) or "_Public projects will appear here automatically._"
content=open(README,encoding="utf-8").read()
content=content[:content.index(START)+len(START)]+"\n"+generated+"\n"+content[content.index(END):]
open(README,"w",encoding="utf-8").write(content)
