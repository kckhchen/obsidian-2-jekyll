---
title: This Should Be the Main Title
layout: post
---

The file name will be `2026-01-11-my-main-post`, since the original file name is `My Main Post` and the creation date is 11th January, 2026. The `h1` header "This Should Be the Main Title" will be treated as post title on the website, and the header will be removed.
## Math Processing

Any math section like a simple \\(a^2 + b^{2} = c^{2}\\) will be rendered correctly, including math blocks:
{: #secid10d1e3}

\\[
\mathbb{E}\left[ \bar{X} \right] = \mathbb{E}\left[ \frac{1}{n} \sum_{i=1}^{n} X_{i} \right] = \frac{1}{n} \mathbb{E}\left[ \sum_{i=1}^{n} X_{i} \right] = \frac{1}{n} \sum_{i=1}^{n} \mathbb{E} \left[ X_{1} \right] = \frac{1}{n} n\mu = \mu
\\]
{: #secid0f5bab}

This also works with multi-linen and math block with environments:

\begin{align}
\mathbb{E} \left[ \frac{1}{n} \sum_{i=1}^{n} (X_{i} - \bar{X})^{2} \right]
&= \frac{1}{n} \mathbb{E} \left[ \sum_{i=1}^{n} X_{i}^{2} - n\bar{X}^{2} \right] \\\\\\\\
&= \frac{1}{n} \left( \sum_{i=1}^{n} \mathbb{E} \left[ X_{i}^{2} \right] - n\mathbb{E} \left[ \bar{X}^{2} \right] \right) \\\\\\\\
&= \frac{1}{n}\left( n(\sigma^{2} + \mu^{2}) - n \left( \frac{\sigma^{2}}{n} + \mu^{2} \right) \right) \\\\\\\\
&= \sigma^{2} + \mu^{2} - \frac{\sigma^{2}}{n} - \mu^{2} \\\\\\\\
&= \frac{n-1}{n} \sigma^{2}
\end{align}
{: #secid2d1a9f}

### A Note on Code Blocks

The line breaks inside the math block will be changed to exactly eight "\\"s.

Inline code with \$'s, such as `$a fake math block$` and code blocks with \$ will remain intact:

```
$ echo "This block"
$ echo "will be safe from math detector."
```
{: #secid2863db}


If you have dollar signs \$ (e.g. The apple costs 10\$ and the banana costs 5\$), please escape them with \\ so that they won't get mistaken as math environments.

### Image Links and Wikilinks

Wikilinks to [Another Post](../my-another-post) will be transformed into Markdown link, with the link replaced to a url (`../another-post`). 

Image links such as

![](/assets/images/random-image-abc.gif){: width="500" }

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

{% include mathjax.html %}