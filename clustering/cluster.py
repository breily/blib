import math

# quick class to hold arbitrary number of dimensions for one point
class Cluster:
    def __init__(self, i, pt=None):
        self.i = i
        self.points = []
        if pt is not None: self.points.append(pt)

# all linkage functions use a distance metric (euclidean here)
def distance(x1, x2):
    if type(x1) is list:
        return math.sqrt(sum([math.pow(d1 - d2, 2) for d1, d2 in zip(x1, x2)]))
    else:
        return abs(x1 - x2)

# average distance for all points between clusters
def average_linkage(c1, c2):
    d = sum([distance(x1, x2) for x1 in c1.points for x2 in c2.points])
    return (d / float(len(c1.points) * len(c2.points)))

# distance of two points furthest apart
def complete_linkage(c1, c2):
    return max([distance(x1, x2) for x1 in c1.points for x2 in c2.points])

# distance of two points nearest together
def single_linkage(c1, c2):
    return min([distance(x1, x2) for x1 in c1.points for x2 in c2.points])

# distance between cluster centroids
def centroid_linkage(c1, c2):
    cen1 = sum(c1.points) / float(len(c1.points))
    cen2 = sum(c2.points) / float(len(c2.points))
    return distance(cen1, cen2)

# given point set (e.g. from usage.py) prints the cluster combinations that will
# occur with that algorithm
def main(points, link=centroid_linkage):
    clusters = []
    for p in points:
        clusters.append(Cluster(len(clusters), p))

    distances = [[0 for _ in xrange(len(clusters) * 2)] for __ in xrange(len(clusters) * 2)]
    for c1 in clusters:
        for c2 in clusters:
            distances[c1.i][c2.i] = link(c1, c2)
            distances[c2.i][c1.i] = distances[c1.i][c2.i]

    deleted = []
    while len(deleted) < (len(clusters) - 1):

        mindist_i = -1
        mindist_j = -1
        mindist = 100000
        for i in range(len(clusters)):
            if i in deleted: continue
            for j in range(len(clusters)):
                if j in deleted: continue
                if i == j: continue
                if distances[i][j] < mindist:
                    mindist = distances[i][j]
                    mindist_i = i
                    mindist_j = j

        print '%d\t%d\t%.07f\t%d' % (mindist_i + 1, mindist_j + 1, mindist, len(clusters) + 1)

        c = Cluster(len(clusters))
        c.points.extend(clusters[mindist_i].points)
        c.points.extend(clusters[mindist_j].points)
        clusters.append(c)
        deleted.append(mindist_i)
        deleted.append(mindist_j)

        for c1 in clusters:
            distances[c.i][c1.i] = link(c, c1)
            distances[c1.i][c.i] = distances[c.i][c1.i]

