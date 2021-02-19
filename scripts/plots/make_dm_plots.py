import json
import os
import numpy as np
import itertools
import re
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from matplotlib.ticker import MultipleLocator
from scipy import interpolate

from yahist import set_default_style
set_default_style()

# def add_cms_info(ax, typ="", lumi="137", xtype=0.12):
#     ax.text(0.0, 1.01,"CMS", horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes, weight="bold", size=20)
#     ax.text(xtype, 1.01,typ, horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes, style="italic", size="x-large")
#     ax.text(0.99, 1.01,"%s fb${}^\mathregular{-1}$ (13 TeV)" % (lumi), horizontalalignment='right', verticalalignment='bottom', transform = ax.transAxes, size="x-large")

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


def get_df(g11=True):
    if g11:
        df = load_data("data/data_dm_v4.txt")
    else:
        df = load_data("data/data_dm_v5.txt")

    df = df[df.tag.str.contains("dmscalar") | df.tag.str.contains("dmpseudo")]
    print(df.tag)
    df["which"] = df.tag.str.split("_").str[0]
    df["proc"] = df.tag.str.split("_").str[1]
    df["massmed"] = df.tag.str.split("_").str[2].astype(int)
    df["massdm"] = df.tag.str.split("_").str[3].astype(int)
    df = df.drop(["tag","folder"],axis=1)

    # separate 6 processes
    ttdm = df[df.proc=="ttdm"].rename(index=str,columns={"xsec":"xsec_ttdm"}).drop(["proc"],axis=1)
    ttsm = df[df.proc=="ttsm"].rename(index=str,columns={"xsec":"xsec_ttsm"}).drop(["proc"],axis=1)
    stwdm = df[df.proc=="stwdm"].rename(index=str,columns={"xsec":"xsec_stwdm"}).drop(["proc"],axis=1)
    stwsm = df[df.proc=="stwsm"].rename(index=str,columns={"xsec":"xsec_stwsm"}).drop(["proc"],axis=1)
    sttdm = df[df.proc=="sttdm"].rename(index=str,columns={"xsec":"xsec_sttdm"}).drop(["proc"],axis=1)
    sttsm = df[df.proc=="sttsm"].rename(index=str,columns={"xsec":"xsec_sttsm"}).drop(["proc"],axis=1)

    # make dataframe where each row contains all 6 processes, and sum up xsecs
    # print ttdm
    dfc = ttdm
    for x in [ttsm,stwdm,stwsm,sttdm,sttsm]:
        dfc = dfc.merge(x,suffixes=["",""],on=["which","massmed","massdm"],how="outer")
    # dfc = dfc.fillna(0.) # FIXME
    # dfc = dfc.fillna(15.e-3) # FIXME
    dfc["xsec_totdm"] = dfc["xsec_ttdm"] + dfc["xsec_stwdm"] + dfc["xsec_sttdm"]
    dfc["xsec_totsm"] = dfc["xsec_ttsm"] + dfc["xsec_stwsm"] + dfc["xsec_sttsm"]

    dfc["stfrac_sm"] = (dfc["xsec_stwsm"] + dfc["xsec_sttsm"])/dfc["xsec_totsm"]
    dfc["stfrac_dm"] = (dfc["xsec_stwdm"] + dfc["xsec_sttdm"])/dfc["xsec_totdm"]

    return dfc

def grid(x, y, z, resX=100j, resY=100j):
    from scipy.interpolate import griddata
    xi, yi = np.mgrid[min(x):max(x):resX, min(y):max(y):resY]
    # Z = griddata((x, y), z, (xi[None,:], yi[None,:]), method="linear") #, interp="linear")
    Z = griddata((x, y), z, (xi[None,:], yi[None,:]), method="linear") #, interp="linear")
    Z = Z[0]
    return xi, yi, Z


dfc1 = get_df(g11=True)
dfc2 = get_df(g11=False)


do_scatter = True
for which in [
        "dmscalar",
        "dmpseudo",
        ]:
    for key in [
            "xsec_totsm",
            # "stfrac_sm",
            # "xsec_totdm",
            # "stfrac_dm",
            ]:

        do_exclusion = False

        # fig,ax = plt.subplots()
        fig, ax = plt.subplots(gridspec_kw={"top":0.92,"bottom":0.14,"left":0.15,"right":0.95},figsize=(5.5,5.5))
        # which = "dmscalar"
        # which = "dmpseudo"
        # key = "xsec_totdm"
        # key = "xsec_totsm"
        df1 = dfc1[dfc1["which"] == which]
        df2 = dfc2[dfc2["which"] == which]

        if do_scatter:
            ax.scatter(df1["massmed"],df1["massdm"],c=df1[key],
            # ax.scatter(df2["massmed"],df2["massdm"],c=df2[key],
                    # norm=mpl.colors.LogNorm(vmin=1.5*1e-4,vmax=200*1e-3),
                    norm=mpl.colors.LogNorm(
                        vmin=max(df1[key].min(),0.001),
                        vmax=min(df1[key].max(),150.),
                        ),
                    cmap='cividis',
                    # cmap='Blues',
                               )

        data_rvals1 = []
        data_rvals2 = []
        if "frac" in key:
            for i,(massmed,massdm,val) in df1[["massmed","massdm",key]].iterrows():
                s = "{:.2f}".format(val)
                if do_scatter:
                    ax.text(massmed,massdm+8.,s,fontsize=7,horizontalalignment="center",verticalalignment="bottom")
        else:
            for i,(massmed,massdm,xsec) in df1[["massmed","massdm",key]].iterrows():
                xsec = xsec*1e3
                color = "k"
                if not np.isfinite(xsec): continue
                if xsec >= 100.: s = "{:.0f}".format(xsec)
                elif xsec >= 10.: s = "{:.1f}".format(xsec)
                elif xsec >= 1.: s = "{:.1f}".format(xsec)
                else: s = "{:.2f}".format(xsec)
                if do_scatter:
                    ax.text(massmed,massdm+8.,s,fontsize=6,horizontalalignment="center",verticalalignment="bottom",color=color)
            for i,(massmed,massdm,xsec) in df2[["massmed","massdm",key]].iterrows():
                xsec = xsec*1e3

        if "dm" in key:
            title = r"DM+X, X=$\mathrm{{t\bar{{t}}}}$,tW,tq [{}]".format(which[2:])
        else:
            title = r"$\mathrm{{t\bar{{t}}}}$+X, X=$\mathrm{{t\bar{{t}}}}$,tW,tq [{}]".format(which[2:])

        minx = 300.
        miny = 0.
        maxy = 700.
        maxx = 750.

        ax.set_xlim([minx,maxx])
        ax.set_ylim([miny,maxy])

        line = ax.plot([250,800],[0.5*250,0.5*800],linestyle="-",color="k",alpha=0.3)
        p1 = ax.transData.transform_point((minx,0.5*minx))
        p2 = ax.transData.transform_point((maxx,0.5*maxy))
        angle =  np.degrees(np.arctan2(*(p2-p1)[::-1]))
        # ax.text(maxx,0.5*maxy-40,r"$\mathrm{m}_\mathrm{med}<2 \mathrm{m}_\mathrm{DM}$   ",fontsize=10,horizontalalignment="right",verticalalignment="bottom",rotation=angle, color="0.3")
        if "pseudo" in which:
            ax.text(maxx,0.5*maxy-0,r"$m_\mathrm{A}<2 m_\chi$   ",fontsize=10,horizontalalignment="right",verticalalignment="bottom",rotation=angle, color="0.3")
        else:
            ax.text(maxx,0.5*maxy-0,r"$m_\mathrm{H}<2 m_\chi$   ",fontsize=10,horizontalalignment="right",verticalalignment="bottom",rotation=angle, color="0.3")

        if "pseudo" in which:
            # ax.text((maxx-minx)*0.8+minx,maxy*0.8,"pseudoscalar\nmediator",fontsize=14,horizontalalignment="center",verticalalignment="center",color="k")
            ax.text((maxx-minx)*0.8+minx,maxy*0.8,"pseudoscalar",fontsize=15,horizontalalignment="center",verticalalignment="center",color="k")
        else:
            # ax.text((maxx-minx)*0.8+minx,maxy*0.8,"scalar\nmediator",fontsize=14,horizontalalignment="center",verticalalignment="center",color="k")
            ax.text((maxx-minx)*0.8+minx,maxy*0.8,"scalar",fontsize=15,horizontalalignment="center",verticalalignment="center",color="k")

        print(which)

        # text = ax.set_title(title)
        # ax.set_ylabel(r"DM mass")
        ax.set_ylabel(r"$m_\chi$ (GeV)")
        # ax.set_xlabel(r"mediator mass")
        if "pseudo" in which:
            ax.set_xlabel(r"$m_\mathrm{A}$ (GeV)")
        else:
            ax.set_xlabel(r"$m_\mathrm{H}$ (GeV)")

        ax.yaxis.set_minor_locator(MultipleLocator(25.))
        ax.xaxis.set_minor_locator(MultipleLocator(25.))

        add_cms_info(ax, lumi="137")
        # ax.xaxis.set_minor_locator(MultipleLocator(10.))

        fig.set_tight_layout(True)
        # fig.set_tight_layout()
        if do_scatter:
            fname = "plot_2d_{}_{}.pdf".format(which,key)
        else:
            fname = "plot_2d_{}_{}_bothcouplings.pdf".format(which,key)
        fig.savefig(fname)
        os.system("ic "+fname)
