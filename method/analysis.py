import pickle
import numpy as np
import os
import pdb

methodID = 1
isHalf = 2

methods = ['cluster', 'proposed','nearest','average','outlier_remove']
picklePath='../results/' + methods[methodID]

# 倍率
gammas = [1.5, 2]
#gammas = [0]


for gamma in gammas:
	print(gamma)
	with open(os.path.join(picklePath,'result_sin_oneside_gamma{}.pkl'.format(gamma)),'rb') as fp:
		predictImg = pickle.load(fp)
		predictCmb = pickle.load(fp)
		gtDists = pickle.load(fp)
	
	predictImg = np.array(predictImg)
	predictCmb = np.array(predictCmb)
	gtDists = np.array(gtDists)

	pdb.set_trace()
	# 遮蔽ぶつあり、なし
	if isHalf > 0:
		halfInd = int(len(predictImg)/2)
	
	if isHalf==1:
		predictImg = predictImg[:halfInd]
		predictCmb = predictCmb[:halfInd]
		gtDists = gtDists[:halfInd]
	elif isHalf==2:
		predictImg = predictImg[halfInd:]
		predictCmb = predictCmb[halfInd:]
		gtDists = gtDists[halfInd:]
	
	
	inds2 = np.where(gtDists==2)[0]
	inds5 = np.where(gtDists==5)[0]

	errorsImg = np.abs(predictImg - gtDists)
	print("img error:{}, std:{} at 2m".format(np.mean(errorsImg[inds2]),np.std(errorsImg[inds2])))
	print("img error:{}, std:{} at 5m".format(np.mean(errorsImg[inds5]),np.std(errorsImg[inds5])))
	print("img error:{}, std:{} All".format(np.mean(errorsImg),np.std(errorsImg)))
	
	print("-----------")

	errorsCmd = np.abs(predictCmb - gtDists)
	print("Cmd error:{}, std:{} at 2m".format(np.mean(errorsCmd[inds2]),np.std(errorsCmd[inds2])))
	print("Cmd error:{}, std:{} at 5m".format(np.mean(errorsCmd[inds5]),np.std(errorsCmd[inds5])))
	print("Cmd error:{}, std:{} All".format(np.mean(errorsCmd),np.std(errorsCmd)))
	print("-----------")
