import matplotlib.pyplot as plt
import numpy as np


class PlotOperations():

    def create_boxplot(self, data):
        # plt.style.use('_mpl-gallery')

        # make data:
        # np.random.seed(10)
        # d = np.random.normal((3, 5, 4), (1.25, 1.00, 1.25), (100, 3))

        d = data

        # plot
        fig, ax = plt.subplots()
        VP = ax.boxplot(d, positions=[2, 4, 6], widths=1.5, patch_artist=True,
                        showmeans=False, showfliers=False,
                        medianprops={"color": "white", "linewidth": 0.5},
                        boxprops={"facecolor": "C0", "edgecolor": "white",
                                  "linewidth": 0.5},
                        whiskerprops={"color": "C0", "linewidth": 1.5},
                        capprops={"color": "C0", "linewidth": 1.5})

        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
               ylim=(0, 8), yticks=np.arange(1, 8))

        plt.show()

    def create_lineplot(self, x_axis, y_axis):
        import matplotlib.pyplot as plt
        import numpy as np

        plt.style.use('_mpl-gallery')

        # make data
        # x = np.linspace(0, 10, 100)
        # y = 4 + 2 * np.sin(2 * x)
        x = x_axis
        y = y_axis

        # plot
        fig, ax = plt.subplots()

        ax.plot(x, y, linewidth=2.0)

        ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
               ylim=(0, 8), yticks=np.arange(1, 8))

        plt.show()


# fig, ax = plt.subplots()  # Create a figure containing a single axes.
# ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the axes.
# plt.show()

if __name__ == "__main__":
    data = (3, 5, 4), (1.25, 1.00, 1.25), (100, 3)
    x = np.linspace(0, 10, 100)
    y = 4 + 2 * np.sin(2 * x)
    pltops = PlotOperations()
    pltops.create_boxplot(data)
    pltops.create_lineplot(x, y)
