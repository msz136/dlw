from plot_comparisons import *

if __name__ == "__main__":
    with np.load(HERE/"data"/"C.npz") as data:
        heatmaps("C",data,"rate",max_table("rate"))
