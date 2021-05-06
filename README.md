# zyt-snippet

## helper function
We make helper functions available to multiple snippet files by defining helper functions in a file `pythonx/snippet_helpers.py`.
Note that Vim will load the `snippet_helpers.py` one time only. That means that any changes you make to the helper functions in `snippet_helpers.py` won’t be seen by your snippet files until you reboot Vim.
See [here](http://vimcasts.org/episodes/ultisnips-python-interpolation/) and `:help UltiSnips-globals` for more infomation.

