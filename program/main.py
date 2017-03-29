from sat import Sat
from gi import Gi
import signal
import timeit
import pprint
import random
from pycryptosat import Solver
from handlers.filehandler import FileHandler
from handlers.plothandler import PlotHandler


class Main(object):
    def generate_n_m(self):
        sat = Sat()
        ph = PlotHandler()
        fh = FileHandler()
        data = sat.generate_systems(n=0,
                                    min_m=0,
                                    max_n=1000,
                                    max_m=1000,
                                    step=10,
                                    save_results=True,
                                    save_systems=True)
        data = fh.read_from_file('./../assets/sat_run/0-n-200_0-m-200_step-5/results')
        ph.plot_sat_results(data)
        # step = 100
        # max_misses = 10
        # min_m = 5
        # n = 1000
        # max_n = 3000
        # max_m = 3000

    def generate_graphs(self):
        ph = PlotHandler()
        gi = Gi()
        results = gi.generate_graphs(outstanding=False, timeout=1, save=False)
        # results = gi.load_results()
        ph.plot_gi_results(results, save=True)
        print results


if __name__ == "__main__":
    main = Main()
    # main.generate_graphs()
    main.generate_n_m()
