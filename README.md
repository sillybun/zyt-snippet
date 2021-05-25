# zyt-snippet

## LaTeX snippet depends on vimtex
The LaTeX snippet use [vimtex](https://github.com/lervag/vimtex) to tell whether the current consor is in a math environment so you need to install it first.

## helper function
We make helper functions available to multiple snippet files by defining helper functions in a file `pythonx/snippet_helpers.py`.
Note that Vim will load the `snippet_helpers.py` one time only. That means that any changes you make to the helper functions in `snippet_helpers.py` won’t be seen by your snippet files until you reboot Vim.
See [here](http://vimcasts.org/episodes/ultisnips-python-interpolation/) and `:help UltiSnips-globals` for more infomation.

## Development

1. Snippets for math expressions that can be commonly used in markdown and LaTeX are collected into one place `Ultisnips/mathtex.snippets`. Any snippet in this file can be used and will be triggered in markdown and LaTeX files. `tex.snippets` and `markdown.snippets` are for snippets that only works for that filetype.
