# -*- coding: utf-8 -*-
from scipy.spatial import distance as dist
from collections import OrderedDict
import numpy as np


class CentroidTracker:
	def __init__(self, maxDisappeared=50, maxDistance=50):
		# 下一个可用的对象ID
		self.nextObjectID = 0
		# 给定对象ID及相应质心
		self.objects = OrderedDict()
		# 标记为“消失”的连续帧数
		self.disappeared = OrderedDict()

		# 允许将给定对象标记为“消失”的最大连续帧数
		self.maxDisappeared = maxDisappeared

		# 存储质心之间的最大距离以关联对象——如果距离大于此最大距离，我们将开始将对象标记为“消失”
		self.maxDistance = maxDistance

	def register(self, centroid):
		# 注册对象时，我们使用下一个可用的对象ID来存储质心
		self.objects[self.nextObjectID] = centroid
		self.disappeared[self.nextObjectID] = 0
		self.nextObjectID += 1

	def deregister(self, objectID):
		del self.objects[objectID]
		del self.disappeared[objectID]

	def update(self, rects):
		# 如果没有检测到任何边界框
		if len(rects) == 0:
			# 所有现存物体这一帧消失
			for objectID in list(self.disappeared.keys()):
				self.disappeared[objectID] += 1

				# 达到最大消失数注销
				if self.disappeared[objectID] > self.maxDisappeared:
					self.deregister(objectID)

			# return early as there are no centroids or tracking info
			# to update
			return self.objects

		# rects行2列全为0数组用来存质心
		inputCentroids = np.zeros((len(rects), 2), dtype="int")

		for (i, (startX, startY, endX, endY)) in enumerate(rects):
			cX = int((startX + endX) / 2.0)
			cY = int((startY + endY) / 2.0)
			inputCentroids[i] = (cX, cY)

		# 如果还没开始追踪物体，则注册
		if len(self.objects) == 0:
			for i in range(0, len(inputCentroids)):
				self.register(inputCentroids[i])

		# 否则更新当前物体质心
		else:

			objectIDs = list(self.objects.keys())
			objectCentroids = list(self.objects.values())

			# 计算距离 objects.size*rect
			D = dist.cdist(np.array(objectCentroids), inputCentroids)

			# D.min(axis=1)每行最小值组成的一维数组  argsort将一维数组从小到大排序返回索引值一维数组
			rows = D.min(axis=1).argsort()

			# D.argmin(axis=1)每行最小值的索引组成的一维数组，对应rows
			cols = D.argmin(axis=1)[rows]

			# 已检查过的行列
			usedRows = set()
			usedCols = set()

			# zip(rows, cols)每行最小值按从小到大排序，对应的索引
			for (row, col) in zip(rows, cols):
				if row in usedRows or col in usedCols:
					continue

				if D[row, col] > self.maxDistance:
					continue

				# 更新质心和消失连续帧数
				objectID = objectIDs[row]
				self.objects[objectID] = inputCentroids[col]
				self.disappeared[objectID] = 0

				usedRows.add(row)
				usedCols.add(col)

			# 未检查的行列 shape[0]第一维的数目 shape[1]第二维的数目 在此分别为行数和列数
			unusedRows = set(range(0, D.shape[0])).difference(usedRows)
			unusedCols = set(range(0, D.shape[1])).difference(usedCols)

			# 行数大于列数即原有物体数大于现有物体数 判断是否有物体消失
			if D.shape[0] >= D.shape[1]:
				for row in unusedRows:
					objectID = objectIDs[row]
					self.disappeared[objectID] += 1
					if self.disappeared[objectID] > self.maxDisappeared:
						self.deregister(objectID)

			# 现有物体数大于原有物体数，则有新物体出现
			else:
				for col in unusedCols:
					self.register(inputCentroids[col])


		return self.objects


