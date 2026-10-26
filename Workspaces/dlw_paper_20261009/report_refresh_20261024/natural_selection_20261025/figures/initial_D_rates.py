from plot_comparisons import *

if __name__ == "__main__":
    with np.load(HERE/"data"/"D.npz") as data:
        slices("D",data,"rate",max_table("rate"))
