set size ratio -1
set xrange [-6:6]
set yrange [-0:6]
set xlabel "x (m)"
set ylabel "z (m)"
set nokey 

x=1
plot "circle.txt" using (0):(0):(6):1:2 with circles 
replot "circle2.txt" using (0):(0):(6):1:2 with circles lc rgb "red"

replot "/media/ubuntu/dnn/ridar/bb/far/o/center/1.txt" using ($2*cos((($1/2)-45)*pi/180)):($2*sin((($1/2)-45)*pi/180)) with points pt 7 
replot "/media/ubuntu/dnn/ridar/bb/far/o/center/1a.txt" using ($2*cos((($1/2)-45)*pi/180)):($2*sin((($1/2)-45)*pi/180)) with points pt 7 lc rgb "red"
set terminal eps
set output '1.eps'
replot
set terminal x11
set output
