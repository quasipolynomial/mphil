#! /usr/bin/python2.7

"""
Main logic
"""

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
# Todo find more instances
# DONE Todo check for k-local consistency
# DONE Todo Build graphs
#   2 kinds of graphs
#   convert
#   check if has any auto
#   auto, k locally, uniquely sat,
# DONE Todo RUN Through traces and check if graph has nothing other than trivial automorphisms
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
    def generate_n_m(self, **kwargs):
        """
        Generate instances
        :param kwargs: 
        :return: 
        """
        sat = Sat()
        ph = PlotHandler()
        fh = FileHandler()
        data = sat.generate_systems(**kwargs)

    def plot_n_m_results(self, filename, **kwargs):
        """
        Plot time taken to generate instances
        :param filename: 
        :param kwargs: 
        :return: 
        """
        ph = PlotHandler()
        fh = FileHandler()
        data = fh.read_from_file(filename, kwargs)
        ph.plot_sat_results(data)

    def generate_graphs(self, **kwargs):
        """
        Run graphs through Traces
        :param kwargs: 
        :return: 
        """
        gi = Gi()
        if kwargs.get("graphs"):
            graphs = kwargs.get("graphs")
            gi.run_graphs(graphs, kwargs)
        else:
            gi.run_all_graphs(kwargs)

    def plot_graphs_results(self, **kwargs):
        """
        Plot time taken to run graphs through Traces
        :param kwargs: 
        :return: 
        """
        ph = PlotHandler()
        gi = Gi()
        results = gi.load_results()
        ph.plot_gi_results(results, kwargs)

    def timed_n_m(self):
        """
        Time execution time of running instances through Sat Solver
        :return: 
        """
        sat = Sat()
        sat.run_solver()

    def plot_timed_n_m(self):
        """
        Plot execution time of running instances through Sat Solver
        :return: 
        """
        sat = Sat()
        ph = PlotHandler()
        results = sat.load_results()
        ph.plot_gauss_results(results)

    def construct(self):
        """
        Convert found systems into graphs and run them through Traces
        :return: 
        """
        # Init
        gi = Gi()
        sat = Sat()
        ph = ProcessHandler()
        fh = FileHandler()
        paths = ph.run_command("ls -v ./../assets/systems_to_convert/")

        # Iterate systems
        for path in paths:
            # Paths
            graph_path = "./../assets/construction/" + path + "_A.dre"
            system_path = "./../assets/systems_to_convert/" + path

            # Extract n and m values
            n, m = path.split("_")
            n = int(n)
            m = int(m)

            # Load system
            system = fh.read_from_file(system_path)

            # Check for k-local consistency
            if not sat.is_k_consistent(n, m, system):
                continue

            # Convert system into graphs and check for automorphisms
            G = sat.convert_system_to_graph(n, m, system)
            gi.convert_graph_to_traces(n, m, G, "A")  # First construction
            if not gi.graph_has_automorphisms(graph_path):
                gi.convert_graph_to_traces(n, m, G, "B")  # Second construction
            else:
                ph.run_command("rm " + graph_path)

    def time_constructions(self):
        """
        Run new constructions through Traces
        :return: 
        """
        gi = Gi()
        ph = PlotHandler()
        graphs = {
            "construction_custom": gi.load_graphs()["construction_custom"]
        }
        results = gi.run_graphs(graphs)
        ph.plot_gi_results(results)


if __name__ == "__main__":
    """
    Command line handling
    """
    main = Main()
    main.generate_n_m(n=1000,
                      min_m=1000,
                      max_n=10000,
                      max_m=10000,
                      step=100,
                      save_results=False,
                      save_systems=True,
                      limit=5,
                      bound=False,
                      max_tries=20)

    exit()
    
    gi = Gi()
    main.construct()
    pass

    # main.generate_graphs(outstanding=False,
    #                      timeout=False,
    #                      save=True)
    #
    # main.plot_graphs_results(save=True)

    # Find
    main.generate_n_m(n=1000,
                      min_m=1000,
                      max_n=10000,
                      max_m=10000,
                      step=100,
                      save_results=False,
                      save_systems=False,
                      limit=10,
                      bound=True,
                      max_tries=10)
    main.plot_n_m_results('./../assets/sat_run/0-n-10000_0-m-10000_step-100/results', aggregate=True)

    # Sat Solver
    # main.timed_n_m()
    # main.plot_timed_n_m()

    sat = Sat()
    # x = sat.find_equations(5, 6)
    # for i in x:
    #     print x.count(i), sat.is_system_uniquely_satisfiable(i, 5)
    #     for j in x:
    #         if i == j:
    #             continue

    fh = FileHandler()
    # system = fh.read_from_file("./../assets/systems/5_5")
    # n = 5
    # m = 5
    m = 1
    n = 3
    system = [[1, 2, 3]]
    G = sat.convert_system_to_construction(n, m, system)
    gi.convert_graph_to_traces_format(n, m, G, "B")

    pass
