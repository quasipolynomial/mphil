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

            # # Check for k-local consistency
            if not sat.is_k_consistent(n, m, system):
                continue

            # Convert system into graphs and check for automorphisms
            G = sat.convert_system_to_graph(n, m, system)
            gi.convert_graph_to_traces(n, m, G, "A")  # First construction
            if not gi.graph_has_automorphisms(graph_path):
                G = sat.convert_system_to_construction(n, m, system)
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




# Tests

def test_1():
    """
    Threshold search 1: 1000 - 10000
    :return: 
    """
    main = Main()
    main.generate_n_m(n=1000,
                      min_m=1000,
                      max_n=10000,
                      max_m=10000,
                      step=100,
                      save_results=True,
                      save_systems=True,
                      limit=10,
                      bound=True,
                      max_tries=10,
                      threshold_search=True)
    main.plot_n_m_results('./../assets/sat_run/0-n-10000_0-m-10000_step-100/results', aggregate=True)


def test_2():
    """
    Search 1: 1 - 100
    :return: 
    """
    main = Main()
    main.generate_n_m(n=1,
                      min_m=1,
                      max_n=100,
                      max_m=100,
                      step=1,
                      save_results=False,
                      save_systems=True,
                      limit=False,
                      bound=False,
                      max_tries=10)


def test_2():
    """
    Search 2: 100 - 1000
    + 10
    :return: 
    """
    main = Main()
    main.generate_n_m(n=100,
                      min_m=100,
                      max_n=1000,
                      max_m=1000,
                      step=10,
                      save_results=False,
                      save_systems=True,
                      limit=False,
                      bound=False,
                      max_tries=10)


def test_3():
    """
    Search 3: 1000 - 10000
    + 100
    :return: 
    """
    main = Main()
    main.generate_n_m(n=1000,
                      min_m=1000,
                      max_n=10000,
                      max_m=10000,
                      step=100,
                      save_results=True,
                      save_systems=True,
                      limit=10,
                      bound=True,
                      max_tries=10)


def test_4():
    """
    Search 4: 10000 - 50000
    + 1000
    :return: 
    """
    main = Main()
    main.generate_n_m(n=10000,
                      min_m=10000,
                      max_n=50000,
                      max_m=50000,
                      step=1000,
                      save_results=False,
                      save_systems=True,
                      limit=5,
                      bound=True,
                      max_tries=5)


def test_5():
    """
    Run sat solver through saved instances
    :return: 
    """
    main = Main()
    main.timed_n_m()
    main.plot_timed_n_m()


def test_6():
    """
    Convert saved instances to graphs and run
    :return: 
    """
    main = Main()
    main.construct()
    # main.time_constructions()


def test_7():
    """
    Run saved .dre graphs through Traces and time results
    :return: 
    """
    main = Main()
    main.generate_graphs(outstanding=False,
                         timeout=False,
                         save=True)

    main.plot_graphs_results(save=True)


def test_8():
    """
    Use recursion to find instances for a given n and m rather than randomly searching
    :return: 
    """
    sat = Sat()
    x = sat.find_equations(5, 6)
    for i in x:
        print x.count(i), sat.is_system_uniquely_satisfiable(i, 5)
        for j in x:
            if i == j:
                continue


if __name__ == "__main__":
    """
    Command line handling
    """
    test_6()