import os
from termcolor import colored
import matplotlib
from matplotlib import pyplot as plt
import warnings
from datetime import datetime
import subprocess
import nbformat
import tempfile

warnings.filterwarnings("ignore", "", UserWarning)
matplotlib.use('Agg')

package = "oemof.solph"  # e.g. "oemof.solph", "tespy", "windpowerlib"
version = "v0.4.x"  # e.g. "", "v0.2.x", "0.4.x"
debug = False  # If True script will stop if error is raised
exclude_notebooks = False
exclude_python_scripts = False


def notebook_run(path):
    """
    Execute a notebook via nbconvert and collect output.
    Returns (parsed nb object, execution errors)
    """
    dirname, __ = os.path.split(path)
    os.chdir(dirname)
    with tempfile.NamedTemporaryFile(suffix=".ipynb") as fout:
        args = [
            "jupyter",
            "nbconvert",
            "--to",
            "notebook",
            "--execute",
            "--ExecutePreprocessor.timeout=60",
            "--output",
            fout.name,
            path,
        ]
        subprocess.check_call(args)

        fout.seek(0)
        nb = nbformat.read(fout, nbformat.current_nbformat)

    errors = [
        output
        for cell in nb.cells
        if "outputs" in cell
        for output in cell["outputs"]
        if output.output_type == "error"
    ]

    return nb, errors


fullpath = os.path.join(os.getcwd(), package, version)

checker = {}
number = 0

start = datetime.now()

for root, dirs, files in sorted(os.walk(fullpath)):
    for name in sorted(files):
        if name[-3:] == ".py" and not exclude_python_scripts:
            fn = os.path.join(root, name)
            os.chdir(root)
            number += 1
            if debug:
                print(fn)
                exec(open(fn).read())
            else:
                try:
                    exec(open(fn).read())
                    checker[name] = "okay"
                except:
                    checker[name] = "failed"
        elif name[-6:] == ".ipynb" and not exclude_notebooks:
            fn = os.path.join(root, name)
            os.chdir(root)
            number += 1
            if debug:
                print(fn)
                notebook_run(fn)
            else:
                try:
                    notebook_run(fn)
                    checker[name] = "okay"
                except:
                    checker[name] = "failed"
        plt.close()


print("******* TEST RESULTS ***********************************")

print("\n{0} examples tested in {1}.\n".format(number, datetime.now()-start))

for k, v in checker.items():
    if v == "failed":
        print(k, colored(v, 'red'))
    else:
        print(k, colored(v, 'green'))
