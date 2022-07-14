# -*- coding: utf-8 -*-
class TrackableObject:
	def __init__(self, objectID, centroid):
		# id和质心
		self.objectID = objectID
		self.centroids = [centroid]

		self.counted = False