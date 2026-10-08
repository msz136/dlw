"""Apply the direct-tau cell while preserving the other numerical schemes."""
from pathlib import Path
import ast
import shutil

HERE = Path(__file__).resolve().parent
source = HERE/'dlw_numeric_cells.py'
backup = HERE/'before_direct_tau'/'dlw_numeric_cells.py'
if not backup.exists():
    shutil.copy2(source, backup)
text = source.read_text('utf-8')
tree = ast.parse(text)
lines = text.splitlines(keepends=True)
for node in tree.body:
    if (isinstance(node, ast.Assign) and len(node.targets)==1
        and isinstance(node.targets[0], ast.Subscript)
        and isinstance(node.targets[0].value, ast.Name)
        and node.targets[0].value.id=='CELLS'
        and isinstance(node.targets[0].slice, ast.Constant)
        and node.targets[0].slice.value=='sd'):
        lines[node.lineno-1:node.end_lineno] = [
            "from sd_tau_cell import CELLS_SD\nCELLS['sd'] = CELLS_SD\n"]
        break
text = ''.join(lines)
text = text.replace("w = v-delta0(u, ghosts, self.h) if self.kind == 'SD' else v",
                    'w = v')
text = text.replace("return u, w+delta0(u, ghosts, self.h) if self.kind == 'SD' else w",
                    'return u, w')
if 'from tau_report_cells import CELLS_UPDATE' not in text:
    text += '\nfrom tau_report_cells import CELLS_UPDATE\nCELLS.update(CELLS_UPDATE)\n'
ast.parse(text)
source.write_text(text, encoding='utf-8')
print('Direct tau cells integrated')
