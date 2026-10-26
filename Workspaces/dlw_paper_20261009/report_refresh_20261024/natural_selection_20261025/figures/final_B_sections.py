from plot_comparisons import *

if __name__ == "__main__":
    with np.load(HERE/"data"/"B.npz") as data:
        slices("B",data,"final",max_table("final"))
