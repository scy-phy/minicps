let SessionLoad = 1
if &cp | set nocp | endif
let s:so_save = &so | let s:siso_save = &siso | set so=0 siso=0
let v:this_session=expand("<sfile>:p")
silent only
cd ~/scy-phy/minicps
if expand('%') == '' && !&modified && line('$') <= 1 && getline(1) == ''
  let s:wipebuf = bufnr('%')
endif
set shortmess=aoO
badd +129 ~/Dropbox/networks/50_012networksexercises/lab6/ics.py
badd +50 minicps/constants.py
badd +1 /tmp/split.bash
badd +29 setup.py
badd +20 tests/constants_tests.py
badd +151 minicps/devices.py
badd +38 tests/devices_tests.py
badd +2 README.md
badd +1 scripts/l3/cpppo_plc1server.sh
badd +22 scripts/attacks/arp-mitm.sh
badd +181 /etc/ettercap/etter.conf
badd +2 logs/minicps.topology.log
badd +12 minicps/links.py
badd +3 scripts/l3/cpppo_client4plc1.sh
badd +2 logs/minicps.constants.log
badd +103 logs/minicps.devices.log
badd +13 scripts/openflow/dpctl-examples.sh
badd +379 ~/pox/pox/forwarding/topo_proactive.py
badd +12 temp/arp-algo.txt
badd +120 scripts/pox/antiarppoison.py
badd +2 scripts/pox/README
badd +330 ~/.vimrc
badd +1 scripts/pox
badd +7 NetrwTreeListing\ 1
badd +5 logs/POXProva.log
badd +68 logs/AntiArpPoison.log
badd +2 logs/POXL2Pairs.log
badd +19 ~/pox/ext/hub.py
badd +265 ~/pox/ext/l2_pairs.py
badd +79 ~/pox/ext/skeleton.py
badd +1 ~/pox/ext/README
badd +132 ~/pox/ext/l2_learning.py
badd +86 scripts/attacks/arp-mitm-l2_learning.txt
badd +3 scripts/attacks/TODO
badd +103 ~/scy-phy/swat/paper-june15/minicps.tex
badd +49 ~/scy-phy/swat/paper-june15/daniele-notes.md
badd +2 scripts/nose.sh
badd +263 ~/pox/pox/forwarding/l3_learning.py
badd +12 scripts/cpppo/server.sh
badd +16 scripts/cpppo/client.sh
badd +99 ~/pox/pox/lib/packet/arp.py
badd +85 ~/pox/pox/lib/packet/ipv4.py
badd +94 ~/pox/pox/lib/packet/ethernet.py
badd +65 ~/pox/pox/lib/packet/tcp.py
badd +418 ~/pox/pox/lib/util.py
badd +39 ~/pox/pox/lib/recoco/events.py
badd +83 ~/pox/ext/timers.py
badd +68 scripts/pox/events.py
badd +954 ~/pox/pox/openflow/of_01.py
badd +51 ~/pox/pox/openflow/__init__.py
badd +181 ~/pox/pox/core.py
badd +491 ~/pox/pox/openflow/libopenflow_01.py
badd +33 ~/pox/pox/openflow/util.py
badd +33 scripts/pox/swat_controller.py
badd +77 logs/POXSwatController.log
badd +150 examples/swat/swat.py
badd +270 examples/swat/constants.py
badd +24 temp/workshop/experiments.py
badd +87 ~/dotfiles/ultisnips/python.snippets
badd +101 minicps/topologies.py
badd +20 tests/topologies_tests.py
badd +25 LICENSE
badd +86 ~/Documents/Dacode/actors.py
badd +37 examples/swat/pox_controller.py
badd +37 examples/swat/daniele-notes.md
badd +87 examples/swat/real-tags/P1-Tags.CSV
badd +196 examples/swat/real-tags/P2-Tags.CSV
badd +7 examples/swat/real-tags/P1-MainProgram-Tags.CSV
badd +59 examples/swat/state_db.py
badd +88 ~/Documents/Dacode/pydb/interact_db.py
badd +5 ~/Documents/Dacode/pydb/schema.sql
badd +20 ~/Documents/Dacode/pydb/create_db.py
badd +45 examples/swat/plc1.py
badd +156 ~/mininet/mininet/log.py
badd +172 examples/swat/real-tags/P3-Tags.CSV
badd +198155 logs/swat.log
badd +240 examples/swat/physical_process.py
badd +1 examples/swat/plc1_cpppo.cache
badd +32 examples/swat/plc2.py
badd +36 examples/swat/plc3.py
badd +216 examples/swat/hmi.py
badd +1 examples/swat/plc2_cpppo.cache
badd +31 examples/swat/ImageContainer.py
badd +109 examples/swat/tutorial.py
badd +32 examples/swat/init_swat.py
badd +70 examples/swat/plc1a.py
badd +61 bin/init
badd +2 bin/swat-tutorial
argglobal
silent! argdel *
edit examples/swat/plc1.py
set splitbelow splitright
wincmd _ | wincmd |
vsplit
1wincmd h
wincmd w
set nosplitbelow
set nosplitright
wincmd t
set winheight=1 winwidth=1
exe 'vert 1resize ' . ((&columns * 40 + 95) / 190)
exe 'vert 2resize ' . ((&columns * 149 + 95) / 190)
argglobal
enew
file __Tag_List__
setlocal fdm=manual
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=#
setlocal fdl=9999
setlocal fml=0
setlocal fdn=20
setlocal fen
wincmd w
argglobal
setlocal fdm=indent
setlocal fde=0
setlocal fmr={{{,}}}
setlocal fdi=''
setlocal fdl=4
setlocal fml=1
setlocal fdn=20
setlocal fen
15
normal! zo
51
normal! zo
let s:l = 43 - ((26 * winheight(0) + 27) / 54)
if s:l < 1 | let s:l = 1 | endif
exe s:l
normal! zt
43
normal! 037|
wincmd w
2wincmd w
exe 'vert 1resize ' . ((&columns * 40 + 95) / 190)
exe 'vert 2resize ' . ((&columns * 149 + 95) / 190)
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
