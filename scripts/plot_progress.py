import os
import sys
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import matplotlib as mpl

from matplotlib import rcParams
rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = ["Helvetica", "Arial", "Liberation Sans", "Bitstream Vera Sans", "DejaVu Sans"]
rcParams['legend.fontsize'] = 11
rcParams['legend.labelspacing'] = 0.2
rcParams['axes.labelsize'] = 'x-large'

data = []
with open("logs/size_log.txt","r") as fh:
    for line in fh:
        if not line.strip(): continue
        date, _, pages, _, _, b = line.strip().split()[1:-1]
        date = date.rsplit("-",1)[0]
        data.append([date,int(pages),int(b)*1.e-3])
df = pd.DataFrame(data,columns=["date","pages","kb"])
df["date"] = pd.to_datetime(df["date"])

fig,ax = plt.subplots()
ax.plot(df["date"],df["pages"])
ax.set_ylim([0.,100.])
ax.set_ylabel("PDF page count")
ax.legend()

deadline = datetime.date(2019,6,15)
plt.axvline(deadline,color="gray")
ax.text(deadline,ax.get_ylim()[1],"semi-fake deadline  ",horizontalalignment="right",verticalalignment="top",rotation=90,color="gray",fontsize=12)

p = mpl.patches.Rectangle((0.,0.),height=1.0,width=0.9,transform=ax.transAxes)
ax.grid(axis="both",linewidth=0.5,alpha=0.5)

fig.autofmt_xdate()

fig.set_tight_layout(True)
fig.savefig("figs/misc/progress.png")
fig.savefig("figs/misc/progress.pdf")
