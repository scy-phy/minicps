let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/scy-phy/minicps/docs
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +104 conf.py
badd +16 index.rst
badd +24 api.rst
badd +16 tests.rst
badd +1 misc.rst
badd +6 ~/mopidy/docs/authors.rst
badd +64 ~/mopidy/docs/codestyle.rst
badd +83 ~/mopidy/docs/conf.py
badd +5 ~/mopidy/docs/versioning.rst
badd +57 ~/mopidy/docs/api/index.rst
badd +7 ~/mopidy/docs/api/architecture.rst
badd +6 ~/mopidy/docs/modules/index.rst
badd +6 ~/mopidy/docs/changelog.rst
badd +10 NetrwTreeListing\ 2
badd +3 ~/mopidy/docs/glossary.rst
badd +15 ~/scy-phy/minicps/README.md
badd +87 swat-tutorial.rst
badd +198 userguide.rst
badd +1 ~/.vim/UltiSnips/rst.snippets
badd +189 ~/.vim/bundle/vim-snippets/UltiSnips/rst.snippets
badd +842 ~/.vimrc
argglobal
silent! argdel *
argadd conf.py
argadd index.rst
argadd api.rst
edit misc.rst
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 54 + 95) / 190)
exe 'vert 2resize ' . ((&columns * 135 + 95) / 190)
argglobal
edit misc.rst
setlocal fdm=marker
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 17 - ((16 * winheight(0) + 27) / 54)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
17
normal! 0
wincmd w
argglobal
edit swat-tutorial.rst
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=0
setlocal fml=1
setlocal fdn=20
setlocal fen
let s:l = 82 - ((26 * winheight(0) + 27) / 54)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
82
normal! 0
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 54 + 95) / 190)
exe 'vert 2resize ' . ((&columns * 135 + 95) / 190)
tabnext 1
if exists('s:wipebuf')
  silent exe 'bwipe ' . s:wipebuf
endif
unlet! s:wipebuf
set winheight=1 winwidth=1 shortmess=filnxtToO
let s:sx = expand("<sfile>:p:r")."x.vim"
if file_readable(s:sx)
  exe "source " . fnameescape(s:sx)
endif
let &so = s:so_save | let &siso = s:siso_save
doautoall SessionLoadPost
unlet SessionLoad
" vim: set ft=vim :
