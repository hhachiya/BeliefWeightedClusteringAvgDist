# -*- coding: utf-8 -*-

import matplotlib.pylab as plt
from PIL import Image
import matplotlib.patches as patches
import numpy as np

import pdb


statePaths = ['near/o/left/','near/o/center/','near/o/right/','far/o/left/','far/o/center/','far/o/right/',
'near/x/left/','near/x/center/','near/x/right/','far/x/left/','far/x/center/','far/x/right/']

for statePath in statePaths:
	imgPath = "data/img/"+statePath+"/img-2.png"
	bbPath = "data/bb/"+statePath+"/rcnn-2.txt"


	# データ読み込み
	im = plt.imread(imgPath)
	with open(bbPath,"rt") as fp:
		bb = fp.readline().split(' ')
	
	bb = np.array(bb[:5]).astype(np.float)

	# プロット
	fig = plt.figure()
	ax = plt.axes()

	# 画像
	plt.imshow(im)

	# BB
	r = patches.Rectangle(xy=(bb[0], bb[1]), width=bb[2]-bb[0], height=bb[3]-bb[1], ec='red', fill=False, linewidth=3.5)
	ax.add_patch(r)

	ax.text(bb[0]+10, bb[1]-10,"{:.2f}".format(bb[4]), bbox=dict(facecolor='red'), fontsize=14, color='white')

	statePath = statePath.replace('/', '_')

	fname = 'object_detection_example_'+statePath+'.eps'
	plt.savefig(fname)
