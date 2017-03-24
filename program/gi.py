import subprocess as sub
import os
import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt
from out import Out


class Gi(object):
    def run_all_graphs(self):
        out = Out()
        graphs = self.load_graphs()
        results = self.run_outstanding_graphs(graphs)
        # results = {
        #     "latin-sw": out.read_from_file("./../assets/graphs_run/latin-sw.txt")
        # }
        # self.print_results(results)

    def run_command(self, command):
        p = os.popen(command, "r")
        out = []
        while 1:
            line = p.readline()
            if not line:
                break
            out.append(line.rstrip())
        return out

    def run_process(self, command, input):
        process = subprocess.Popen([command], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        return process.communicate(input=input)

    def load_graphs(self):
        graphs = {}
        for graph in self.run_command('ls -v ./../assets/graphs/'):
            graphs[graph] = []
            for graph_instance in self.run_command('ls -v ./../assets/graphs/' + graph):
                graphs[graph].append(graph_instance)
        return graphs

    def run_graphs(self, graphs):
        out = Out()
        results = {}
        for graph in graphs:
            result = self.run_graph(graphs, graph)
            results[graph] = result
            out.write_to_file("./../assets/graphs_run/" + graph + ".txt", result)
        return results

    def run_outstanding_graphs(self, graphs):
        out = Out()
        results = {}
        run = self.run_command("ls -v ./../assets/graphs_run/")
        for graph in graphs:
            if graph+".txt" in run:
                continue

            result = self.run_graph(graphs, graph)
            results[graph] = result
            out.write_to_file("./../assets/graphs_run/" + graph + ".txt", result)


    def run_graph(self, graphs, graph):
        results = []
        for graph_instance in graphs[graph]:
            print graph_instance
            results.append(self.run_graph_instance(graph, graph_instance))
        return results

    def run_graph_instance(self, graph, graph_instance):
        path = "./../assets/graphs/" + graph + "/" + graph_instance
        stdout, stderr = self.run_process("dreadnaut", 'At -a V=0 -m <"' + path + '" x q')
        nodes = re.search("(n=?)=\d+", ' '.join(self.run_command("head '" + path+"'"))).group(0)[2:]
        time = re.search("(time=?) = \d+.\d+\d+", stdout).group(0)[7:]

        return {
            "name": graph_instance,
            "nodes": nodes,
            "time": time
        }

    def print_results(self, results):
        for i in results:
            x_axis = []
            y_axis = []
            for result in results[i]:
                print result
                if result['nodes'] in x_axis:
                    pos = x_axis.index(result["nodes"])
                    # y_axis[pos] = "%.2f" % (float(y_axis[pos]) + float(result["time"]) * 0.5) # avg
                    y_axis[pos] = y_axis[pos] if y_axis[pos] > result["time"] else result["time"]
                    continue
                x_axis.append(result['nodes'])
                y_axis.append(result['time'])
            self.plot_graph_2d(i, x_axis, y_axis)

    def plot_graph_2d(self, title, x, y):
        plt.title(title)
        plt.xlabel('nodes')
        plt.ylabel('time (sec)')
        plt.plot(x, y)
        plt.scatter(x, y)
        plt.ylim(ymin=0)
        plt.yticks(np.arange(0, float(max(y)) + 0.01, 0.01))
        plt.grid()
        plt.show()


gi = Gi()
gi.run_all_graphs()
