from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure


class PrettyPlot:
    # general settings
    subplot_height = 6
    subplot_width = 10
    padding = 0
    hide_ax_borders = True
    hide_ax_ticks = True
    bar_width = 0.85

    # colors
    title_color = '#555555'
    axis_label_color = '#6E6D6C'
    grid_color = 'grey'
    bar_color = '#5169A7'
    axis_number_color = '#6E6D6C'

    def __init__(self, n_rows=1, n_cols=1):
        self.fig = Figure(
            figsize=(self.subplot_width * n_cols + self.padding, self.subplot_height * n_rows + self.padding),
            edgecolor='white'
        )
        self.canvas = FigureCanvas(self.fig)

    def add_bar_chart(self, bar_vals, bar_labels, x_axis_label='', y_axis_label='', position=111, title=''):
        ax = self.fig.add_subplot(position)

        ax.set_title(title, fontsize=10, color=self.title_color)
        ax.set_xlabel(x_axis_label, fontsize=12, color=self.axis_label_color)
        ax.set_ylabel(y_axis_label, fontsize=12, color=self.axis_label_color)

        if self.hide_ax_borders:
            ax.spines["top"].set_visible(False)
            ax.spines["bottom"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)

        if self.hide_ax_ticks:
            ax.tick_params(
                which='both',  # both major and minor ticks are affected
                bottom='off',  # ticks along the bottom edge are off
                top='off',  # ticks along the top edge are off
                left='off',  # ticks along the left edge are off
                right='off')  # ticks along the right edge are off

        ax.yaxis.grid(True, color=self.grid_color, linestyle='-', alpha=0.4, zorder=0)
        ax.tick_params(axis='both', colors=self.axis_number_color)
        ax.set_ylim(0, 1.3 * max(bar_vals))
        rects = ax.bar(
            bar_labels,
            bar_vals,
            width=self.bar_width,
            color=self.bar_color,
            alpha=1,
            edgecolor='white',
            zorder=3,
            align='center'
        )
        autolabel(ax, rects, self.bar_color)

    def save_fig(self, filepath):
        self.fig.savefig(filepath, bbox_inches='tight')


def autolabel(ax, rects, color):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '%d' % int(height),
                ha='center', va='bottom', color=color, weight='bold')
