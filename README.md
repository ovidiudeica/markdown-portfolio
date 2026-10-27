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

GitHub Pages builds the site with Jekyll using the Cayman theme specified in `_config.yml`. The homepage includes the five example files from `_includes/`. Changes to the original learning content are not required for the Open Graph link preview.

## Origin and license

This repository started as a GitHub Learning Lab learning exercise. Its original Markdown examples and accompanying PDF remain intact.

See [LICENSE](LICENSE) for the MIT license and original GitHub, Inc. attribution.
