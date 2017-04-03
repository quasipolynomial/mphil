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

    def time_n_m(self):
        sat = Sat()
        ph = PlotHandler()
        fh = FileHandler()
        path = './../assets/sat_run/0-n-10000_0-m-10000_step-100/'
        results = sat.compare_gauss(path)
        ph.plot_sat_results(results)

    def generate_graphs(self):
        ph = PlotHandler()
        gi = Gi()
        # results = gi.generate_graphs(outstanding=True, timeout=False, save=True)
        results = gi.load_results()
        ph.plot_gi_results(results, save=True)
        print results

    def time_n_m_new(self, **kwargs):
        sat = Sat()
        fh = FileHandler()
        ph = ProcessHandler()
        results = []
        skip = kwargs.get("outstanding", False)
        completed = []
        if fh.read_from_file("./../assets/systems_run/run"):
            for result in fh.read_from_file("./../assets/systems_run/run"):
                completed.append(result[0])

        for filename in ph.run_command('ls -v ./../assets/systems/'):
            # prep
            path = './../assets/systems/' + filename
            system = fh.read_from_file(path)
            split = filename.split("_")
            n = split[0]
            m = split[1]
            key = "{0}:{1}".format(n, m)
            if skip and key in completed:
                continue
            print key
            input = sat.prepare_cryptominisat_system(n, m, system)
            fh.write_to_file_simple("./../assets/systems_run/temp_storage", input)

            # run
            cmd = "./../assets/sat/cryptominisat/build/cryptominisat5 --verb=0 ./../assets/systems_run/temp_storage"
            time_a, out_a = ph.run_function_timed(ph.run_command, (cmd,), return_args=True)

            # run with gauss
            cmd = "./../assets/sat/cryptominisat/build_gauss/cryptominisat5 --verb=0 ./../assets/systems_run/temp_storage"
            time_b, out_b = ph.run_function_timed(ph.run_command, (cmd,), return_args=True)

            # Save
            results.append([key, n, m, time_a, time_b, time_b - time_a])
            fh.update_file("./../assets/systems_run/run", results)


if __name__ == "__main__":
    main = Main()
    gi = Gi()
    # gi.generate_random_graphs()
    gi.read_sparse_6_graphs()
    # main.generate_graphs()
    # main.generate_n_m()
    # main.time_n_m()
    # main.time_n_m_new(outstanding=False)
    # sat = Sat()
    # fh = FileHandler()
    # pl = PlotHandler()
    # results = fh.read_from_file("./../assets/systems_run/run")
    # pl.plot_gauss_results(results)
