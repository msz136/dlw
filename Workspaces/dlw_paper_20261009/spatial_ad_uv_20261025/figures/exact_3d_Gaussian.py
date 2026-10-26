from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from plot_exact_3d import draw
draw('Gaussian')
