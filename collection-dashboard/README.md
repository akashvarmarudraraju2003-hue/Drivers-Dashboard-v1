# Driver Collection Dashboard
A GitHub Action downloads the driver report every 30 minutes, builds `data.json`, and publishes the dashboard on GitHub Pages.

## Setup (5 minutes)
1. Create a new GitHub repo and upload everything in this folder (keep `.github/workflows/update.yml`).
2. Repo **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Go to **Actions → Update dashboard → Run workflow**. When it finishes, your URL is shown in the job (https://<user>.github.io/<repo>/).

## Privacy - read this
GitHub Pages sites are **public** unless your GitHub plan supports private Pages (Enterprise Cloud). The dashboard shows driver names and balances.
- By default only the last 4 digits of each driver ID are published (`MASK_IDS=1` in `build.py`).
- If names must not be public, use a private-Pages plan, or host the same `site/` folder behind a login (e.g. Cloudflare Access, Netlify password).

## Local test
`pip install pandas openpyxl && python build.py driver_report.xlsx` then open `site/index.html` through a local server (`python -m http.server -d site`).
