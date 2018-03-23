#!/usr/bin/env python
# -*- coding: utf-8 -*-
import matplotlib.pylab as plt
import numpy as np
import scipy.io as sio
import os, sys, cv2
import argparse
import math
import pandas as pd
import pickle
import pdb

# 色をランダムに決定する関数
def generate_random_color(c):
	#colorlist = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']
	colorlist = ['#194be6','#3cb44b','#ffe119','#0082c8','#f58231','#911eb4','#46f0f0','#f032e6','#d2f53c','#fabebe','#008080','#e6beff','#aa6e28','#fffac8','#000008','#aaffc3','#808000','#ffd8b1']
	
	if c > len(colorlist)-1:
		color = tuple([np.random.rand() for _ in range(3)])
	else:
		color = colorlist[c]

	return color

#------------------------------------
# カーネルの計算
# x: カーネルを計算する対象の行列（次元 x データ数）
def gaussProb(x,z,sigma=1.0):
	dist = np.sum(np.square(x-z),axis=0)
	prob = np.exp(-dist/(2*sigma**2))

	return prob
#------------------------------------

#------------------------------------
# 外れ値除去平均距離法
def outlierAvgPredict(cropLaser,ratio=0.2):
	status = []
	
	outlierNum = int(len(cropLaser)*ratio)
	
	avg = np.mean(cropLaser)
	diff = np.abs(cropLaser - avg)
	sortedInd = np.argsort(diff)
	
	predict = np.mean(cropLaser[sortedInd[outlierNum:]])
	
	return predict,status
#------------------------------------

#------------------------------------
# 平均距離法
def avgPredict(cropLaser):
	status = []
	predict = np.mean(cropLaser)
	return predict,status
#------------------------------------

#------------------------------------
# 最小距離法
def nearestPredict(cropLaser):
	status = []
	predict = np.min(cropLaser)
	return predict,status
#------------------------------------

#------------------------------------
# Max Cluster Avg Distance method
def MCAD(cropLaser, laser, bb, thresh=-1, isCombine=True, isPlot=True):

	#-------------
	# 初期化
	status = np.zeros([4,len(cropLaser[1])])
	
	# 重み付きデータ数
	cntWeightNew = 0
	cntWeightMax = 0
	
	# クラスタ番号
	clInd=0
	clMaxInd = 0
	#-------------

	# weight
	laserCropThetas = cropLaser[0].values/540*270-45
	laserCropPoints = np.vstack([cropLaser[1].values*np.cos(laserCropThetas/180*np.pi),cropLaser[1].values*np.sin(laserCropThetas/180*np.pi)])
	weights = gaussProb(cPoint, laserCropPoints)
	
	#---------------------------------
	# 各試行に対する処理
	
	# 類似度の閾値を決定する
	thresh_f = thresh
	if thresh < 0:
		dists = cropLaser[1].values
		diffs = np.abs(dists[:-1]-dists[1:])
		mins = np.sin(0.5/180*np.pi)
		thresh = np.median(diffs/mins)

	for point in range(0,len(cropLaser[1])-1):

		# 現在の点の距離
		dist1=cropLaser[1][point]
		
		# 次の点の距離
		dist2=cropLaser[1][point+1]
		
		# 弦の長さ
		#math.sqrt(dist1**2+dist1**2-(2*dist1*dist1*np.cos(theta))) # 現在の点の二等辺三角形の底辺の長さ（余弦定理）
		#math.sqrt(dist2**2+dist2**2-(2*dist2*dist2*np.cos(theta))) # 次点の二等辺三角形の底辺の長さ（余弦定理）
		base1 = dist1*np.sin(theta) # 現在の点に関する最小距離
		base2 = dist2*np.sin(theta) # 次点のに関する最小距離
		dist  = math.sqrt(dist1**2+dist2**2-(2*dist1*dist2*np.cos(theta))) # 現在と次の点の弦の長さ（余弦定理）
		
		# 現在の点の方が遠い場合
		if dist/base1 < thresh:					# もし現在と次の点が近ければ
			if isCombine:
				cntWeightNew += weights[point]		# クラスタ内のデータ数をインクリメント
			else:
				cntWeightNew += 1.0

		else:									# もし現在と次の点が遠ければ
			# 最大クラスタより大きい場合、最大を入れ替える
			if cntWeightNew >= cntWeightMax:
				cntWeightMax = cntWeightNew
				clMaxInd = clInd
				cntWeightNew = 0
				clInd+=1

			# 最大クラスタより小さい場合、捨てる
			elif cntWeightNew < cntWeightMax:
				cntWeightNew = 0
				clInd+=1

		# 処理プロセスの記録
		status[0,point] = cropLaser[0][point]
		status[1,point] = weights[point]
		status[2,point] = dist1
		status[3,point] = clInd
	#---------------------------------

	#---------------------------------
	# 最大クラスタの平均距離
	predict = np.mean(status[2,status[3]==clMaxInd])
	#---------------------------------

	#------------------------------------
	#メッシュの作成
	if isPlot:
		plt.clf()
		
		X, Z = plt.meshgrid(plt.linspace(-8,8,100), plt.linspace(-8,8,100))
		width, height = X.shape
		X.resize(X.size)
		Z.resize(Z.size)
		points = np.vstack([X,Z])
		Y = gaussProb(cPoint, points)

		X.resize((width, height))
		Z.resize((width, height))
		Y.resize((width, height))
	
		# contourプロット
		levels=[x / 10.0 for x in np.arange(0, 11, 1)]
		CS = plt.contourf(X,Z,Y,levels) 
	
		# contourの数値ラベル
		#plt.clabel(CS, colors='black', inline=True, inline_spacing=0, fontsize=14)
	
		# contourのカラーバー
		CB = plt.colorbar(CS)
		CB.set_ticks(levels)
		CB.ax.tick_params(labelsize=14)
		for line in CB.lines: 
			line.set_linewidth(20)

		# 色空間の設定
		plt.gray()

	#------------------------------------

	#---------------------------------
	# クラスタのプロット
	if isPlot:
		print("bb dist:{}, laser dist:{}".format(bbDist,predict))

		plt.plot(laser[1]*np.cos((laser[0]*0.5-45)/180*np.pi),laser[1]*np.sin((laser[0]*0.5-45)/180*np.pi),'.',color='gray',linewidth=1)

		plt.plot([aPoint[0],cPoint[0],bPoint[0]],[aPoint[1],cPoint[1],bPoint[1]],lineStyle='-',color='red',linewidth=1)

		cluster = -1
		for point in np.arange(len(cropLaser[1])-1):
			if cluster != status[3, point]:
				cluster = int(status[3, point])
				
			color = generate_random_color(cluster)
				
			plt.plot(cropLaser[1][point]*np.cos((cropLaser[0][point]*0.5-45)/180*np.pi),cropLaser[1][point]*np.sin((cropLaser[0][point]*0.5-45)/180*np.pi),'.',color=color,linewidth=1)

		# max cluster
		color = "#ff0000"
		points = np.where(status[3]==clMaxInd)[0]
		plt.plot(cropLaser[1][points]*np.cos((cropLaser[0][points]*0.5-45)/180*np.pi),cropLaser[1][points]*np.sin((cropLaser[0][points]*0.5-45)/180*np.pi),'.',color=color,linewidth=1)
			
		plt.xlim(-8,8)
		plt.ylim(-5,8)
		plt.savefig(os.path.join(resPath,'laser_bb_cluster_{}_{}.svg'.format(trial,gamma_f)))
		plt.savefig(os.path.join(resPath,'laser_bb_cluster_{}_{}.eps'.format(trial,gamma_f)))
	#---------------------------------

	return predict,status
#------------------------------------

#################################################
methodID = 1

methods = ['MCAD', 'BWMCAD','nearest','average','outlier_remove']

# ファイルパス
statePaths = ['near/o/left/','near/o/center/','near/o/right/','far/o/left/','far/o/center/','far/o/right/',
'near/x/left/','near/x/center/','near/x/right/','far/x/left/','far/x/center/','far/x/right/']
gtDist = [2,2,2,5,5,5,2,2,2,5,5,5]

# スキャンの角度
theta = 0.5*np.pi/180

# カメラ画角
camTheta = 93.2

# 倍率
threshs = [1.4, 1.5, 2 , 3, 4, 5]
#threshs = [0]

# データ数
nData = 30

# plotするか否か
isPlot = True

for thresh in threshs:
	# 予測距離
	predictImg = []
	predictCmb = []
	gtDists = []

	for statePathInd in np.arange(len(statePaths)):
		print(statePaths[statePathInd])
	
		cropLaserPath='../data/cropLaser/' + statePaths[statePathInd]
		laserPath='../data/laser/' + statePaths[statePathInd]
		bbPath='../data/bb/' + statePaths[statePathInd]
		resPath='../results/' + methods[methodID] + '/' + statePaths[statePathInd]
		picklePath='../results/' + methods[methodID]

		# 結果フォルダが存在しなければ作成
		if not os.path.exists(resPath):
			os.makedirs(resPath)

		for trial in np.arange(1,nData+1):

			# データの読み込み
			cropLaser=pd.read_csv(os.path.join(cropLaserPath,'{}.txt'.format(trial)),header=None, sep=' ')
			laser=pd.read_csv(os.path.join(laserPath,'row-{}.txt'.format(trial)),header=None, sep=' ')
			bb = pd.read_csv(os.path.join(bbPath,'rcnn-{}.txt'.format(trial)),header=None, sep=' ')
		
			#-------------
			# BBのスキャンのインデックス
			aInd = int(bb[2]/744*93.2*2)
			bInd = int(bb[0]/744*93.2*2)
	
			# bbの中心の方位と距離、座標
			aAngle = 136.5 - bb[2]/744*93.2
			bAngle = 136.5 - bb[0]/744*93.2
			cAngle = (bAngle-aAngle)/2
			bbDist = bb[4].values[0]

			# 画像からの予測結果を格納
			predictImg.append(bbDist)
		
			# GT距離の格納
			gtDists.append(gtDist[statePathInd])

			# 極座標変換
			bPoint = np.array([bbDist*np.cos(bAngle/180*np.pi),bbDist*np.sin(bAngle/180*np.pi)])
			aPoint = np.array([bbDist*np.cos(aAngle/180*np.pi),bbDist*np.sin(aAngle/180*np.pi)])
			cPoint = (bPoint-aPoint)/2 + aPoint
			#-------------
	
			#-------------
			# 距離推定
			if methodID==0:
				predict, status = MCAD(cropLaser, laser, bb, thresh, isCombine=False)

			elif methodID==1:
				predict, status = MCAD(cropLaser, laser, bb, thresh, isCombine=True)

			elif methodID==2:
				predict, status = nearestPredict(cropLaser[1])

			elif methodID==3:
				predict, status = avgPredict(cropLaser[1])

			elif methodID==4:
				predict, status = outlierAvgPredict(cropLaser[1],0.2)

			# 画像とレーザの組み合わせからの予測結果を格納
			predictCmb.append(predict)
			#-------------

	#---------------------------------
	# 結果の出力
	with open(os.path.join(picklePath,'result_thresh{}.pkl'.format(thresh)),'wb') as fp:
		pickle.dump(predictImg,fp)
		pickle.dump(predictCmb,fp)
		pickle.dump(gtDists,fp)
#---------------------------------
#################################################
