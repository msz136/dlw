from plot_comparisons import *

if __name__ == "__main__":
    with np.load(HERE/"data"/"A.npz") as data:
        heatmaps("A",data,"final",max_table("final"))
