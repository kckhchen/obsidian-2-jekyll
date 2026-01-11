---
title: This Should Be the Main Title
layout: post
---

The date will be the file creation date. This file was created on 11th January, 2026.

## Math Processing

Any math section like a simple \\(a^2 + b^{2} = c^{2}\\) will be rendered correctly, including math blocks:


\\[
\mathbb{E}\left[ \bar{X} \right] = \mathbb{E}\left[ \frac{1}{n} \sum_{i=1}^{n} X_{i} \right] = \frac{1}{n} \mathbb{E}\left[ \sum_{i=1}^{n} X_{i} \right] = \frac{1}{n} \sum_{i=1}^{n} \mathbb{E} \left[ X_{1} \right] = \frac{1}{n} n\mu = \mu
\\]


This also works with multi-linen and math block with environments:


\begin{align}
\mathbb{E} \left[ \frac{1}{n} \sum_{i=1}^{n} (X_{i} - \bar{X})^{2} \right]
&= \frac{1}{n} \mathbb{E} \left[ \sum_{i=1}^{n} X_{i}^{2} - n\bar{X}^{2} \right]  \\\\\\\\
&= \frac{1}{n} \left( \sum_{i=1}^{n} \mathbb{E} \left[ X_{i}^{2} \right]  - n\mathbb{E} \left[ \bar{X}^{2} \right]  \right) \\\\\\\\
&= \frac{1}{n}\left( n(\sigma^{2} + \mu^{2}) - n \left( \frac{\sigma^{2}}{n} + \mu^{2} \right)  \right) \\\\\\\\
&= \sigma^{2} + \mu^{2} - \frac{\sigma^{2}}{n} - \mu^{2} \\\\\\\\
&= \frac{n-1}{n} \sigma^{2}
\end{align}


### A Note on Code Blocks

The line breaks inside the math block will be changed to exactly eight "\\"s.

Inline code with \$'s, such as `$a fake math block$` and code blocks with \$ will remain intact:

```
$ echo "This block"
$ echo "will be safe from math detector."
```
^aa46c7

If you have dollar signs \$ (e.g. The apple costs 10\$ and the banana costs 5\$), please escape them with \\ so that they won't get mistaken as math environments.

Wikilinks to [a-fake-link](../another-post/) will be transformed into Markdown link, with the link replaced to a url (`../anoter-post`). Image Wikilinks like

![](/assets/images/random-image-abc.gif){: width="500" }

will be rendered to be compatible with Jekyll, along with the specified `width`.

This post might look broken on normal `md` editors, but the format

[This points back to Math Processing.](#math-processing)

[This points to a section in another post.](../another-post#math-processing)

[#^aa46c7](#^aa46c7)

{% include mathjax.html %}