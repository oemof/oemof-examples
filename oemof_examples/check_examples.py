import os
from termcolor import colored
import matplotlib
import warnings

warnings.filterwarnings("ignore", "", UserWarning)
matplotlib.use('Agg')

package = "oemof.solph"  # e.g. "oemof.solph", "tespy", "windpowerlib"
version = "v0.4.x"  # e.g. "", "v0.2.x", "0.4.x"
debug = False  # If True script will stop if error is raised

fullpath = os.path.join(os.getcwd(), package, version)

checker = {}
number = 0

for root, dirs, files in os.walk(fullpath):
    for name in files:
        if name[-3:] == ".py":
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

print("******* TEST RESULTS ***********************************")

print("\n{0} examples tested.\n".format(number))

for k, v in checker.items():
    if v == "failed":
        print(k, colored(v, 'red'))
    else:
        print(k, colored(v, 'green'))
