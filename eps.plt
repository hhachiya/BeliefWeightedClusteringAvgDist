set size ratio -1
set xrange [-7:7]
set yrange [-6:7]
set xlabel "x (m)"
set ylabel "z (m)"
set nokey

x=1
plot "circle.txt" using (0):(0):(7):1:2 with circles lc rgb "black"
replot "circle2.txt" using (0):(0):(7):1:2 with circles lc rgb "blue"


replot "ridar/row/near/o/center/row-1.txt" using ($2*cos((($1/2)-45)*pi/180)):($2*sin((($1/2)-45)*pi/180)) with points pt 7 ps 0.5 lc rgb "black"
replot "ridar/bb/near/o/center/1.txt" using ($2*cos((($1/2)-45)*pi/180)):($2*sin((($1/2)-45)*pi/180)) with points pt 7 ps 1 lc rgb "grey"
#replot "ridar/bb/near/o/center/1a.txt" using ($2*cos((($1/2)-45)*pi/180)):($2*sin((($1/2)-45)*pi/180)) with points pt 7 ps 1 lc rgb "blue"

set terminal eps
set output 'laser_example.eps'
replot
set terminal x11
set output