"""Shared figure typography and displayed endpoint precision for the 2HS report."""

PLOT_STYLE = '''# 图中文字与公式统一使用随 Matplotlib 提供的 STIX 字体。
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["STIXGeneral", "Times New Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "mathtext.default": "it",
    "text.usetex": False,
})'''


def apply_presentation(notebook):
    for cell in notebook.cells:
        if cell.id == "hs-prepare" and PLOT_STYLE not in cell.source:
            cell.source = cell.source.rstrip() + "\n\n" + PLOT_STYLE + "\n"
        if cell.id == "hs-reference":
            cell.source = cell.source.replace(
                ']).to_string(index=False))',
                ']).to_string(index=False, formatters={\n'
                '    "初始物理左端": "{:.1f}".format, "初始物理右端": "{:.1f}".format,\n'
                '    "FD 的 dx": "{:.6f}".format,\n'
                '}))',
            )
        if cell.id == "hs-two-initial":
            cell.source = cell.source.replace(
                ']).to_string(index=False))',
                ']).to_string(index=False, formatters={\n'
                '    "物理左端": "{:.1f}".format, "物理右端": "{:.1f}".format,\n'
                '    "FD dx": "{:.6f}".format,\n'
                '}))',
            )
    return notebook
