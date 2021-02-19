import sys
import os
import numpy as np
import sys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib.patheffects as meffects
import matplotlib.font_manager as mfm
import pandas as pd
import pickle
import fnmatch
import glob
import ast
from matplotlib.ticker import MultipleLocator

import os
import matplotlib.pyplot as plt


# # SIGH
# import matplotlib
# matplotlib.rcParams['xtick.direction'] = 'in'
# matplotlib.rcParams['ytick.direction'] = 'in'

XSEC_TTTT = 11.97
GREEN = (0.,0.8,0.)
YELLOW = (1.,0.8,0.)

def set_defaults():
    from matplotlib import rcParams
    rcParams["font.family"] = "sans-serif"
    rcParams["font.sans-serif"] = ["Helvetica", "Arial", "Liberation Sans", "Bitstream Vera Sans", "DejaVu Sans"]
    rcParams['legend.fontsize'] = 13
    rcParams['legend.labelspacing'] = 0.2
    rcParams['axes.xmargin'] = 0.0 # rootlike, no extra padding within x axis
    rcParams['axes.labelsize'] = 'x-large'
    rcParams['axes.formatter.use_mathtext'] = True
    rcParams['legend.framealpha'] = 0.65
    rcParams['axes.labelsize'] = 'x-large'
    rcParams['axes.titlesize'] = 'x-large'
    rcParams['xtick.labelsize'] = 'x-large'
    rcParams['ytick.labelsize'] = 'x-large'
    rcParams['figure.subplot.hspace'] = 0.1
    rcParams['figure.subplot.wspace'] = 0.1
    rcParams['figure.subplot.right'] = 0.96
    rcParams['figure.max_open_warning'] = 0
    rcParams['figure.dpi'] = 125
    rcParams["axes.formatter.limits"] = [-5,4] # scientific notation if log(y) outside this

# def add_cms_info(ax, typ="", lumi="137", xtype=0.12):
#     ax.text(0.0, 1.01,"CMS", horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes, weight="bold", size=20)
#     ax.text(xtype, 1.01,typ, horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes, style="italic", size="x-large")
#     ax.text(0.99, 1.01,"%s fb${}^\mathregular{-1}$ (13 TeV)" % (lumi), horizontalalignment='right', verticalalignment='bottom', transform = ax.transAxes, size="x-large")

def add_cms_info(ax, typ="", lumi="137", xtype=0.12):
    ax.text(0.99, 1.01,"(13 TeV)", horizontalalignment='right', verticalalignment='bottom', transform = ax.transAxes, size="x-large")

def get_fig_ax():
    fig, ax = plt.subplots(gridspec_kw={"top":0.92,"bottom":0.14,"left":0.15,"right":0.95},figsize=(5.5,5.5))
    return fig, ax

class DoubleBandObject(object): pass
class DoubleBandObjectHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = mpatches.Rectangle([x0, y0-height*0.25], width, height*1.5, facecolor=YELLOW,
                                   edgecolor="none", lw=0.,
                                   transform=handlebox.get_transform())
        handlebox.add_artist(patch)
        patch = mpatches.Rectangle([x0, y0+0.25*height*1.5-height*0.25], width, height*1.5*0.5, facecolor=GREEN,
                                   edgecolor="none", lw=0.,
                                   transform=handlebox.get_transform())
        handlebox.add_artist(patch)
        patch = mlines.Line2D(
                [x0+width*0.03,x0+width-width*0.03],[y0-height*0.25+height*0.75],color=(0.,0.,0.),linewidth=1,linestyle="--",
                transform=handlebox.get_transform(),
                )
        handlebox.add_artist(patch)
        return patch

class OneSideHatchObject(object): pass
class OneSideHatchObjectHandler(object):
    def legend_artist(self, legend, orig_handle, fontsize, handlebox):
        x0, y0 = handlebox.xdescent, handlebox.ydescent
        width, height = handlebox.width, handlebox.height
        patch = mlines.Line2D(
                [x0+width*0.03,x0+width-width*0.03],[y0+height*0.2,y0+height*0.2],color=(0.4,0.4,0.4),linewidth=2,linestyle="-",
                transform=handlebox.get_transform(),
                )
        handlebox.add_artist(patch)
        patch = mpatches.Rectangle([x0, y0+height*0.2], width, height-height*0.2, facecolor='none',
                                   edgecolor=(0.4,0.4,0.4), hatch='///', lw=0.,
                                   transform=handlebox.get_transform())
        handlebox.add_artist(patch)
        return patch


def make_yukawa_plot():

    # A: gza
    # B: int 
    # F: higgs
    def calc_sigma(kt,A,B,F):
        return A + B*kt**2 + F*kt**4

    # kfactor such that xsec=11.97 at kt=1
    kfactor = 1.2445

    gza_13tev = 9.997*kfactor
    int_13tev = -1.547*kfactor
    higgs_13tev = 1.168*kfactor
    # scale variations for 13 tev numbers
    gza_13tev_up = 14.104*kfactor
    int_13tev_up = -2.152*kfactor
    higgs_13tev_up = 1.625*kfactor
    gza_13tev_down = 6.378*kfactor
    int_13tev_down = -0.999*kfactor
    higgs_13tev_down = 0.7655*kfactor

    kts_fine = np.linspace(0.,3.0,31.)
    theory_cent = calc_sigma(kts_fine,gza_13tev,int_13tev,higgs_13tev)
    theory_down = calc_sigma(kts_fine,gza_13tev_down,int_13tev_down,higgs_13tev_down)
    theory_up = calc_sigma(kts_fine,gza_13tev_up,int_13tev_up,higgs_13tev_up)

    fig,ax = get_fig_ax()
    add_cms_info(ax)

    p1 = ax.fill_between(kts_fine, theory_down, theory_up, linewidth=0., facecolor="C0", alpha=0.3)
    p2 = ax.plot(kts_fine, theory_cent, linestyle="--", marker="",color=(0.04,0.16,0.31))

    legend = ax.legend(
            [
                (p1,p2[0]),
                ],
            [
                "Predicted cross section",
                ],
            handler_map={OneSideHatchObject: OneSideHatchObjectHandler()},
            labelspacing=0.6,
            fontsize=12,
            )

    ax.xaxis.set_minor_locator(MultipleLocator(0.1))
    ax.yaxis.set_minor_locator(MultipleLocator(2))

    ax.axvline(1., color="gray")
    ax.text(1.1, 40., "SM", color="gray", fontsize=14)

    ax.set_ylim([0.,55.])
    ax.set_ylabel(r"$\sigma_{t\bar{t}t\bar{t}}$ (fb)")
    ax.set_title("")
    ax.set_xlabel(r"$|y_\mathrm{t}\ /\ y_\mathrm{t}^\mathrm{SM}|$")
    fig.set_tight_layout(True)
    fname = "cross_section_yt.pdf"
    fig.savefig(fname)
    os.system("ic {}".format(fname))
    print("Saved {}".format(fname))

if __name__ == "__main__":

    set_defaults()

    make_yukawa_plot()
