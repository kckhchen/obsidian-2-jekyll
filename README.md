# Obsidian2Jekyll

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)

Make your Obsidian articles Jekyll-ready.

This is a tool build with python that scans your obsidian folder, formats your articles to make them compatible with Jekyll's requirements, and saves them to your destination folder, waiting to be published, so you can keep your articles clean, while Jekyll gets its preferred flavor.

## Features

- Auto-generates frontmatters with all the essentials.
- Converts your `h1` header to your post title.
- Copies used images to Jekyll assets folder and update `![[img]]` links.
- Converts `[[Wikilinks]]` to standard Markdown links.
- Math / Code / Callout / Internal-link supports (Auto-installs callout CSS/HTML).

## Live Demo

| Original Obsidian Article | Processed Jekyll Site |
| :---: | :---: |
| <img src="./assets/images/obsidian-demo.gif" width="400"> | <img src="./assets/images/jekyll-demo.gif" width="400"> |

  <p style="text-align: center">
    <a href="https://kckhchen.com/obsidian-2-jekyll-demo/my-main-post/"><b>Read the Blog Post</b></a>
  </p>

## Quick Start

### Prerequisites

- Python 3.8+
- The `python-frontmatter` package. You can install it with:

```
pip install python-frontmatter
```

### Run the Tool

#### 1. Clone this repo:

```bash
git clone https://github.com/kckhchen/obsidian-2-jekyll.git
cd obsidian-2-jekyll
```

#### 2. Configure `config.py` to locate your vault:


| Variable              | Description                                 | Example                      |
| --------------------- | ------------------------------------------- | ---------------------------- |
| `SOURCE_DIR`          | A folder in your vault for publication      | `/Users/me/Obsidian/Publish` |
| `JEKYLL_DIR`          | Your Jekyll project folder                  | `/Users/me/Jekyll`           |
| `IMG_DEST`            | Image folder in your Jekyll project folder  | `assets/images`              |

```python
# config.py
SOURCE_DIR = "/Users/me/Obsidian/Publish"  # Path to Your Post Folder
JEKYLL_DIR = "/Users/me/Jekyll"            # Your Site
IMG_DEST   = "assets/images"               # Relative to Jekyll Root
```

#### 3. Run the command

```bash
# Process new posts
python3 main.py

# Process and clean up deleted posts
python3 main.py --update
```

## User Guide

You can find the full User Guide and Advanced Settings [here](./assets/docs/GUIDE.md).
