from pathlib import Path
import runpy,sys
sys.argv=['plot_comparison_fields.py','C','fields']
runpy.run_path(str(Path(__file__).resolve().parents[1]/'plot_comparison_fields.py'),run_name='__main__')
