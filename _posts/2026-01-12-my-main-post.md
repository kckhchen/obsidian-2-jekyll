---
layout: post
title: Main Title
---

This is a demo website for my tool [Obsidian-2-Jekyll](https://github.com/kckhchen/obsidian-2-jekyll).

The file name will be `2026-01-12-my-main-post`, since the original file name is `My Main Post` and the creation date is 12th January, 2026. The `h1` title "This Should Be the Main Title" will be treated as post title on the website, and the header will be removed.

## Math Processing

Any math section like a simple \\(a^2 + b^{2} = c^{2}\\) will be rendered correctly, including math blocks:
{: #secid10d1e3}


$$
\mathbb{E}\left[ \bar{X} \right] = \mathbb{E}\left[ \frac{1}{n} \sum_{i=1}^{n} X_{i} \right] = \frac{1}{n} \mathbb{E}\left[ \sum_{i=1}^{n} X_{i} \right] = \frac{1}{n} \sum_{i=1}^{n} \mathbb{E} \left[ X_{1} \right] = \frac{1}{n} n\mu = \mu
$$

{: #secid0f5bab}

This also works with multi-line and math block with environments:


$$
\begin{align}
\mathbb{E} \left[ \frac{1}{n} \sum_{i=1}^{n} (X_{i} - \bar{X})^{2} \right]
&= \frac{1}{n} \mathbb{E} \left[ \sum_{i=1}^{n} X_{i}^{2} - n\bar{X}^{2} \right] \\
&= \frac{1}{n} \left( \sum_{i=1}^{n} \mathbb{E} \left[ X_{i}^{2} \right] - n\mathbb{E} \left[ \bar{X}^{2} \right] \right) \\
&= \frac{1}{n}\left( n(\sigma^{2} + \mu^{2}) - n \left( \frac{\sigma^{2}}{n} + \mu^{2} \right) \right) \\
&= \sigma^{2} + \mu^{2} - \frac{\sigma^{2}}{n} - \mu^{2} \\
&= \frac{n-1}{n} \sigma^{2}
\end{align}
$$

{: #secid2d1a9f}

### A Note on Code Shields

Inline code with \$'s, such as `$a fake math block$` and code blocks with \$ will remain intact:

```
$ echo "This block"
$ echo "will be safe from math detector."

$$
A math block inside a code block.
$$
```
{: #secid2863db}

Wikilinks also won't be affected when inside code blocks.
```
A [[Wikilink inside a code block]] will not be processed.
An ![[image-link-inside-code-block.img]] will not be processed.
```


If you have dollar signs \$ (e.g. The apple costs 10\$ and the banana costs 5\$), please escape them with \\ so that they won't get mistaken as math environments.

### Image Links and Wikilinks

Wikilinks to [Another Post](../my-another-post) will be transformed into Markdown link, with the link replaced to a url (`../another-post`). 

Image links such as

![](./obsidian-2-jekyll/assets/images/random-image-abc.gif){: width="500" }

will be rendered to be compatible with Jekyll, along with the specified `width` (if provided).

The `.md` files found in the `_posts` folder might look broken and won't be rendered by most Markdown editors correctly, but they are compatible with Jekyll's requirements.

### Some Links to Sections/Blocks

[This links back to the header "Math Processing"](#math-processing)

[Block link to a paragraph in this post](#secid10d1e3)

[Block link to a code block in this post](#secid2863db)

[Block link to a math block in this post](#secid0f5bab)

[Block link to a math block with a math environment in this post](#secid2d1a9f)
### Links to Other Posts

[Block link to a paragraph in another post](../my-another-post#secidf07645)

[This points to a section in another post.](../my-another-post#amazing-h2-title)

## Callouts

<div class="callout callout-info" markdown="1">
<div class="callout-title">Info</div>
If a callout does not have a title, the callout type will be the title.

</div>

<div class="callout callout-warning" markdown="1">
<div class="callout-title">Callout Title (Warning callout)</div>
Optionally, a callout can have a title.

</div>

<div class="callout callout-quote" markdown="1">
<div class="callout-title">A Quote Callout</div>

</div>

<div class="callout callout-error" markdown="1">
<div class="callout-title">An Error Callout</div>
Just like the callout above, a callout can have no messages.

</div>

<div class="callout callout-hint" markdown="1">
<div class="callout-title">A Hint Callout</div>
Just another callout

</div>

<div class="callout callout-example" markdown="1">
<details>
    <summary class="callout-title">A Foldable Callout</summary>
    Just like how you use it in Obsidian, a callout type followed be a +/- sign will make the callout foldable.

</details>
</div>

<div class="callout callout-success" markdown="1">
<details open>
    <summary class="callout-title">A foldable callout but default open</summary>
    Callout type followed by a + will make the callout open by default.

</details>
</div>

<div class="callout callout-random" markdown="1">
<div class="callout-title">A not yet support callout</div>
A non-standard callout type or a callout type not yet supported will be in this default style.

</div>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>

{% include obsidian-callouts.html %}