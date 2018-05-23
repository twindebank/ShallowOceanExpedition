import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_template import FigureCanvas
from matplotlib.figure import Figure


class PrettyPlot:
    subplot_height = 6
    subplot_width = 10
    padding = 0
    hide_ax_borders = True
    hide_ax_ticks = True

    def __init__(self, n_rows=1, n_cols=1):
        self.fig = Figure(
            figsize=(self.subplot_width * n_cols + self.padding, self.subplot_height * n_rows + self.padding),
            # defaults to rc figure.figsize
            edgecolor='white'
        )
        self.canvas = FigureCanvas(self.fig)

    def add_bar_chart(self, bar_vals, bar_labels, x_axis_label='', y_axis_label='', position=111, title=''):
        ax = self.fig.add_subplot(position)

        ax.set_title(title, fontsize=10, color='#555555')
        ax.set_xlabel(x_axis_label, fontsize=12, color='#6E6D6C')
        ax.set_ylabel(y_axis_label, fontsize=12, color='#6E6D6C')

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

        ax.yaxis.grid(True, color='grey', linestyle='-', alpha=0.4, zorder=0)
        ax.tick_params(axis='both', colors='#6E6D6C')
        ax.set_ylim(0, 1.3 * max(bar_vals))
        rects = ax.bar(
            bar_labels,
            bar_vals,
            width=0.85,
            color='#5169A7',
            alpha=1,
            edgecolor='white',
            zorder=3,
            align='center'
        )
        autolabel(ax, rects)

    def save_fig(self, filepath):
        self.fig.savefig(filepath, bbox_inches='tight')


def autolabel(ax, rects):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                '%d' % int(height),
                ha='center', va='bottom', color='#5169A7', weight='bold')
