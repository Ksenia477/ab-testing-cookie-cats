"""Выполнить весь ноутбук и сохранить отчёт: python run_analysis.py."""

import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
for variable, folder in {
    "MPLCONFIGDIR": "matplotlib",
    "IPYTHONDIR": "ipython",
    "JUPYTER_RUNTIME_DIR": "jupyter/runtime",
}.items():
    directory = ROOT / ".cache" / folder
    directory.mkdir(parents=True, exist_ok=True)
    os.environ[variable] = str(directory)

import nbformat
from jupyter_client import KernelManager
from nbclient import NotebookClient
from nbconvert import HTMLExporter


def main():
    path = ROOT / "ab_test_cookie_cats.ipynb"
    notebook = nbformat.read(path, as_version=4)
    nbformat.validate(notebook)
    # Используем Python текущего окружения без установки глобального ядра.
    manager = KernelManager(kernel_name="python3")
    manager.kernel_spec.argv = [
        sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"
    ]
    client = NotebookClient(
        notebook,
        km=manager,
        timeout=180,
        allow_errors=False,
        resources={"metadata": {"path": str(ROOT)}},
    )
    print("Выполняю ноутбук с чистым ядром…", flush=True)
    client.execute(cleanup_kc=True)
    nbformat.write(notebook, path)

    exporter = HTMLExporter(template_name="lab")
    exporter.exclude_input = True
    exporter.exclude_input_prompt = True
    exporter.exclude_output_prompt = True
    exporter.mathjax_url = ""
    html, _ = exporter.from_notebook_node(notebook)
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True)
    (reports / "ab_test_report.html").write_text(html, encoding="utf-8")
    code_cells = sum(cell.cell_type == "code" for cell in notebook.cells)
    print(f"Готово: {code_cells} ячеек выполнены без ошибок.")
    print("Отчёт: reports/ab_test_report.html")
    print("Вывод для бизнеса: reports/business_summary.md")


if __name__ == "__main__":
    main()
