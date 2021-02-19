import subprocess
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

BDTOBSUL = 22.5

XSEC_TTTT = 11.97

def get_df(s):
    cmd = """grep -E "(# hhat|Integrated weight)" /home/users/namin/2018/fourtop/all/FTAnalysis/studies/FTInterpretations/runs/out_oblique_scan_v1/{s}*/Events/run_*/*_tag_1_banner.txt | xargs -L 2 echo | awk '{{print $3" "$11}}'""".format(s=s)
    data = map(lambda x:map(float,x.strip().split()),subprocess.getoutput(cmd).splitlines())
    df = pd.DataFrame(data,columns=["hhat","xsec"])
    df = df.sort_values(by=["hhat"])
    df["xsec"] *= 1e3
    return df


def plot_custom():
    df13 = get_df("out_test_13tevhhatscan_part")

    fig,ax = plt.subplots()

    hhats = np.linspace(0.,0.20,100)
    ax.plot(df13.hhat,df13.xsec/df13.xsec.min(),marker="o",label="MadGraph",markersize=5.,alpha=1.,color="C2")


    from scipy.optimize import curve_fit
    def f(x,a,b,c):
        return 1.+a*x+b*x**2+c*x**3
    subset = df13.hhat.values<0.25
    coef,cov = curve_fit(f,df13.hhat.values[subset],(df13.xsec/df13.xsec.min()).values[subset])
    coef = np.concatenate([np.array([1.]),coef])[::-1]
    xs = np.linspace(0.,0.25,1000)
    fpoly = np.poly1d(coef)
    ys = fpoly(xs)
    label = (
            r"Fit to MadGraph: "
            r"${:.0f}"
            r"{:+.2f}\hat{{H}}"
            r"{:+.2f}\hat{{H}}^2"
            r"{:+.2f}\hat{{H}}^3$"
            ).format(*coef[::-1])
    ax.plot(xs,ys,color="k",label=label)

    # ul = BDTOBSUL/11.97
    # dfy, fyint = get_corrected_ul()
    # ax.plot(hhats,np.ones(len(hhats))*ul,label="uncorrected obs UL (BDT)",color="0.6",linestyle="--")
    # ax.plot(hhats,fyint(hhats)/11.97,label="ttH-corrected obs UL (BDT)",color="k",linestyle="--")

    # dfcustom["xsecratio"] = fpoly(dfcustom.hhat)*dfcustom.obsr
    # ax.plot(dfcustom["hhat"],dfcustom["xsecratio"],label="Dedicated samples: obs UL (BDT)",color="r",marker="x")
    # fcustomint = interpolate.interp1d(dfcustom["hhat"],dfcustom["xsecratio"],kind="linear")
    # xs = np.linspace(dfcustom.hhat.min(),dfcustom.hhat.max(),100)

    # xs = np.linspace(0.,dfcustom["hhat"].max(),1000)
    # xy = np.c_[xs,fpoly(xs),fyint(xs)/11.97,fcustomint(xs)]
    # xcross = xy[np.abs(xy[:,1]-xy[:,3]).argmin()][0]
    # ax.plot([xcross,xcross],[1.,ul*1.5],linewidth=1.0,color="r",linestyle="--")
    # ax.annotate(
    #         "$\hat{{H}}={:.3f}$".format(xcross),
    #         color="r",
    #         xy=(xcross,1.0),
    #         xytext=(xcross*1.2,1+(ul-1)*0.5),
    #         arrowprops=dict(arrowstyle="->",color="r"),
    #         ha="left",
    #         fontsize=12
    #         )

    ax.set_ylim([1.,ax.get_ylim()[1]])
    ax.set_ylabel(r"$\sigma_{\hat{H}+\mathrm{SM}}/\sigma_\mathrm{SM}$")
    ax.set_title(r"$\sigma_{\hat{H}+\mathrm{SM}}/\sigma_\mathrm{SM}$ vs $\hat{H}$", fontsize=14)
    ax.set_xlabel(r"$\hat{H}$")

    ax.text(0.01, 2.75, "MadGraph5\n13TeV", fontsize=12)

    ax.yaxis.set_minor_locator(MultipleLocator(0.1))

    ax.legend()

    fig.set_tight_layout(True)
    fig.savefig("higgs_oblique.pdf")
    os.system("ic higgs_oblique.pdf")


if __name__ == "__main__":

    plot_custom()
