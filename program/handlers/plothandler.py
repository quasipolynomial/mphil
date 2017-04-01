import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pyplot as PLT
from matplotlib import cm as CM
from matplotlib import mlab as ML
import numpy as np
from numpy.random import uniform, seed
from matplotlib.mlab import griddata
import matplotlib.pyplot as plt
import operator


class PlotHandler(object):
    def plot_graph_2d(self, title, x, y, **kwargs):
        # labels
        plt.title(title)
        plt.xlabel(kwargs.get("x_label", "Set X"))
        plt.ylabel(kwargs.get("y_label", "Set Y"))

        # Plotting
        if kwargs.get("scatter", False):
            if kwargs.get("colour_z", False):
                z = kwargs["colour_z"]
                plt.scatter(x, y, c=z, s=500)
                clb = plt.colorbar()
                clb.ax.set_title('Time(sec)')
            else:
                plt.scatter(x, y)
        else:
            plt.scatter(x, y)
            plt.plot(x, y)
        if kwargs.get("timed_out", False):
            timed_out = kwargs["timed_out"]
            plt.plot(x, timed_out, c='red')

        # Axis / Style
        plt.ylim(ymin=0)
        # plt.yticks(np.arange(0, float(max(y)) + 0.01, 0.01))
        plt.grid()

        # Save / Show
        if kwargs.get("save", False):
            plt.savefig("./../assets/graphs_run/" + title)
        if kwargs.get("hide", False):
            pass
        else:
            plt.show()
        plt.clf()

    def plot_graph_3d(self, data):
        x = []
        y = []
        z = []
        for r in data:
            if r[0] == 'key':
                continue
            elif r[4] > 0:
                x.append(r[1])
                y.append(r[2])
                z.append(r[4])
                print r[0], r[4]

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c='r', marker='o')
        ax.set_xlabel('N Values')
        ax.set_ylabel('M Values')
        ax.set_zlabel('Time (sec)')
        plt.show()

    def plot_gi_results(self, results, **kwargs):
        kwargs["x_label"] = "nodes"
        kwargs["y_label"] = "time(sec)"
        for graph in results:
            x_axis = []
            y_axis = []
            timed_out = []
            prev = -1
            i = 0
            for result in results[graph]:
                print result
                if result['nodes'] in x_axis:
                    # Some code to deal with nodes with multiple entries
                    pos = x_axis.index(result["nodes"])
                    # y_axis[pos] = "%.2f" % (float(y_axis[pos]) + float(result["time"]) * 0.5) # avg
                    y_axis[pos] = y_axis[pos] if y_axis[pos] > result["time"] else result["time"]
                    continue
                if result["time"] == -1:
                    result["time"] = prev["time"]
                    timed_out.append(i)
                x_axis.append(result['nodes'])
                y_axis.append(result['time'])
                prev = result
                i = i+1
            kwargs["timed_out"] = timed_out
            self.plot_graph_2d(graph, x_axis, y_axis, **kwargs)

    def plot_sat_results(self, data):
        x = []
        y = []
        z = []

        for r in data:
            if r[0] == 'key':
                continue
            elif r[4] > 0:
                x.append(r[1])
                y.append(r[2])
                z.append(r[4])

        self.plot_graph_2d("Sat run 0-n-10000_0-m-10000_step-100",
                           x,
                           y,
                           colour_z=z,
                           scatter=True,
                           x_label="N Values",
                           y_label="M Values")
        self.plot_graph_3d(data)

        # self.plot_graph_2d_heatmap("title", x, y, z)

    def plot_gauss_results(self, data):
        x = []
        y = []
        z = []
        for r in data:
            x.append(r[1])
            y.append(r[2])
            z.append(r[3])

        self.plot_graph_2d("Sat run 0-n-10000_0-m-10000_step-100",
                           x,
                           y,
                           colour_z=z,
                           scatter=True,
                           x_label="N Values",
                           y_label="M Values")
