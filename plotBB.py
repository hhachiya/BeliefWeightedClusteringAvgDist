# -*- coding: utf-8 -*-

import matplotlib.pylab as plt
from PIL import Image
import matplotlib.patches as patches
import numpy as np

import pdb


imgPath = "data/img/near/o/center/img-1.png"
bbPath = "data/bb/near/o/center/rcnn-1.txt"

# データ読み込み
#im = Image.open(imgPath)
im = plt.imread(imgPath)
with open(bbPath,"rt") as fp:
	bb = fp.readline().split(' ')
	
bb = np.array(bb[:4]).astype(np.float)

# プロット
fig = plt.figure()
ax = plt.axes()

# 画像
plt.imshow(im)

# BB
r = patches.Rectangle(xy=(bb[0], bb[1]), width=bb[2]-bb[0], height=bb[3]-bb[1], ec='orange', fill=False, linewidth=3.5)
ax.add_patch(r)

ax.text(bb[0]-10, (bb[3]-bb[1])/2+bb[1],'B', bbox=dict(facecolor='white'), fontsize=14, color='red')
ax.text(bb[2]-10, (bb[3]-bb[1])/2+bb[1],'A', bbox=dict(facecolor='white'), fontsize=14, color='red')
#plt.show()
plt.savefig('object_detection_example.eps')


#plt.axis('scaled')
#ax.set_aspect('equal')
#plt.xlim(0,1242)
#plt.ylim(-10,385)
#plt.yticks([1,187,375])

#plt.savefig(os.path.join(visualPath,"anchors.png"))
