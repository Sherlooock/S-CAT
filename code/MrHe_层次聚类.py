import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import json


def hierarchy_cluster(data, method='average', threshold=1):
	'''层次聚类
	Arguments:
		data [[0, float, ...], [float, 0, ...]] -- 文档 i 和文档 j 的距离
	Keyword Arguments:
		method {str} -- [linkage的方式： single、complete、average、centroid、median、ward] (default: {'average'})
		threshold {float} -- 聚类簇之间的距离
	Return:
		cluster_number int -- 聚类个数
		cluster [[idx1, idx2,..], [idx3]] -- 每一类下的索引
	'''
	data = np.array(data)
	print(data)
	Z = linkage(data, method=method)
	cluster_assignments = fcluster(Z, threshold, criterion='distance')
	num_clusters = cluster_assignments.max()
	indices = get_cluster_indices(cluster_assignments)
	# fig = plt.figure()
	# dn = dendrogram(Z)
	# plt.show()
	return num_clusters, indices


def get_cluster_indices(cluster_assignments):
	'''映射每一类至原数据索引
	Arguments:
		cluster_assignments 层次聚类后的结果
	Returns:
		[[idx1, idx2,..], [idx3]] -- 每一类下的索引
	'''
	n = cluster_assignments.max()
	indices = []
	for cluster_number in range(1, n + 1):
		indices.append(np.where(cluster_assignments == cluster_number)[0])

	return indices


if __name__ == '__main__':
	index_all = []
	f = open('e_cluster.json', 'r')
	arr = json.load(f)
	f.close()

	arr = np.array(arr)
	r, c = arr.shape
	for i in range(r):
		for j in range(i, c):
			if arr[i][j] != arr[j][i]:
				arr[i][j] = arr[j][i]
	for i in range(r):
		for j in range(i, c):
			if arr[i][j] != arr[j][i]:
				print(arr[i][j], arr[j][i])

	num_clusters, indices = hierarchy_cluster(arr)

	print("%d clusters" % num_clusters)
	for k, ind in enumerate(indices):
		print("cluster", k + 1, "is", ind)
		index_all.append(list(ind))
	print(index_all)
