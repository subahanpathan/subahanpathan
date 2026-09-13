this is generated
let change now readme

Yes — this is a much better version for the README. The plain text lifecycle is replaced with the new professional “From Ideas to Impact” engineering graphic.

Download the update

Download README + engineering lifecycle image

It contains:

README.md
assets/
└── engineering-lifecycle.png
What changed

The old:

IDEA
 ↓
DESIGN
 ↓
BUILD
 ↓
TEST
...

is now replaced by the visual lifecycle:

IDEA → DESIGN → BUILD → TEST → AUTOMATE → DEPLOY → MONITOR → IMPROVE ↺

with your Subahan Pathan branding and technology stack.

Important

Upload both:

README.md
assets/engineering-lifecycle.png

The README already points to:

https://raw.githubusercontent.com/subahanpathan/subahanpathan/main/assets/engineering-lifecycle.png

So after pushing both files, it should display automatically.

Don't upload the image somewhere else or change the README URL. 

i want to do it manually guide me

Absolutely. Let's do it manually, one step at a time. No ZIP extraction confusion.

We only need to change two things:

Replace README.md
Add assets/engineering-lifecycle.png

GitHub supports uploading files directly from the repository page using Add file → Upload files.

Step 1 — Download the new README

Download this:

Download updated README.md

Save it somewhere easy, such as your Downloads folder.

Don't rename it.

Step 2 — Download the new lifecycle image

Download this image:

Download engineering-lifecycle.png

Again, save it somewhere easy to find.

Step 3 — Open your repository

Go to:

subahanpathan/subahanpathan

Make sure you're on the main branch.

Step 4 — Replace README.md

On the repository page, find:

README.md

Click it.

Then click the pencil ✏️ Edit this file button.

GitHub supports editing a README directly from the repository UI.

Important

You will see all your current README code.

Press:

Ctrl + A

Then delete everything.

Now open the new README.md that you downloaded.

Press:

Ctrl + A → Ctrl + C

Go back to GitHub and press:

Ctrl + V

You should now see the new README code.

Step 5 — Commit the README

Scroll to the bottom.

For commit message, enter:

feat: upgrade engineering lifecycle section

Then choose the option to commit directly to main if GitHub gives you that choice.

Click:

Commit changes

Step 6 — Add the image

Now go back to the main repository page.

Click:

Add file → Upload files

GitHub's official instructions use this exact upload flow.

Upload:

engineering-lifecycle.png

But don't commit it to the root.

On the upload page, you can drag the image in. Then we need it inside:

assets/

The easiest method is:

Before uploading

If assets doesn't exist, click:

Add file → Create new file

In the filename box enter:

assets/engineering-lifecycle.png

However, GitHub's browser editor isn't suitable for putting binary image data into the file manually.

So instead, use Add file → Upload files, then upload the image into the assets directory if the interface lets you navigate there. GitHub supports uploading files to a selected repository folder.

If assets doesn't exist

Do this:

Click Add file
Click Create new file
Filename:
assets/.gitkeep
Commit it.

Then:

Open the new assets folder
Click Add file
Click Upload files
Upload:
engineering-lifecycle.png
Commit.

You can later delete .gitkeep; it isn't required once the image exists.

Step 7 — Check the image

Your repository should now look like:

subahanpathan/
└── subahanpathan/
    ├── .github/
    ├── assets/
    │   └── engineering-lifecycle.png
    ├── scripts/
    └── README.md

The README references:

assets/engineering-lifecycle.png

through the raw GitHub URL, so the image will render inside the profile README.

Step 8 — Refresh your profile

Open:

Your GitHub profile

Press:

Ctrl + F5

You should now see the new:

07 · HOW I ENGINEER

with:

IDEA → DESIGN → BUILD → TEST → AUTOMATE → DEPLOY → MONITOR → IMPROVE

instead of the old text diagram.

Do only Step 1 now

Download the new README first. Once you've done that, tell me "done", and I'll guide you through Step 2 only.

README.md
Document
engineering-lifecycle.png
Image
Ad

Sponsored options
Ad
README.md

<div align="center">

SUBAHAN PATHAN
FULL-STACK ENGINEER · DEVOPS · CLOUD · AUTOMATION

Building production-ready software with a focus on scalable architecture, reliable delivery, and practical automation.

<p> <a href="https://github.com/subahanpathan"> <img src="https://img.shields.io/badge/GitHub-111827?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"> </a> <a href="https://www.linkedin.com/in/subahan-pathan-a991a1337/"> <img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"> </a> <a href="https://github.com/subahanpathan?tab=repositories"> <img src="https://img.shields.io/badge/Projects-0F172A?style=for-the-badge&logo=github&logoColor=white" alt="Projects"> </a> </p>

</div>

01 · ENGINEERING PROFILE

I work across the full software lifecycle — from product interfaces and backend services to databases, cloud infrastructure, CI/CD, and operational automation.

My approach is simple:

Build clean. Automate repeatable work. Ship reliably. Improve continuously.

Area	Focus
Full-Stack Engineering	React, Next.js, TypeScript, JavaScript, Node.js, Python
Backend & Data	REST APIs, PostgreSQL, MongoDB, MySQL, Redis
DevOps & Cloud	Docker, Kubernetes, AWS, Linux, Nginx, Terraform
Delivery & Automation	Git, GitHub Actions, Jenkins, CI/CD, scripting, deployment automation
02 · ENGINEERING FOCUS

<table> <tr> <td width="25%" valign="top">

Product Engineering
Responsive interfaces
Component-driven UI
API integration
Full-stack applications
Production deployments

</td> <td width="25%" valign="top">

Backend Systems
REST APIs
Authentication
Data modeling
PostgreSQL / MongoDB
Service integration

</td> <td width="25%" valign="top">

DevOps & Cloud
Docker
Kubernetes
AWS
Linux / Nginx
Infrastructure as code

</td> <td width="25%" valign="top">

Automation
GitHub Actions
Jenkins
CI/CD pipelines
Bash / Python automation
Monitoring mindset

</td> </tr> </table>

03 · TECHNOLOGY STACK

Application

<p> <img src="https://skillicons.dev/icons?i=ts,js,react,nextjs,nodejs,python,html,css" alt="Application technologies"> </p>

Data

<p> <img src="https://skillicons.dev/icons?i=postgres,mongodb,redis,mysql" alt="Data technologies"> </p>

Cloud & Infrastructure

<p> <img src="https://skillicons.dev/icons?i=aws,docker,kubernetes,terraform,linux,nginx" alt="Cloud and infrastructure technologies"> </p>

Delivery & Tooling

<p> <img src="https://skillicons.dev/icons?i=git,github,githubactions,jenkins,vercel,vscode" alt="Delivery and tooling technologies"> </p>

04 · FEATURED PRODUCTION WORK

<table> <tr> <td width="50%" valign="top">

<a href="https://erp-topaz-three.vercel.app/"> <img src="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/previews/erp.png" alt="ERP project preview"> </a>

ERP

Production web application focused on business workflow and operational management.

Stack: Full-stack web · Database · Deployment

<p> <a href="https://erp-topaz-three.vercel.app/">Live Preview</a> · <a href="https://github.com/subahanpathan/ERP">Source</a> </p>

</td> <td width="50%" valign="top">

<a href="https://sub-verse-six.vercel.app/"> <img src="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/previews/subverse.png" alt="Sub-Verse project preview"> </a>

Sub-Verse

A modern web experience built around interactive product-style presentation.

Stack: React · Next.js · TypeScript · Deployment

<p> <a href="https://sub-verse-six.vercel.app/">Live Preview</a> · <a href="https://github.com/subahanpathan/-SubVerse">Source</a> </p>

</td> </tr>

<tr> <td width="50%" valign="top">

<a href="https://meter-flow-mu.vercel.app/"> <img src="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/previews/meter-flow.png" alt="Meter Flow project preview"> </a>

Meter Flow

Web application for managing meter-oriented operational workflows and data.

Stack: Full-stack web · Data · Deployment

<p> <a href="https://meter-flow-mu.vercel.app/">Live Preview</a> · <a href="https://github.com/subahanpathan/meter-flow">Source</a> </p>

</td> <td width="50%" valign="top">

<a href="https://bug-tracker-omega-three.vercel.app/"> <img src="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/previews/bug-tracker.png" alt="Bug Tracker project preview"> </a>

Bug Tracker

Application for organizing software issues, tracking work, and improving development visibility.

Stack: React · Node.js · Database · Deployment

<p> <a href="https://bug-tracker-omega-three.vercel.app/">Live Preview</a> · <a href="https://github.com/subahanpathan/Bug-Tracker">Source</a> </p>

</td> </tr>

<tr> <td width="50%" valign="top">

<a href="https://nexus-ai-inky-iota.vercel.app/"> <img src="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/previews/nexus-ai.png" alt="Nexus AI project preview"> </a>

Nexus AI

AI-focused application exploring practical interfaces and intelligent application workflows.

Stack: AI · Full-stack web · API integration

<p> <a href="https://nexus-ai-inky-iota.vercel.app/">Live Preview</a> · <a href="https://github.com/subahanpathan/nexus-ai">Source</a> </p>

</td> <td width="50%" valign="top">

<a href="https://signflow-olive-three.vercel.app/"> <img src="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/previews/signflow.png" alt="SignFlow project preview"> </a>

SignFlow

Web application centered around digital workflow and document-signing experiences.

Stack: Full-stack web · Workflow · Deployment

<p> <a href="https://signflow-olive-three.vercel.app/">Live Preview</a> · <a href="https://github.com/subahanpathan/signflow">Source</a> </p>

</td> </tr> </table>

05 · ENGINEERING METRICS

<p align="center"> <img src="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/profile/stats.svg" alt="GitHub Engineering Metrics" width="100%" /> </p>

<p align="center"> <sub>Automatically generated from GitHub activity using GitHub Actions.</sub> </p>

06 · CONTRIBUTION ACTIVITY

<p align="center"> <picture> <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/github-contribution-grid-snake-dark.svg"> <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/github-contribution-grid-snake.svg"> <img src="https://raw.githubusercontent.com/subahanpathan/subahanpathan/output/github-contribution-grid-snake.svg" alt="GitHub contribution snake animation"> </picture> </p>

07 · HOW I ENGINEER

<p align="center"> <img src="https://raw.githubusercontent.com/subahanpathan/subahanpathan/main/assets/engineering-lifecycle.png" alt="From Ideas to Impact — engineering lifecycle" width="100%" /> </p>

08 · ENGINEERING PRINCIPLES
Clarity over complexity — simple systems are easier to maintain.
Automation over repetition — repeatable work should become a pipeline.
Security by default — permissions and secrets should be intentional.
Observability matters — production systems need useful signals.
Ship, measure, improve — delivery is a loop, not a finish line.
09 · CURRENT DIRECTION

I'm focused on building stronger systems across:

Full-Stack Development · DevOps · Cloud Infrastructure · CI/CD · Automation · AI-enabled Applications

10 · LET'S CONNECT

<p align="center"> <a href="https://github.com/subahanpathan"> <img src="https://img.shields.io/badge/GitHub-View%20Profile-111827?style=for-the-badge&logo=github&logoColor=white" alt="GitHub profile"> </a> <a href="https://www.linkedin.com/in/subahan-pathan-a991a1337/"> <img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn profile"> </a> </p>

<!-- PROJECTS_START -->

11 · PROJECT INDEX

Refreshing automatically from GitHub repository activity.

<!-- PROJECTS_END -->

<p align="center"> <sub>Designed and maintained as an automated engineering profile.</sub> </p>
