# Fix for `actions/configure-pages@v5` Not Found

This package no longer uses `actions/configure-pages@v5`, so the error below will stop:

```text
Get Pages site failed. Please verify that the repository has Pages enabled and configured to build using GitHub Actions
```

## What changed

`.github/workflows/pages.yml` now publishes the static `docs/` folder to a `gh-pages` branch using `peaceiris/actions-gh-pages@v4`.

## Steps

1. Replace your old `.github/workflows/pages.yml` with the new one.
2. Commit and push to `main`.
3. Open **Actions → Publish GitHub Pages → Run workflow**.
4. After the run creates the `gh-pages` branch, open **Settings → Pages**.
5. Set:
   - **Source:** Deploy from a branch
   - **Branch:** `gh-pages`
   - **Folder:** `/root`
6. Save.

Your site will be available at:

```text
https://YOUR_USERNAME.github.io/YOUR_REPOSITORY/
```

## Important

If GitHub says `gh-pages` branch is not found, run the workflow once first. The workflow creates that branch.
