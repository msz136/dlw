from plot_comparisons import *

if __name__ == "__main__":
    with np.load(HERE/"data"/"D.npz") as data:
        heatmaps("D",data,"final",max_table("final"))
