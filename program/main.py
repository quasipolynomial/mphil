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


# Todo search for smaller range
# Todo find instances
# TODO Build graphs
#   2 kinds of graphs
#   convert
#   check if has any auto
#   auto, k locally, uniquely sat,
# DONE Todo Run on two different builds
# DONE Todo Save each system to file
# DONE Todo extending graphs (random ones)
# DONE Todo add timeouts to graphs
# DONE Todo Rerun and find times
# DONE Todo random graphs
# DONE Todo subsecond times
# DONE Todo gauss elim
# DONE TODO Run sat
# DONE TODO Run graphs
# DONE TODO Make graphs from output

class Main(object):
    def generate_n_m(self):
        sat = Sat()
        ph = PlotHandler()
        fh = FileHandler()
        # system = fh.read_from_file("./../assets/systems/2600_6900")
        # print sat.is_system_uniquely_satisfiable(system, 2600)
        data = sat.generate_systems(n=0,
                                    min_m=0,
                                    max_n=10000,
                                    max_m=10000,
                                    step=100,
                                    save_results=True,
                                    save_systems=True,
                                    limit=10,
                                    bound=False,
                                    max_tries=20)
        # data = fh.read_from_file('./../assets/s'
        #                          'at_run/0-n-10000_0-m-10000_step-100/results',
        #                          aggregate=True)
        ph.plot_sat_results(data)

    def generate_graphs(self):
        ph = PlotHandler()
        gi = Gi()
        graphs = {
            "triang": gi.load_graphs()["triang"]
        }
        results = gi.run_graphs(graphs)

        # results = gi.run_all_graphs(outstanding=False,
        #                             timeout=False,
        #                             save=True)
        # results = gi.load_results()
        ph.plot_gi_results(results, save=True)
        print results

    def time_n_m(self):
        sat = Sat()
        ph = PlotHandler()
        # sat.run_solver()
        results = sat.load_results()
        ph.plot_gauss_results(results)


if __name__ == "__main__":
    main = Main()
    # main.generate_graphs()
    main.generate_n_m()
    # main.time_n_m()
