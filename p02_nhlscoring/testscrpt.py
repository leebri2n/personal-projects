from hockey_rink import NHLRink
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

pbp = pd.read_csv("https://hockey-data.harryshomer.com/pbp/nhl_pbp20192020.csv.gz", compression="gzip")
pbp["goal"] = (pbp.Event == "GOAL").astype(int)
pbp["x"] = np.abs(pbp.xC)
pbp["y"] = pbp.yC * np.sign(pbp.xC)
shots = pbp.loc[(pbp.Ev_Zone == "Off") & ~pbp.x.isna() & ~pbp.y.isna() & (pbp.Event.isin(["GOAL", "SHOT", "MISS"]))]

print(pbp)
print(type(pbp))
print(pbp["goal"])
print(pbp["x"])
print(pbp["y"])
print("PRINTING SHOTS DF")
print(shots)

fig, axs = plt.subplots(1, 3, figsize=(14, 8))
rink = NHLRink(rotation=270)
for i in range(3):
    rink.draw(ax=axs[i], display_range="ozone")
    contour_img = rink.contourf(shots.x, shots.y, values=shots.goal, ax=axs[0], cmap="bwr",
                            plot_range="ozone", binsize=10, levels=50, statistic="mean")
    plt.colorbar(contour_img, ax=axs[0], orientation="horizontal")
    rink.heatmap(shots.x, shots.y, values=shots.goal, ax=axs[1], cmap="magma",
             plot_xlim=(25, 89), statistic="mean", vmax=0.2, binsize=3)
    rink.hexbin(shots.x, shots.y, values=shots.goal, ax=axs[2], binsize=(8, 12), plot_range="ozone", zorder=25, alpha=0.85)
