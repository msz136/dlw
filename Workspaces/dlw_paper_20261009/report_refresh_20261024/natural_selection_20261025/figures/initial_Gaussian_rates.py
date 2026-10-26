from plot_comparisons import *

if __name__ == "__main__":
    with np.load(HERE/"data"/"Gaussian.npz") as data:
        slices("Gaussian",data,"rate",max_table("rate"))
