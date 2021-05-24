# zyt-snippet

## LaTeX snippet depends on vimtex
The LaTeX snippet use [vimtex](https://github.com/lervag/vimtex) to tell whether the current consor is in a math environment so you need to install it first.

## helper function
We make helper functions available to multiple snippet files by defining helper functions in a file `pythonx/snippet_helpers.py`.
Note that Vim will load the `snippet_helpers.py` one time only. That means that any changes you make to the helper functions in `snippet_helpers.py` won’t be seen by your snippet files until you reboot Vim.
See [here](http://vimcasts.org/episodes/ultisnips-python-interpolation/) and `:help UltiSnips-globals` for more infomation.
