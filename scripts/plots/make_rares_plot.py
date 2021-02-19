import sys
import numpy as np
sys.path.insert(0,'/home/users/namin/.local/lib/python2.7/site-packages/')

import os
import pandas as pd
from mytqdm import tqdm

import matplotlib as mpl
mpl.use('Agg')
from matplotlib import rcParams
import matplotlib.pyplot as plt
from matplottery.utils import Hist1D
from matplottery.plotter import plot_stack

import uproot
import itertools
import root_numpy as rn

np.set_printoptions(linewidth=150)


# colors from https://github.com/sgnoohc/Ditto/blob/master/python/makeplot.py#L193-L200
info_multitop = [
        ("TTWW" , [  0/255. , 114/255. , 178/255.]),
        ("TTTW" , [ 86/255. , 180/255. , 233/255.]),
        ("TTWZ" , [  0/255. , 158/255. , 115/255.]),
        ("TTWH" , [240/255. , 228/255. ,  66/255.]),
        ("TTHH" , [230/255. , 159/255. ,   0/255.]),
        ("TTZH" , [213/255. ,  94/255. ,   0/255.]),
        ("TTTJ" , [204/255. , 121/255. , 167/255.]),
        ("TTZZ" , [140/255. ,  93/255. , 119/255.]),
        ]

info_multiboson = [
        ("TZQ" , [  0/255. , 114/255. , 178/255.]),
        # ("WWDPS" , [ 86/255. , 180/255. , 233/255.]),
        ("QQWW" , [ 86/255. , 180/255. , 233/255.]),
        ("TWZ" , [  0/255. , 158/255. , 115/255.]),
        ("WZZ" , [240/255. , 228/255. ,  66/255.]),
        ("ZZ" , [230/255. , 159/255. ,   0/255.]),
        # ("GGHtoZZto4L" , [213/255. ,  94/255. ,   0/255.]),
        ("WWDPS" , [204/255. , 121/255. , 167/255.]),
        ("VHtoNonBB" , [140/255. ,  93/255. , 119/255.]),
        ("WW[GWZ]" , [110/255. ,  54/255. ,   0/255.]),
        ]

def transform_label(x):
    if "[" in x:
        toexplode = x.split("[")[-1].split("]")[0]
        x = x.replace(toexplode,",".join(toexplode))
    x = x.replace("[","{").replace("]","}").replace("T","t").replace("Q","q").replace("G",r"$\gamma$")
    x = x.replace("to",r"$\rightarrow$")
    x = x.replace("BB",r"$b\bar{b}$")
    x = x.replace("tt",r"t$\bar{\mathrm{t}}$")
    return x

# fname_patt = "/nfs-7/userdata/namin/tupler_babies/merged/FT/v3.13_all/output/year_2016/{}.root"
# fname_patt = "/nfs-7/userdata/namin/tupler_babies/merged/FT/v3.13_all/output/year_2017/{}.root"

for which,info in zip(["multitop","multiboson"],[info_multitop,info_multiboson]):
    hists = []
    bins = np.arange(0.5,17.5-2,1)
    for stag,color in info:
        tmp = []
        for year in [2016,2017,2018]:
            fname_patt = "/nfs-7/userdata/namin/tupler_babies/merged/FT/v3.24/output/year_%i/{}.root" % year
            try:
                arr = rn.root2array(fname_patt.format(stag),"t",branches=["sr-2", "{}*scale1fb".format({2016:35.9,2017:41.5,2018:58.8}[year])],
                    selection="hyp_class==3 && br && fired_trigger && passes_met_filters && sr>2")
                arr.dtype.names = ( "sr-2", "weight",)
                label = transform_label(stag)
                h = Hist1D(arr["sr-2"], weights=arr["weight"],bins=bins, label=label,color=color)
                tmp.append(h)
            except:
                print "ERROR with {} for {}".format(stag,year)
                continue
        h = sum(tmp)
        hists.append(h)

    fname = "plots_rares/h_{}.pdf".format(which)
    plot_stack(
            bgs=hists[::-1],
            filename=fname,
            do_log=False,
            # xlabel="SR",
            ylabel="Events",
            title="{}".format(which),
            lumi = 35.9+41.5+58.8,
            cms_type = "Preliminary",
            do_bkg_syst=True,
            xticks = ["SR{}".format(i) for i in range(1,20)],
            mpl_xtick_params=dict(fontsize=8,rotation=45),
            )
    os.system("ic {}".format(fname))

