from plot_comparisons import *

if __name__ == "__main__":
    with np.load(HERE/"data"/"Sinusoidal.npz") as data:
        heatmaps("Sinusoidal",data,"final",max_table("final"))
