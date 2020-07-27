#!/usr/bin/env python3
# coding: utf-8
import os
import sys
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import ndimage

from matplotlib import rcParams
rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Helvetica", "Arial", "Liberation Sans", "Bitstream Vera Sans", "DejaVu Sans"]
rcParams['legend.fontsize'] = 12
rcParams['axes.labelsize'] = 'x-large'

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# plt.xkcd()

basedir = "/Users/namin/sandbox/notmythesis"

data = []
with open("{}/logs/size_log.txt".format(basedir),"r") as fh:
    for line in fh:
        if not line.strip(): continue
        date, _, pages, _, _, b = line.strip().split()[1:-1]
        date = date.rsplit("-",1)[0]
        data.append([date,int(pages),int(b)*1.e-3])
df = pd.DataFrame(data,columns=["date","pages","kb"])
df["date"] = pd.to_datetime(df["date"])

df = df.set_index("date")["2020":].reset_index()

fig,ax = plt.subplots()
ax.plot(df["date"],df["pages"],label="actual", marker=".")
ax.set_ylim([0.,150.])
ax.set_ylabel("PDF page count")

deadline = datetime.date(2020,8,12)
plt.axvline(deadline,color="gray")
ax.text(deadline,ax.get_ylim()[1],"actual deadline  ",horizontalalignment="right",verticalalignment="top",rotation=90,color="gray",fontsize=12)

p = mpl.patches.Rectangle((0.,0.),height=1.0,width=0.9,transform=ax.transAxes)
ax.grid(axis="both",linewidth=0.5,alpha=0.5,clip_path=p)

xdeadline = mpl.dates.date2num(deadline)

def data_to_fig(x,y):
    return fig.transFigure.inverted().transform(ax.transData.transform((x,y)))
xfirst = mpl.dates.date2num(df["date"].values[0])
xlatest = mpl.dates.date2num(df["date"].values[-1])
yfirst = df["pages"].values[0]
ylatest = df["pages"].values[-1]
x0, y0 = ax.get_xlim()[0],ax.get_ylim()[0]
x1, y1 = ax.get_xlim()[1],ax.get_ylim()[1]

# ax.set_xlim([None, ax.get_xlim()[1]+90])
ax.set_xlim([None, ax.get_xlim()[1]+15])

slope = (ylatest-yfirst)/(xlatest-xfirst)
xs = np.linspace(xlatest,xdeadline,100)
xnorms = (xs-xlatest)/(xs.max()-xs.min())
ys_high = (ylatest + slope*1.5*(xs-xlatest))*np.exp(-10*xnorms)
ys_low = (ylatest + slope*0.7*(xs-xlatest))*np.exp(-15*xnorms)
ax.fill_between(xs,ys_low,ys_high,color="C0",alpha=0.25,label="projected 95% \nlack-of-confidence-in-myself \nbands")

ax.legend()

p = mpl.patches.Rectangle((xdeadline,0.),height=ax.get_ylim()[1],width=(ax.get_xlim()[1]-xdeadline),transform=ax.transData,edgecolor=(0.7,0.7,0.7),hatch="///",facecolor="none")
ax.add_patch(p)

fig.autofmt_xdate()

fig.set_tight_layout(True)
fig.savefig("{}/figs/misc/progress.png".format(basedir))

os.system("ic {}/figs/misc/progress.png".format(basedir))
