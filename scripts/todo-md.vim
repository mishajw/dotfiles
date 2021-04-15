" Colors for nicer todo.md files.

highlight TodoGreenHighlight   ctermbg=2    ctermfg=black  cterm=italic,bold,underline
highlight TodoYellow           ctermbg=226  ctermfg=black
highlight TodoOrangeHighlight  ctermbg=11   ctermfg=white  cterm=italic,bold,underline
highlight TodoOrange           ctermbg=11   ctermfg=white
highlight TodoRed              ctermbg=1    ctermfg=white
highlight TodoLightRed         ctermbg=9    ctermfg=black
highlight TodoBlue             ctermbg=4    ctermfg=white
highlight TodoPurple           ctermbg=13   ctermfg=white
highlight TodoFade             ctermfg=243

function SetupTodo()
  call matchadd('TodoGreenHighlight',   '#todo\>')
  call matchadd('TodoOrangeHighlight',  '#onit\>')
  call matchadd('TodoOrange',           '#redy\>')
  call matchadd('TodoYellow',           '#revw\>')
  call matchadd('TodoFade',             '#done\>.*')
  call matchadd('TodoRed',              '#blkr\>')
  call matchadd('TodoLightRed',         '#blkd\>')
  call matchadd('TodoPurple',           '#qstn\>')
  call matchadd('TodoPurple',           '#idea\>')
  call matchadd('TodoBlue',             '#clup\>')

  call matchadd('TodoYellow',           '\[.*\]$')
  call matchadd('TodoOrange',           '\[today\]$')
  call matchadd('TodoRed',              '\[now\]$')

  set colorcolumn=60
  set textwidth=60
endfunction

au BufRead,BufNewFile *todo.md call SetupTodo()
