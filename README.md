# Markdown Portfolio

A small educational website created in July 2020 as part of GitHub Learning Lab's **Communicating Using Markdown** course. It demonstrates common Markdown features using **Jekyll** and the **Cayman** theme, and is published with **GitHub Pages**.

**Live website:** https://ovidiudeica.github.io/markdown-portfolio/

## Markdown examples

The site preserves the original learning exercises:

- Heading levels (`h1`, `h2`, and `h6`).
- An externally hosted GitHub Octodex image.
- A link to a GitHub profile.
- Emoji shortcode examples and a Markdown table.
- Ordered and unordered lists, including nested items.
- Italic, bold, and combined text emphasis.

## Repository structure

| File or directory | Purpose |
| --- | --- |
| `index.md` | Assembles the learning examples into the homepage |
| `_includes/01-name.md` | Heading examples |
| `_includes/02-image.md` | Image example |
| `_includes/03-links.md` | Link example |
| `_includes/04-lists.md` | Emoji table and list examples |
| `_includes/05-emphasis.md` | Text-formatting examples |
| `_config.yml` | Jekyll/Cayman theme settings and page-preview metadata |
| `assets/images/og-preview.png` | GitHub Pages / LinkedIn link-preview image |
| `communicating-using-markdown.pdf` | Original learning material |

## Publishing

Jekyll generates the Cayman-themed site from the committed direct dependencies.
The homepage still includes the five historical examples from `_includes/`.
Do not change the original learning content merely to update link-preview metadata.


## Publishing through GitHub Actions (since 28 October 2026)

This site uses **Settings → Pages → Source: GitHub Actions**, not branch-based Pages Jekyll builds.
The `github-pages` environment permits deployments only from the protected `master`
branch; administrative bypass of environment protection was disabled during the cutover.
Deployment is **manual only**, never automatic on `push` or pull requests.

1. Open [Container-free Pages workflow](https://github.com/ovidiudeica/markdown-portfolio/actions/workflows/pages-migration-preview.yml).
2. Choose **Run workflow**, select `master`, enable
   **Confirm Settings > Pages > Source is GitHub Actions**, then run **once**.
3. Check that both the `preview` (Jekyll build and vulnerability audit) and
   `deploy` jobs complete successfully. Do not mistake green Dependabot PR
   previews for production deployments.
4. Check the live site, canonical and Open Graph metadata, original content and assets.
   The branch's required CI must pass before deployment. The deployment job uses
   `actions/deploy-pages`; the build uses the committed `Gemfile.lock`, not
   GitHub's managed `jekyll-build-pages` container.

**Emergency rollback:** stop manual deployment; if publication is broken, switch
**Settings → Pages → Build and deployment → Source** back to
**Deploy from a branch → master → /(root)**. This restores the old path but
**reintroduces the provider-managed Jekyll image risk**: re-open
[the tracked security issue](https://github.com/ovidiudeica/myfirstslideshow/issues/32)
and reinstate the Actions workflow once repaired. Rollback never requires
force-pushing or disabling branch protection.

## Origin and license

This repository started as a GitHub Learning Lab learning exercise. Its original Markdown examples and accompanying PDF remain intact.

See [LICENSE](LICENSE) for the MIT license and original GitHub, Inc. attribution.
