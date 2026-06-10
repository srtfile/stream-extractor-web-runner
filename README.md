# Stream Extractor Web Runner

This repo runs the Python stream extractor through GitHub Actions and shows results inside a GitHub Pages webpage.

> Use only for media URLs you own or have permission to process. Public repos can expose submitted URLs and extracted results through Actions logs, artifacts, and Pages output.

## How it works

1. `docs/index.html` is served by GitHub Pages.
2. You paste URLs and a GitHub token into the webpage.
3. The page calls GitHub's workflow dispatch API for `.github/workflows/extract-web.yml`.
4. GitHub Actions runs `stream_extractor_cli.py`.
5. The workflow publishes `docs/results/<job_id>.json` to the `gh-pages` branch.
6. The webpage polls that JSON file and renders the results.

## Deploy the webpage

This package uses branch-based Pages deployment to avoid the `actions/configure-pages` error.

1. Push this repo to GitHub.
2. Go to **Actions → Publish GitHub Pages → Run workflow**.
3. After it finishes, go to **Settings → Pages**.
4. Set:
   - **Source:** Deploy from a branch
   - **Branch:** `gh-pages`
   - **Folder:** `/root`
5. Open your Pages URL.

## Token needed in the webpage

Create a **fine-grained personal access token** for this repo with:

- **Actions:** Read and write
- Repository access: only this repo

The webpage uses the token only in the browser request to GitHub's API. Do not hard-code it into `index.html`.

## Workflows

- `.github/workflows/pages.yml` publishes the static webpage to `gh-pages`.
- `.github/workflows/extract-web.yml` runs extraction and publishes result JSON to `gh-pages`.
- `.github/workflows/extract.yml` is the older issue/manual runner and can be deleted if you only want the web runner.

## Common errors

### `404 workflow not found`

Make sure `.github/workflows/extract-web.yml` is committed to the branch selected in the webpage, usually `main`.

### `401 Bad credentials` or `403 Resource not accessible`

Your token is wrong, expired, or missing **Actions: Read and write** permission.

### Page keeps waiting forever

Open the Actions tab and check the `Web Run Extractor` workflow logs. If it failed, the JSON result file was not published.
