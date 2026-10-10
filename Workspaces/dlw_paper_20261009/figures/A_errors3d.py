from pathlib import Path
import runpy,sys
sys.argv=['plot_spatial_errors3d.py','A','errors']
runpy.run_path(str(Path(__file__).resolve().parents[1]/'plot_spatial_errors3d.py'),run_name='__main__')
