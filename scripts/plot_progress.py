#!/usr/bin/env python
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
# print df["date"].to_pydatetime()
# df["date"] = pd.Timestamp(df["date"]).to_pydatetime()

fig,ax = plt.subplots()
ax.plot(df["date"],df["pages"],label="actual")
ax.set_ylim([0.,100.])
ax.set_ylabel("PDF page count")

deadline = datetime.date(2019,6,15)
plt.axvline(deadline,color="gray")
ax.text(deadline,ax.get_ylim()[1],"semi-fake deadline  ",horizontalalignment="right",verticalalignment="top",rotation=90,color="gray",fontsize=12)

p = mpl.patches.Rectangle((0.,0.),height=1.0,width=0.9,transform=ax.transAxes)
ax.grid(axis="both",linewidth=0.5,alpha=0.5,clip_path=p)

# print ax.get_xlim()
# xnum0 = ax.get
# xnum1 = 

xdeadline = mpl.dates.date2num(deadline)

def data_to_fig(x,y):
    return fig.transFigure.inverted().transform(ax.transData.transform((x,y)))
xfirst = mpl.dates.date2num(df["date"].dt.values[0])
xlatest = mpl.dates.date2num(df["date"].dt.values[-1])
yfirst = df["pages"].values[0]
ylatest = df["pages"].values[-1]
x0, y0 = ax.get_xlim()[0],ax.get_ylim()[0]
x1, y1 = ax.get_xlim()[1],ax.get_ylim()[1]


slope = (ylatest-yfirst)/(xlatest-xfirst)
print slope
# ax.plot([xlatest,x1],[ylatest,y1],color="r",marker="o")
xs = np.linspace(xlatest,xdeadline,100)
xnorms = (xs-xlatest)/(xs.max()-xs.min())
# print xnorms
ys_high = (ylatest + slope*1.5*(xs-xlatest))*np.exp(-10*xnorms)
ys_low = (ylatest + slope*0.7*(xs-xlatest))*np.exp(-15*xnorms)
# ax.plot(xs,ys,color="b",marker="o")
print xs
print xdeadline
ax.fill_between(xs,ys_low,ys_high,color="C0",alpha=0.25,label="projected 95% lack-of-confidence-in-myself bands")
print df

ax.legend()

p = mpl.patches.Rectangle((xdeadline,0.),height=ax.get_ylim()[1],width=(ax.get_xlim()[1]-xdeadline),transform=ax.transData,edgecolor=(0.7,0.7,0.7),hatch="///",facecolor="none")
ax.add_patch(p)
print p

# # xw = 0.05*(ax.get_xlim()[1]-ax.get_xlim()[0])
# # yw = 0.05*(ax.get_ylim()[1]-ax.get_ylim()[0])
# xw_fig = 0.15*(xr_fig-xl_fig)
# yh_fig = 0.15*(yt_fig-yb_fig)
# # print x0,y0,xw,yw
# print x0_fig,y0_fig,xw_fig,yh_fig
# # ax2 = fig.add_axes([x0,y0,xw,yw],transform=ax.transData)
# poo_img = plt.imread("poo-mark.png")

# ax.imshow(poo_img,extent=[0,1,0,1],aspect="auto")

# ax2 = fig.add_axes([x0_fig-xw_fig/2.,y0_fig-yh_fig/2.,xw_fig,yh_fig],frameon=False,anchor="C")
# tr = mpl.transforms.Affine2D().rotate_deg(60.)
# ax2.imshow(poo_img,alpha=0.3,transform=tr+ax2.transData,extent=[-1,1,-1,1])
# # ax2.imshow(poo_img,alpha=0.3)
# # ax2.set_transform(tr+ax2.transData)
# print ax2
# # ax2.axis("off")
# # print (fig.transFigure + ax.transAxes.inverted()).transform((x0,y0))


# ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(5.))
# ax.yaxis.set_major_locator(mpl.ticker.MultipleLocator(20.))

# ax.grid(axis="both",linewidth=0.5,alpha=0.5,clip_path=p)

# box = mpl.transforms.Bbox.from_bounds(0.8, 0, 0.2, 0.2)
# ax2 = fig.add_axes(fig.transFigure.inverted().transform_bbox( ax.transAxes.transform_bbox(box)))

# x,y = mpl.dates.date2num(df["date"].dt.values[-1]),df["pages"].values[-1]
# print x,y
# print fig.add_axes([0.,0.,0.1,0.1],transform=ax.transData,projection="rectilinear")
#     # loc[0]/fig_width-poo_size/2, loc[1]/fig_height-poo_size/2,
#     #                        poo_size, poo_size], anchor='C')

# poo_img = plt.imread("poo-mark.png")
# ax_width = ax.get_window_extent().width
# fig_width = fig.get_window_extent().width
# fig_height = fig.get_window_extent().height
# poo_size = ax_width/(fig_width*len(x))
# poo_axs = [None for i in range(len(x))]
# loc = ax.transData.transform((x,y))
# poo_axs[i] = fig.add_axes([loc[0]/fig_width-poo_size/2, loc[1]/fig_height-poo_size/2,
#                            poo_size, poo_size], anchor='C')
# poo_axs[i].imshow(poo_img)
# poo_axs[i].axis("off")

fig.autofmt_xdate()

fig.set_tight_layout(True)
fig.savefig("{}/figs/misc/progress.pdf".format(basedir))
fig.savefig("{}/figs/misc/progress.png".format(basedir))

os.system("ic {}/figs/misc/progress.png".format(basedir))
