import os
import numpy as np
import itertools

import matplotlib
import matplotlib.pyplot as plt

from scipy.spatial import ConvexHull

from yahist import set_default_style
set_default_style()
from matplotlib import rcParams
rcParams["axes.xmargin"] = 0.1

# set_defaults()

srs = {2: {}, 3:{}}

# nb range, nj range ; both are inclusive
# set upper nj or nb to 10 or 5 if it there is a geq

import ROOT as r
nbs = range(2,5)
njs = range(2,9)
nlepsall = range(2,4)
triplets = list(itertools.product(nlepsall,nbs,njs))
d_points = {2: {}, 3: {}}
r.gROOT.ProcessLine(".L /home/users/namin/2018/fourtop/all/FTAnalysis/analysis/misc/signal_regions.h ")
for nleps,nbtags,njets in triplets:
    sr = r.signal_region_ft(njets,nbtags, 100.0, 500.0, 100, 11, 11, 30, 30, 30, nleps, False)
    if sr < 0: continue
    if sr not in d_points[nleps]: d_points[nleps][sr] = []
    d_points[nleps][sr].append((nbtags+0.5,njets+0.5))
    d_points[nleps][sr].append((nbtags+0.5,njets-0.5))
    d_points[nleps][sr].append((nbtags-0.5,njets+0.5))
    d_points[nleps][sr].append((nbtags-0.5,njets-0.5))

nsrs = 18
d_namelookup = dict(zip(range(1,nsrs+1),["CRZ","CRW"]+["SR{}".format(i-1) for i in range(2,nsrs+1)]))

# # 2 leps
# srs[2]["CRW"] = ((2,2), (2,5))
# srs[2]["SR1"] = ((2,2), (6,6))
# srs[2]["SR2"] = ((2,2), (7,7))
# srs[2]["SR3"] = ((2,2), (8,10))
# srs[2]["SR4"] = ((3,3), (5,5))
# srs[2]["SR5"] = ((3,3), (6,6))
# srs[2]["SR6"] = ((3,3), (7,7))
# srs[2]["SR7"] = ((3,3), (8,10))
# srs[2]["SR8"] =  ((4,4), (5,5))
# srs[2]["SR9"] =  ((4,4), (6,6))
# srs[2]["SR10"] = ((4,4), (7,10))
# # nlep >= 3
# srs[3]["SR11"] = ((2,2), (5,5))
# srs[3]["SR12"] = ((2,2), (6,6))
# srs[3]["SR13"] = ((2,2), (7,10))
# srs[3]["SR14"] = ((3,5), (4,4))
# srs[3]["SR15"] = ((3,5), (5,5))
# srs[3]["SR16"] = ((3,5), (6,10))

# def get_hull(ranges):
#     nbrange, njrange = np.array(ranges,dtype=float)
#     pad = False
#     if pad:
#         nbrange[0] -= 0.475
#         njrange[0] -= 0.445
#         nbrange[1] += 0.475
#         njrange[1] += 0.445
#     else:
#         nbrange[0] -= 0.5
#         njrange[0] -= 0.5
#         nbrange[1] += 0.5
#         njrange[1] += 0.5
#     corners = np.array([
#         [nbrange[0], njrange[0]],
#         [nbrange[1], njrange[0]],
#         [nbrange[0], njrange[1]],
#         [nbrange[1], njrange[1]],
#         ])
#     return corners, ConvexHull(corners)

def get_hull(points):
    return np.array(points), ConvexHull(points)

fig, (ax2, ax3) = plt.subplots(nrows=1, ncols=2, sharey=True, figsize=(6,4))

def plot_one(ax, srs, title=""):
    for srname in srs:
        # points, hull = get_hull(srs["CRW"])
        points, hull = get_hull(srs[srname])
        cx, cy = points[hull.vertices].mean(axis=0)
        for simplex in hull.simplices:
            edgeb, edgej = points[simplex, 0], points[simplex, 1]
            style = "C3-"
            if (edgej[0] == edgej[1]) and (edgej[0] > 8):
                style = "C3--"
            if (edgeb[0] == edgeb[1]) and (edgeb[0] > 4):
                style = "C3--"
            ax.plot(edgeb, edgej, style, linewidth=1.5)
        ax.text(cx,cy,d_namelookup[srname], horizontalalignment="center", verticalalignment="center", fontsize=12)

    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))

    ax.set_title(title)
    ax.set_xlabel("number of b-tagged jets")
    if "3" not in title:
        ax.set_ylabel("number of jets")

    # ax.set_aspect('equal')
    ax.grid(True)

plot_one(ax2, d_points[2], title="number of leptons = 2")
plot_one(ax3, d_points[3], title="number of leptons $\\geq$ 3")
# plot_one(ax2, srs[2], title="# leptons = 2")
# plot_one(ax3, srs[3], title="# leptons = 3")

fig.tight_layout()

fig.savefig("srplot.pdf")
os.system("ic srplot.pdf")
