from plot_comparisons import *

if __name__ == "__main__":
    with np.load(HERE/"data"/"C.npz") as data:
        slices("C",data,"final",max_table("final"))
