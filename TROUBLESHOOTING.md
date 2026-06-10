# Troubleshooting

## `Get Pages site failed` / `HttpError: Not Found`

This means the repository does not yet have GitHub Pages enabled, or Pages is not configured to use **GitHub Actions**.

### Fast manual fix

1. Open your repository on GitHub.
2. Go to **Settings**.
3. Go to **Pages**.
4. Under **Build and deployment**, set **Source** to **GitHub Actions**.
5. Save if GitHub shows a save button.
6. Go to **Actions → Deploy GitHub Pages → Run workflow**.

### Fully automatic setup

The optional workflow `.github/workflows/enable-pages-once.yml` can enable Pages for you, but GitHub does not allow the default `GITHUB_TOKEN` to do that first-time enablement.

You must create a repository secret named `PAGES_TOKEN` containing a Personal Access Token with permission to administer Pages for this repository. After running **Enable GitHub Pages once**, run **Deploy GitHub Pages** again.

Delete or disable `enable-pages-once.yml` after Pages is enabled if you do not need it anymore.
