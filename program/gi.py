import re
import signal
from handlers.exceptionhandler import signal_handler, TimeoutError
from handlers.filehandler import FileHandler
from handlers.processhandler import ProcessHandler
import networkx as nx
import numpy as np


class Gi(object):
    def generate_graphs(self, **kwargs):
        """
        Run all/some graphs on dreadnaut
        :param kwargs: 
        :return: 
        """
        # Init
        fh = FileHandler()
        ph = ProcessHandler()
        results = {}
        graphs = self.load_graphs()
        run = ph.run_command("ls -v ./../assets/graphs_run/")

        for graph in graphs:
            # Skip existing graphs
            if kwargs.get("outstanding", False) and graph + ".txt" in run:
                continue

            # Gather results
            graph_results = []
            for graph_instance in graphs[graph]:
                print graph_instance
                graph_results.append(self.run_graph_instance(graph, graph_instance, **kwargs))
            results[graph] = graph_results

            # Save
            if kwargs.get("save", False):
                fh.write_to_file("./../assets/graphs_run/" + graph + ".txt", graph_results)
        return results

    def run_graph_instance(self, graph, graph_instance, **kwargs):
        """
        Run a specific instance on dreadnaut
        :param graph: 
        :param graph_instance: 
        :param kwargs: 
        :return: 
        """
        # Init
        ph = ProcessHandler()
        path = "./../assets/graphs/" + graph + "/" + graph_instance
        nodes = re.search("(n=?)=\d+", ' '.join(ph.run_command("head '" + path + "'"))).group(0)[2:]
        process = ph.open_process("dreadnaut")

        # Set timeout
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(kwargs.get("timeout", 0))

        # Gather results
        try:
            time, (stdout, stderr) = ph.run_function_timed(process.communicate, ('At -a V=0 -m <"' + path + '" x q',),
                                                           return_args=True)
            split = re.search('(time=?) = \d+.\d+\d+', stdout)
            if split:
                d_time = split.group(0)[7:]
            else:
                time = -1
                d_time = -1

        except TimeoutError:
            print "Timed out: Took too long to validate"
            time = -1
            process.kill()
            process.terminate()
        finally:
            signal.alarm(0)

        return {
            "name": graph_instance,
            "nodes": nodes,
            "time": time,
            "d_time": d_time
        }

    def load_graphs(self):
        """
        Load graph instances from package
        :return: 
        """
        ph = ProcessHandler()
        graphs = {}
        for graph in ph.run_command('ls -v ./../assets/graphs/'):
            graphs[graph] = []
            for graph_instance in ph.run_command('ls -v ./../assets/graphs/' + graph):
                graphs[graph].append(graph_instance)
        return graphs

    def load_results(self):
        """
        Load results from tests
        :return: 
        """
        ph = ProcessHandler()
        fh = FileHandler()
        results = {}
        graphs = self.load_graphs()
        run = ph.run_command("ls -v ./../assets/graphs_run/")
        for graph in graphs:
            if graph + ".txt" in run:
                results[graph] = fh.read_from_file("./../assets/graphs_run/" + graph + ".txt")
        return results

    def generate_random_graph(self):
        nodes = [6000, 7000, 8000, 9000, 10000]
        fh = FileHandler()
        for i in nodes:

            # Build matrix
            output = ["$=1 n={0} g".format(i)]
            g = nx.gnp_random_graph(i, 0.5)
            matrix = np.triu(nx.to_numpy_matrix(g))
            r = 1
            for row in matrix:
                c = 1
                new_row = []
                for col in row:
                    if col == 1:
                        new_row.append(str(c))
                    c = c + 1
                if new_row:
                    line = " ".join(new_row)
                    line = str(r) + ": " + line
                    output.append(line)
                r = r + 1
            output[-1] = output[-1]+"."
            output.append("$$")

            # Output matrix to graph
            fh.write_to_file_simple("./../assets/graphs/ran2/custom"+str(i)+".dre", output)


x = Gi()
x.generate_random_graph()
