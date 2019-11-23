function! snip_util#RefreshLineNumber() abort
if has("python3")
python3 << EOF
import vim
b = vim.current.buffer
for index, line in enumerate(b):
    ob = re.fullmatch(r"(\s*print\(\"line \[)(\d+)(\] .*)", line)
    if ob:
        b[index] = ob.group(1) + str(index+1) + ob.group(3)
EOF
endif
endfunction
