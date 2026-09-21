# Robotics Lab at IIT — preserved static website

This is a faithful static preservation of https://robots.iit.edu/, captured on 2026-09-21. The public site is the source of truth. Its text, page names, layout, colors, fonts, images, and slideshows are retained. The original live website and its DNS settings remain unchanged. A separate GitHub Pages test deployment is configured below.

## Preview locally

With Python 3 installed, open PowerShell and run:

```powershell
Set-Location -LiteralPath 'C:\Users\mspen\OneDrive\Documents\Webpage Migration\robots-iit'
python -m http.server 8000 --bind 127.0.0.1
```

Open http://127.0.0.1:8000/ in your browser. Press Ctrl+C to stop the server. Use an HTTP server, not double-clicked HTML files: existing root-relative URLs intentionally remain root-relative.

## Structure

- `index.html` and the other 15 root HTML files: original public pages; `/` and `/index.html` both work.
- `uploads/2/5/7/1/25715664/`: original image, PDF, and ZIP paths, including full-size slideshow pictures.
- `files/main_style.css`, `files/theme/`: preserved original theme and its local assets.
- `assets/vendor/`: locally hosted CDN styles, fonts, images, jQuery, and slideshow library. Domain names in directory names record provenance; they do not make network requests.
- `files/static.js` and `files/static.css`: small compatibility layer for desktop dropdowns and slideshow thumbnail events.
- `robots.txt`, `sitemap.xml`: captured public discovery files.
- `.nojekyll`: serves the site without Jekyll processing.
- `CNAME`: prepared with `robots.iit.edu` for eventual branch-based GitHub Pages hosting. The local file changes no DNS or live hosting.
- `_migration/`: exact downloaded source files, URL/hash inventory, reference graph, removed-script log, validation results, and screenshots. Excluded from Git by `.gitignore`; do not publish this archival directory because its original HTML still references live services.
- `tools/validate.py`: repeatable offline link and asset checker using only Python's standard library.
- `MIGRATION_REPORT.md`: counts, scope, changes, dependencies, and limitations.

## Validate

```powershell
python tools/validate.py
```

The command checks HTML links, CSS URLs/imports, fragment targets, and declared slideshow images. It writes `_migration/link-check.json` and exits nonzero if a local file or fragment is missing. Browser testing during migration additionally checked rendered images, dynamic requests, JavaScript errors, and mobile/desktop navigation.

## GitHub Pages test deployment

Repository: https://github.com/mspenko/robots-iit

Preview URL: https://mspenko.github.io/robots-iit/

The GitHub Actions workflow `.github/workflows/pages.yml` validates the source, builds a deployment artifact with the repository base path, and deploys to GitHub Pages on pushes to `main`. The original HTML/CSS/image paths in this source remain unchanged. `tools/build_pages.py` adjusts root-relative page, stylesheet, image, font, and slideshow URLs only in the generated artifact.

Only HTML and the `uploads`, `files`, and `assets` directories are published, with generated `.nojekyll` and robots.txt files. Archives, documentation, tools, Git metadata, and `CNAME` are excluded. The test site has `noindex, nofollow` metadata and a robots.txt crawl restriction. No custom domain is configured for this test, and robots.iit.edu continues to use its existing host.

To build a local preview of the project path into a fresh directory:

```powershell
python tools/build_pages.py --base-path /robots-iit --output _site/robots-iit
python -m http.server 8000 --bind 127.0.0.1 --directory _site
```

Open http://127.0.0.1:8000/robots-iit/. The builder requires an empty output directory to avoid stale artifacts; choose a new output location for subsequent builds. `_site/` is ignored by Git. Ordinary root preview still works using the instructions above.

## Eventual custom-domain cutover

The preserved `CNAME` file documents the intended domain but is omitted from the test artifact. For a future cutover, verify domain ownership in GitHub, configure `robots.iit.edu` in repository Settings → Pages, and coordinate with IIT's DNS administrator to point the `robots` CNAME to `mspenko.github.io`. Then enable HTTPS when available. No DNS change is part of the test deployment.

The workflow uses the base path reported by GitHub, so it will build for the domain root once the custom domain is configured. At cutover, add `--production` to the build command to restore the preserved sitemap/robots.txt and remove test-only noindex metadata. Test the custom-domain deployment before retiring Weebly.

Official instructions: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site

## Editing

Edit the preserved HTML and local CSS directly; no Node, npm, build system, or Weebly subscription is needed to serve the static copy. Retain existing filenames, including the source spelling `agility-and-manueverability.html`, to preserve incoming links. Keep the archive as a baseline before redesigning. Original third-party copyright/license notices remain in vendor files.
