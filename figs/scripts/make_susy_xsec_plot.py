#!/usr/bin/env python3

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from yahist import set_default_style
set_default_style()

def plot_one(ax, df, label, scale=1, color=None):
    baseline = ax.plot(df.mass_GeV, scale*df.xsec_pb, label = label, color=color)
    if "unc_up_pb" in df.columns:
        band = ax.fill_between(df.mass_GeV, scale*df.xsec_pb + scale*df.unc_down_pb, scale*df.xsec_pb + scale*df.unc_up_pb, alpha = 0.2, facecolor = baseline[0].get_color(), linewidth=0)
    else:
        band = ax.fill_between(df.mass_GeV, scale*df.xsec_pb - scale*df.unc_pb     , scale*df.xsec_pb + scale*df.unc_pb   , alpha = 0.2, facecolor = baseline[0].get_color(), linewidth=0)

  
filenames = [
  "pp13_gluino_NNLO+NNLL.json",
  "pp13_gluinosquark_NNLO+NNLL.json",
  "pp13_squark_NNLO+NNLL.json",
  "pp13_stopsbottom_NNLO+NNLL.json",
]

fig, ax = plt.subplots()

# load data and plot
colors = ["C0","C1","C2","C3","C4","C5"]
for color,filename in zip(colors,filenames):
    print(filename)
    data = json.load(open(os.path.join("data/susyjsons/", filename)))
    df   = pd.DataFrame.from_dict(data["data"], orient = "index")
    df["mass_GeV"] = df.index.astype(int)
    df = df.sort_values("mass_GeV")
    df.reset_index(inplace = True, drop = True)
    # plot
    latex = data["process_latex"]
    plot_one(ax, df, latex, scale=1e3, color=color)
    print(latex)
    # for letter in "gqb":
    #     latex = latex.replace(r"\tilde %s"%(letter), r"\tilde{\mathrm{%s}}"%(letter))
    m = 2000
    if "_stopsbottom_" in filename:
        m = 1800
    tmp = df[df["mass_GeV"] == m]
    x, y = tmp["mass_GeV"], tmp["xsec_pb"]*1e3
    # x, y = 1750, df["xsec_pb"].iloc[-1]
    # print(x,y)
    y *= 0.8
    if "_stopsbottom_" in filename:
        y *= 0.4
    ax.text(x,y,latex, color=color, rotation=-30, fontsize=14)

# draw legend and style plot
ax.set_xlabel("particle mass [GeV]")
ax.set_ylabel("cross section [fb]")
ax.set_yscale("log")
ax.grid(True)
ax.set_xlim(100, 2500)
ax.set_ylim(1e-5*1e3, 1e2*1e3)
# ax.legend(ncol = 2, framealpha = 1)
# ax.legend(ncol = 2)
# ax.locator_params(axis = "y", base = 100) # for log-scaled axis, it's LogLocator, not MaxNLocator
from matplotlib.ticker import MultipleLocator, LogLocator, NullFormatter
ax.set_title("$\mathit{pp}$, $\sqrt{\mathit{s}}$ = 13 TeV, NLO+NLL - NNLO$_\mathregular{approx}$+NNLL", fontsize = 12)

ax.xaxis.set_minor_locator(MultipleLocator(100.))

ax.yaxis.set_major_locator(LogLocator(base=10., subs=(1.,)))
ax.yaxis.set_minor_locator(LogLocator(base=10., subs=np.arange(2,10)*0.1))

fig.set_tight_layout(True)
fig.savefig("plot_susy_xsecs.pdf")
os.system("ic plot_susy_xsecs.pdf")
