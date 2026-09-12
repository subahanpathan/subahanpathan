import json, os, urllib.request
from pathlib import Path
from html import escape

USER="subahanpathan"
TOKEN=os.environ["GH_TOKEN"]

def get(url):
    req=urllib.request.Request(url, headers={
        "Accept":"application/vnd.github+json",
        "Authorization":f"Bearer {TOKEN}",
        "X-GitHub-Api-Version":"2022-11-28",
        "User-Agent":"subahanpathan-profile"
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

u=get(f"https://api.github.com/users/{USER}")
repos=[]
for page in range(1,5):
    batch=get(f"https://api.github.com/users/{USER}/repos?per_page=100&page={page}")
    repos += batch
    if len(batch)<100: break

public_repos=len([r for r in repos if not r.get("fork")])
stars=sum(r.get("stargazers_count",0) for r in repos)
forks=sum(r.get("forks_count",0) for r in repos)
languages={}
for r in repos:
    for lang, n in get(r["languages_url"]).items():
        languages[lang]=languages.get(lang,0)+n

top=sorted(languages.items(), key=lambda x:x[1], reverse=True)[:6]
total=sum(languages.values()) or 1

def svg(title, rows, width=700, height=245):
    bg="#0d1117"; fg="#f0f6fc"; muted="#8b949e"; line="#30363d"
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
         f'<rect width="100%" height="100%" rx="14" fill="{bg}"/>',
         f'<text x="28" y="42" font-family="Arial, sans-serif" font-size="22" font-weight="700" fill="{fg}">{escape(title)}</text>']
    y=82
    for label,value in rows:
        out += [f'<text x="30" y="{y}" font-family="Arial, sans-serif" font-size="15" fill="{muted}">{escape(label)}</text>',
                f'<text x="{width-30}" y="{y}" text-anchor="end" font-family="Arial, sans-serif" font-size="17" font-weight="700" fill="{fg}">{escape(str(value))}</text>',
                f'<line x1="30" y1="{y+15}" x2="{width-30}" y2="{y+15}" stroke="{line}"/>']
        y += 34
    out.append("</svg>")
    return "\n".join(out)

Path("dist").mkdir(exist_ok=True)
Path("dist/github-stats.svg").write_text(svg("GitHub Engineering Metrics",[
    ("Public repositories",public_repos),
    ("Total stars",stars),
    ("Total forks",forks),
    ("Followers",u.get("followers",0)),
    ("Public gists",u.get("public_gists",0)),
]),encoding="utf-8")

rows=[]
for lang,n in top:
    rows.append((lang, f"{n/total*100:.1f}%"))
Path("dist/top-languages.svg").write_text(svg("Top Languages",rows,height=max(245,82+34*len(rows))),encoding="utf-8")
