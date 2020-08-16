import json
import os
import numpy as np
import itertools
import re
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import MultipleLocator
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from scipy import interpolate

from yahist import set_default_style
set_default_style()

def add_cms_info(ax, typ="", lumi="137", xtype=0.12):
    ax.text(0.99, 1.01,"(13 TeV)", horizontalalignment='right', verticalalignment='bottom', transform = ax.transAxes, size="x-large")

def load_data(fname="data/ftinterpretations_data.txt"):
    data = []
    with open(fname,"r") as fh:
        for line in fh:
            parts = line.strip().split(":")
            if not parts: continue
            if "hadoop" in parts[0]:
                folder = ""
                proctag = parts[0].rsplit("/",1)[-1].rsplit(".",1)[0]
                xsec = float(parts[-1].strip())
            else:
                folder = parts[0].split("/Events",1)[0].rsplit("/",2)[-2]
                proctag = parts[0].split("/Events",1)[0].rsplit("/",1)[-1]
                xsec = float(parts[-1].strip())
            data.append(dict(folder=folder,tag=proctag,xsec=xsec))
    df = pd.DataFrame(data)
    return df

def plot_crossings(df, ul=2.,which="phi"):
    fig, ax = plt.subplots(nrows=1, ncols=1)
    edges = []
    masses = sorted(df["mass"].unique())
    print(len(masses))
    import matplotlib
    cmap = matplotlib.cm.get_cmap("magma")
    colors = cmap(np.linspace(0,0.8,len(masses)))
    for color,mass in zip(colors,masses):
    # for mass in masses:
        sel = df["mass"]==mass
        xs = df["coupling"][sel]
        ys = df["ratio"][sel]
        # mask that returns unique elements (assuming xs is sorted, which it is)
        uniq = np.array([True]+(np.diff(xs)!=0).tolist())
        xs = xs[uniq]
        ys = ys[uniq]
        label = "{:.0f}GeV".format(mass)
        # ax.plot(xs,ys,label=label,markersize=5.,marker="o")
        ax.plot(xs,ys,label=label,markersize=5.,marker="o", color=color)
        if len(xs) >= 3:
            fint = interpolate.interp1d(xs,ys,kind="quadratic")
            xnew = np.linspace(xs.min(),xs.max(),100.)
            ynew = fint(xnew)
            # ax.plot(xnew,ynew,linewidth=1.0,color="k")
            # ax.plot(xnew,ynew,linewidth=1.0,color=color)
            if ynew.min() < ul < ynew.max():
                big_xy = np.c_[np.linspace(xs.min(),xs.max(),1000),fint(np.linspace(xs.min(),xs.max(),1000))]
                xcross = big_xy[np.abs(big_xy[:,1]-ul).argmin()][0]
                edges.append([mass,xcross])
                # ax.plot([xcross,xcross],[0.,ul*1.5],linewidth=1.0,color="k",linestyle="--")
                ax.plot([xcross,xcross],[0.,ul*1.5],linewidth=1.0,color=color,linestyle="--")

    ax.plot([0.,1.5],[ul,ul],label="",color="k",linestyle="--")
    ax.set_ylim([1.,ax.get_ylim()[1]])
    ax.set_ylabel(r"$\sigma_\mathrm{NP+SM}/\sigma_\mathrm{SM}$")
    if which == "phi":
        ax.set_title(r"scalar $\phi$: $\sigma_\mathrm{NP+SM}/\sigma_\mathrm{SM}$ vs $g_\mathrm{t\phi}$", fontsize=14)
        ax.set_xlabel(r"$g_\mathrm{t\phi}$")
        ax.set_xlim([0.6,1.6])
    else:
        ax.set_title(r"vector $Z'$: $\sigma_\mathrm{NP+SM}/\sigma_\mathrm{SM}$ vs $g_\mathrm{tZ'}$", fontsize=14)
        ax.set_xlabel(r"$g_\mathrm{tZ'}$")
    ax.legend(loc="upper right")
    ax.xaxis.set_minor_locator(MultipleLocator(0.05))
    add_cms_info(ax)
    # ax.set_yscale("log")
    fig.tight_layout()
    fig.savefig("plot_xsec_{}.pdf".format(which))
    os.system("ic plot_xsec_{}.pdf".format(which))
    edges = np.array(edges)
    edges = np.concatenate([edges,[[340.,2.0],[25.,2.0]]])
    return edges


if __name__ == "__main__":


    d_edges = {}
    for which in ["zprime","phi"]:
    # for which in ["zprime"]:
        df = load_data()
        df = df[df.tag.str.contains(which)]
        df["mass"] = df.tag.str.split("_").str[2].astype(int)
        df["coupling"] = df.tag.str.split("_").str[3].str.replace("p",".").astype(float)
        df = df.drop(["tag"],axis=1)
        df = df.sort_values(["mass","coupling"])
        xsec_sm = df[df.coupling==0.]["xsec"].values.min()
        df["ratio"] = df["xsec"]/xsec_sm # ratio wrt SM (smallest xsec in the list)
        edges = plot_crossings(df,which=which)
        d_edges[which] = edges
