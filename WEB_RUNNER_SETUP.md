# Web runner setup

## 1. Upload files

Upload this project to a GitHub repo.

## 2. Publish the page

Run **Actions → Publish GitHub Pages** once. Then set **Settings → Pages → Deploy from branch → gh-pages → /root**.

## 3. Create a token

Create a fine-grained GitHub personal access token:

- Repository access: selected repository only
- Repository permissions: **Actions: Read and write**

## 4. Use the webpage

Open your GitHub Pages URL, enter:

- owner
- repo
- branch: `main`
- token
- URLs

Click **Run and show results**. The page starts GitHub Actions and waits for the result JSON to appear under `/results/<job_id>.json`.

## Security note

Do not embed the token in JavaScript. This static GitHub Pages approach requires the repo owner to paste a token at runtime. For a public no-token webpage, you need a real backend/serverless function to hold the secret safely.
