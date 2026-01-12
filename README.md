# Obsidian2Jekyll

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)

Make your Obsidian articles Jekyll-ready.

This is a tool build with python that scans your obsidian folder, formats your articles to make them compatible with Jekyll's requirements, and saves them to your destination folder, waiting to be published, so you can keep your articles clean, while Jekyll gets its preferred flavor.

This tool will do the following things (See "[What It Does](#what-it-does)" for more details):

1. Adds (or appends) a frontmatter with `title:` and `layout:`.
2. Prepends dates before file names.
3. Strips comment blocks `%%...%%` away.
4. Copies associated images to a dedicated folder and updates image links.
5. Updates any Wikilinks to Markdown links.
6. Processes inline math (if any).
7. Shields code blocks from all the operations above.

## Quick Start

### Prerequisites

- Python 3.8+
- `python-frontmatter` package. You can install with:

```
pip install python-frontmatter
```

### Prepare Your Posts

You don't need to do anything to your post to prepare for this tool, although you may want to manually add a frontmatter beforehand if you want to set the dates, categories, permalinks, or other configurations for your post. If you don't need any configurations, your posts are good to go as-is.

Although the tool will set up `title`, `math`, `layout`, etc. for your post in the frontmatter, you can also set them up yourself and the tool will respect your configurations. It will also not alter your existing configurations such as `slug` or `permalink`.

In short, just write normally. Use `h1` as the main title, use code blocks, math blocks, inline math, comments, etc. Don't worry about the frontmatter and the file name.

### Prepare Your Folder

You need to create (or assign) a **publication folder dedicated to all the posts you wish to publish**. The tool will look for every `.md` file in the folder and publish them.

Articles outside the dedicated folder will not be processed, so you can still keep your private notes in your vault, and drag them into the publication folder when they are ready.

### Run the tool

Clone this repository and `cd` to the folder:

```bash
git clone https://github.com/kckhchen/obsidian-2-jekyll.git
cd obsidian-2-jekyll
```

Open the `config.py` and set the source paths and destination paths of your posts and images. All configurable variables are listed below:

| Variable              | Description                                            |
| --------------------- | ------------------------------------------------------ |
| `SOURCE_DIR`          | Path to your dedicated post folder (inside your vault's root folder, not nested) |
| `POST_DEST`           | Path to the folder to store your formatted posts       |
| `IMG_DEST`            | Path to the folder to store associated images          |
| `IMG_LINK`            | **Absolute link** to your image folder for the website |
| `MATH_RENDERING_MODE` | Choose from `metadata` and `inject_cdn`. See [below](#5-process-inline-math)    |

Then simply run this command in the folder:

```bash
python3 main.py
```

Then you can find the formatted, Jekyll-ready posts, along with the images in the posts in your destination folder. If you set `POST_DEST` as `./_posts` and place the folder at the root of your Jekyll page directory, then the posts can be readily visible to Jekyll.

### Clean Up Stale Files

The tool implements incremental builds and does not clean up outdated files in the destination folder by default. That means if you delete a post or remove a post from your publication folder, the destination folder will not reflect the removal.

However, you can use the `-c` or `--cleanup` flag to make the tool remove any stale files:
```
python3 main.py --cleanup
```
This will, after asking for your confirmation, remove all the `.md` files in the destination folder whose corresponding file is not in the publication folder. It will also remove outdated posts (i.e., if you manually add a new `date` in the frontmatter or somehow change the creation date of your post).

If you'd like to process new files *and* clean up stale files at the same time, you can use the `-u` or `--update` flag:
```
python3 main.py --update
```
This is effectively the same as:
```
python3 main.py
python3 main.py --cleanup
```

### (Optional) Change Layout Form

This tool set `layout: post` for you in the frontmatter. If you would like you use other layouts you can specify it with the `--layout` flag:

```
python3 main.py --layout page
```

If you don't want to use the flag to change the layout every time, you can add the layout in the frontmatter and the tool will respect your configuration.

### (Optional) Dry Run

You can use the `--dry` flag to do a dry run. The operations will be printed on the screen so you know which files will be altered or processed, but they will not be executed.

```
python3 main.py --dry
```

Dry runs won't be available for `--cleanup` and `--update`, but it will ask for your confirmation before removing files by default.

## Live Demo

This repository comes with a demo website. Please visit [here](https://kckhchen.com/obsidian-2-jekyll/my-main-post/) to see the presentation on a Jekyll website, which includes most of the situations that will be handled by this tool. Additionally, you can have a look inside the `examples/Example-Vault/` folder for the raw Obsidian `.md` article, and you can find the processed version in the `_posts/` folder.

A quick side-by-side comparison between the original Obsidian article and the Jekyll site:

| Original Obsidian Article | Processed Jekyll Site |
| :---: | :---: |
| <img src="./assets/images/obsidian-screenshot.png" width="500"> | <img src="./assets/images/jekyll-screenshot.png" width="500"> |

If you'd like to see more examples, All posts in [my personal blog](https://kckhchen.com/blog/) are processed with this tool *(note: all the posts are in Mandarin Chinese)*.

## What It Does

The tool automatically does the following things to your posts:

### 1. Adds a Frontmatter with `title:` and `layout:`

If the post does not have a frontmatter yet, this tool will create one for it. It will also automatically add `layout: post` (or any layout format of your choice) to signal Jekyll which layout to use. It will also looks for the first `h1`, treats it as the title, and sets the `title:` accordingly in the frontmatter, after which it will remove the `h1` to prevent duplicate titles.

If no `h1` is present, `title:` won't be added and Jekyll will generate a title based on the file name.

### 2. Prepends Dates Before File Names

If you have set `date:` in the frontmatter, the tool will respect your parameter and prepend the date to the (slugged) file name. If no `date:` is given, the tool will prepend the **creation date** (or modification date, when creation dates are not available for some OS) to the file name to meet Jekyll's requirements.

If the file already has `yyyy-mm-dd` prepended to the file name, it will be removed, and the new date will be prepended (if you'd like to specify the date, please add it in the frontmatter).

For example, a `.md` file named `My New Note!.md` will be renamed to `yyyy-mm-dd-my-new-note.md`.

### 3. Copies Associated Images to a Dedicated Folder And Updates Image Links

Image links `![[img.png|optional-width]]`, given that the actual images exist somewhere in the vault, will be transformed to `![](IMG_LINK/img.png){: width="optional-width" }`. If no width parameter is given, only the image link is returned.

Also, all images associated with any of the processed posts will be copied to the dedicated image folder, while other irrelevant images will not be copied. This keeps your destination folder clean and tidy.

> [!NOTE]
> The current cleanup tool has not yet been able to automatically remove stale images when none of the posts in the destination folder are referencing them. This feature will be implemented in future updates.

### 4. Updates Any Wikilinks to Markdown Links

The tool looks for anything in the form of `[[url|optional-displayed-text]]` and changes them to Markdown links `[optional-displayed-text](url)`.

It works with links to other posts `[[another-post]]`, header links `[[#some-h2-title]]`, block/section links `[[#^link-to-block]]`, and headers and blocks from other posts `[[another-post#some-h3-title]]`.

However, please note that the tool transforms links to other posts to `[Displayed Text](../another-post)`, i.e. it assumes the posts are in the same folder.

> [!NOTE]
> Section and block links are automatically prepended with a `secid` (e.g., `#^1e2t3` becomes `#secid1e2t3`) to ensure compatibility with HTML standards, which do not allow id's to start with a number. Don't worry if the id's don't look the same as in the original post.

### 5. Process Inline Math

The tool will look for inline math `$...$` and swap it into `\(...\)` so that most $\LaTeX$ math renderers will render it correctly. Math blocks `$$...$$` will be left as-is.

If the post contains math (be it inline math or math blocks), the tool will do one of the following things, depending on your configuration.

#### If `MATH_RENDERING_MODE = "metadata"`

The tool will add `math: true` to the frontmatter. If the Jekyll theme you use supports math modes then the math will be rendered by whatever renderer the theme chooses.

#### If `MATH_RENDERING_MODE = "inject_cdn"`

The tool will automatically inject a [MathJax](https://www.mathjax.org/) script at the bottom of the post so that the browser will be able to render the math, even if your theme doesn't.

Generally, if your Jekyll theme supports math mode then `metadata` should be preferred. Only use `inject_cdn` when the theme does not support math rendering.

> [!NOTE]
> If you wish to use the dollar sign `$` normally outside code blocks, please escape it with a backslash so that the tool won't treat it as math blocks.

### 6. Shields Code Blocks From All the Operations Above.

All the operations above will ignore code blocks, so that literal dollar signs `$` or Wikilinks `[[]]`, etc. inside code blocks will remain intact.

## To-Do's

This tool is still under development and is actively updated and maintained. Some features to be implemented will be listed here.

- [ ] Parses callouts (e.g., `> [!INFO]`) and renders them correctly.
- [ ] Parse image alt texts.
- [ ] Prevents potential matching of `$` inside tricky areas like url, etc.
- [ ] Auto-removes stale image files.
- [ ] Shields math blocks too.
- [ ] Wikilinks to math blocks might be slightly off (mistakenly referring to the paragraph below instead of the block itself).

Any other suggestions are welcome.