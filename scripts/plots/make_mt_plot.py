import matplotlib.pyplot as plt
import os
from yahist import Hist1D, set_default_style
import uproot

set_default_style()

# bins = "250,0,750"
# fname = "/nfs-7/userdata/namin/tupler_babies/merged/FT/v3.31/output/year_2018/T1TTTT.root"
# t = uproot.open(fname)["t"]
# mtmin, hypclass = t["mtmin"].array(), t["hyp_class"].array()
# mtmin = mtmin[hypclass==3]
# Hist1D(mtmin, bins=bins).to_json("hist_mtmin_signal.json")
# fname = "/nfs-7/userdata/namin/tupler_babies/merged/FT/v3.31/output/year_2018/TTBAR_PH.root"
# t = uproot.open(fname)["t"]
# mtmin, hypclass = t["mtmin"].array(), t["hyp_class"].array()
# mtmin = mtmin[hypclass==3]
# Hist1D(mtmin, bins=bins).to_json("hist_mtmin_ttbar.json")


h_signal = Hist1D.from_json("hist_mtmin_signal.json")
h_ttbar = Hist1D.from_json("hist_mtmin_ttbar.json")

h_signal = h_signal.normalize()
h_ttbar = h_ttbar.normalize()

fig, ax = plt.subplots()
h_signal.plot(histtype="step", label="signal (T1tttt)", color="C3", gradient=True)
h_ttbar.plot(histtype="step", label=r"background ($t\bar{t}$ + jets)", color="C0", gradient=True)

ax.axvline(84., color="gray")
ax.text(1.1*84., 0.03, "$m_{W}$", fontsize=14, color="gray")

ax.set_yscale("log")
ax.set_ylabel("Frac. of events")
ax.set_xlabel(r"$m_\mathrm{T}^\mathrm{min}$ (GeV)")

xtype = 0.10
typ = "Simulation"
ax.text(0.0, 1.01,"CMS", horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes, weight="bold", size=15)
ax.text(xtype, 1.01,typ, horizontalalignment='left', verticalalignment='bottom', transform = ax.transAxes, style="italic", size=15)
ax.text(0.99, 1.01,"(13 TeV)", horizontalalignment='right', verticalalignment='bottom', transform = ax.transAxes, size=14)

fig.set_tight_layout(True)

ax.legend(fontsize=12)

fig.savefig("mtmin_signal_ttbar.pdf")
os.system("ic mtmin_signal_ttbar.pdf")
