# Obsidian2Jekyll

Make your Obsidian articles Jekyll-ready.

This is a python script that scans your obsidian folder, formats your articles to make them compatible with Jekyll's requirements, and saves them to your destination folder, waiting to be published, so you can keep your articles clean, while Jekyll gets its preferred flavor.

This script will do the following things (See [What It Does](#what-it-does) for more details):

1. Adds a frontmatter with `title:` and `layout:`.
2. Prepends dates before file names.
3. Copies associated images to a dedicated folder and updates image links.
4. Updates any Wikilinks to Markdown links.
5. Processes math blocks and inline math (if any).

Enjoy your clean vault and your clean notes. Leave the messy works to Obsidian2Jekyll.

## Quick Start

### Prerequisites

- Python 3.8+

No external packages are needed for this script to run.

### Prepare Your Posts

You don't need to do anything to your post to prepare for this script, although you may want to manually add a frontmatter beforehand if you want to set the date, categories, or other configurations for your post (if no dates are given in the frontmatter, the creation date will be used).

You do, however, need to **create a folder** dedicated to all the posts you wish to publish. The script will look for every `.md` file in the folder and publish them.

Articles outside the dedicated folder will not be visible to the script and will not be processed, so you can still keep your private notes in your vault.

### Run the Script

Clone this repository and `cd` to the folder:

```bash
git clone https://github.com/kckhchen/obsidian-2-jekyll.git
cd obsidian-2-jekyll
```

Open the `config.py` and configure the source paths and destination paths of your posts and images. The configurable variables are listed below:

| Variable       | Description                                            |
| -------------- | ------------------------------------------------------ |
| `VAULT_DIR`    | Path to your Obsidian vault                            |
| `POST_FOLDER`  | Name of your dedicated post folder (inside your vault) |
| `IMG_FOLDER`   | Name of your image folder (inside your vault)          |
| `POST_DIST`    | Path to store your formatted posts                     |
| `IMG_DIST`     | Path to store your images related to your posts        |
| `LAYOUT`       | Layout style for the posts, default to `"post"`        |

Then simply run this command in the folder:

```bash
python3 process_posts.py
```

Then you can find the formatted, Jekyll-ready posts, along with the images in the posts in your destination folder. If you set `POST_DIST` as `./_posts` then the posts can be instantly visible to Jekyll.

(Most of the files inside this repository are for visualizing the demo website. You can safely delete most of the files and keep only the `.py` scripts.)

### (Optional) GitHub Actions Integration

You can also easily assign a GitHub Action to automatically parse the articles for you every time you push a new `.md` to the repository.

## Live Demo

This repository comes with a demo website. Please visit [here](https://kckhchen.com/obsidian-2-jekyll/blog) to see the presentation on a Jekyll website, which includes most of the situations that will be handled by this script. Additionally, you can have a look inside the `examples/` folder for the raw Obsidian `.md` article, and you can find the processed version in the `_posts/` folder.

[[a screenshot placeholder]]

## What It Does

The script automatically does the following things to your posts:

### 1. Adds a Frontmatter with `title:` and `layout:`

If the post does not have a frontmatter yet, this script will create one for it. It will also automatically add `layout: post` (or layout format of your choice) to signal Jekyll which format to use. It will also looks for the first `h1`, treats it as the title, and update the `title:` accordingly, after which it will remove the `h1` to prevent duplicate titles.

If no `h1` is present, `title:` won't be added and Jekyll will generate a title based on the file name.

### 2. Prepends Dates Before File Names

If you have set `date:` in the frontmatter, the script will respect your parameter and prepend the date to the (slugged) file name. If no `date:` is given, the script will prepend the **creation date** to the file name to meet Jekyll's requirements.

If the file has `yyyy-mm-dd` in its file name, it will be removed, and the new date will be prepended.

For example, a `.md` file named `My New Note.md` will be renamed to `yyyy-mm-dd-my-new-note.md`.

> [!NOTE]
> This script **removes the destination folders and re-creates them** every time it is run. This can ensure posts removed from your publication folder will no longer be present in the destination folder, and any updates to the contents, file names, and frontmatters will be updated accordingly.

### 3. Copies Associated Images to a Dedicated Folder And Updates Image Links

Image links `![[img.png|optional-width]]`, given that the actual images exist in the image folder, will be transformed to `![](IMG_DIST/img.png){: width="optional-width" }`. If no width parameter is given, only the image link is returned.

Also, all images associated with any of the processed posts will be copied to the dedicated image folder, while other irrelevant images will not be copied. This keeps your publication folder clean and tidy.

> [!NOTE]
> This script change image Wikilinks to links from the **root folder** (i.e. it strips away the leading `.` in the path). Please make sure the path to the image folder starts from the root to prevent Jekyll from missing it.

### 4. Updates Any Wikilinks to Markdown Links

The script looks for anything in the form of `[[url|Displayed Text]]` and changes them to Markdown links `[Displayed Text](url)`. Displayed texts are optional.

It works with links to other posts `[[another-post]]`, header links `[[#some-h2-title]]`, block/section links `[[#^link-to-block]]`, and headers and blocks from other posts `[[another-post#some-h3-title]]`.

However, please note that the script transforms links to other posts to `[Displayed Text](../another-post)`, i.e. it assumes the posts are in the same root folder. Please revise the permalink to `/:title/` to ensure this feature works.

> [!NOTE]
> Section and block links are automatically prepended with a `secid` (e.g., `#^1e2t3` becomes `#secid1e2t3`) to ensure compatibility with HTML standards, which do not allow IDs to start with a number.

### 5. Process Math Blocks and Inline Math

It processes math blocks while protecting code blocks, ensuring that dollar signs in scripts or code aren't accidentally converted to LaTeX.

The script will look for any `$...$` and `$$...$$` *outside code blocks* and transform them into `\(...\)` and `\[...\]`.

Since Obsidian requires math environments `\begin{...} \end{...}` be enclosed within `$$...$$` while Jekyll strictly forbids it, this will also be treated. Specifically, linebreaks (double-backslashes) in multi-line math blocks will be transformed to **eight backslashes** so the html can be rendered correctly.

If the post contains math blocks, the script will automatically insert `{% include mathjax.html %}` at the end of the post, so that any Jekyll theme supported will be able to render the math. If the Jekyll does not support math mode natively, you can always create a `mathjax.html` snippet inside the `_includes/` folder. Please refer to the folder for details on the snippet.

> [!NOTE]
> If you wish to use the dollar sign `$` normally outside code blocks, please escape it with a backslash so that the script won't treat it as math blocks.

