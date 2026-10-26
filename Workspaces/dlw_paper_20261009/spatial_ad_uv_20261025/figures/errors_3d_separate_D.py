from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from plot_3d import draw
draw('D','separate','error')
