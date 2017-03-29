import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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
            else:
                plt.scatter(x, y)
        else:
            plt.plot(x, y)
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
        for graph in results:
            x_axis = []
            y_axis = []
            for result in results[graph]:
                print result
                if result['nodes'] in x_axis:
                    pos = x_axis.index(result["nodes"])
                    # y_axis[pos] = "%.2f" % (float(y_axis[pos]) + float(result["time"]) * 0.5) # avg
                    y_axis[pos] = y_axis[pos] if y_axis[pos] > result["time"] else result["time"]
                    continue
                x_axis.append(result['nodes'])
                y_axis.append(result['time'])
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

        self.plot_graph_2d("Sat run [insert run name]",
                           x,
                           y,
                           colour_z=z,
                           scatter=True,
                           x_label="N Values",
                           y_label="M Values")
