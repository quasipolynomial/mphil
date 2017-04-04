from sat import Sat
from gi import Gi
import signal
import timeit
import pprint
import random
from pycryptosat import Solver
from handlers.filehandler import FileHandler
from handlers.plothandler import PlotHandler
from handlers.processhandler import ProcessHandler


class Main(object):
    def generate_n_m(self):
        sat = Sat()
        ph = PlotHandler()
        fh = FileHandler()
        # data = sat.generate_systems(n=0,
        #                             min_m=0,
        #                             max_n=10000,
        #                             max_m=10000,
        #                             step=100,
        #                             save_results=True,
        #                             save_systems=True)
        data = fh.read_from_file('./../assets/sat_run/0-n-10000_0-m-10000_step-100/results',
                                 aggregate=True)
        ph.plot_sat_results(data)

    def generate_graphs(self):
        ph = PlotHandler()
        gi = Gi()
        results = gi.run_all_graphs(outstanding=False,
                                    timeout=False,
                                    save=True)
        # ph.plot_gi_results(results, save=True)
        print results

    def time_n_m(self):
        sat = Sat()
        sat.run_solver()


if __name__ == "__main__":
    main = Main()
    main.generate_graphs()
    main.time_n_m()
