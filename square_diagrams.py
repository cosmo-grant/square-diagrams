# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 16:28:55 2020

@author: Cosmo

Makes square diagrams using tikz and matplotlib.

A square diagram is a square divided into columns of different widths, and
each column divided into rectangles of different heights. It can be used, for
example, to represent a Bayesian experiment: a hypothesis's prior is
represented by the corresponding column's width, and the likelihood of an
outcome given the hypothesis is represented by the corresponding rectangle's
height.

In addition, by making all rectangles except those corresponding to a
particular outcome semi-transparent, a square diagram also helps illustrate
Bayes Theorem.

The function tikz_square_diagram prints tikz instructions. (TikZ is a LaTeX
package.) If you copy and paste the instructions into your LaTeX document, with
the tikz package installed, it will make a square diagram. The function
plt_square_diagram is similar, but creates a matplotlib figure instead, so
doesn't require LaTeX.
"""


import itertools
import more_itertools
import matplotlib.pyplot as plt


### TIKZ SQUARE DIAGRAMS ###


def cum_steps(lst):
    """Returns a stream of pairs, overlapping, in the accumulated list.

    For example, [1, 2, 3, 4] -> (0, 1), (1, 3), (3, 6), (6, 10).
    """
    return more_itertools.pairwise(
        itertools.accumulate([0] + lst))


def tikz_rectangle(x1, y1, x2, y2, label, color, opaque):
    """Prints a tikz instruction to draw a filled, labeled rectangle.

    Args:
        x1, y1, x2, y2: Floats. Coordinates of bottom-left and top-right of rectangle.
        label: String. The rectangle's label.
        color: String. The rectangle's fill color.
        opaque: Boolean flag for whether to make the rectangle semi-transparent.
    """

    opacity_inst = '' if opaque else ', opacity=0.15'

    # rectangle has non-zero height
    if y2 > y1:
        print('\t'
              f'\\filldraw[draw=black, fill={color}!50' + opacity_inst + ']'
              f'({x1},{y1}) rectangle ({x2},{y2}) '
              f'node[midway] {{{label}}};'
        )


def make_column(x1, x2, yy, labels, colors, special_label):
    """Prints tikz instructions for one column of a square diagram.

    Args:
        x1, x2: X-coordinates of left and right of column
        yy: Stream of pairs of y-coordinates of rectangles.
        labels: List of strings. The rectangles' labels.
        colors: List of strings. The rectangles' fill colors.
        special_label: Label of special rectangle, if any, or else None.
          If there is a special rectangle, all the other rectangles should be
          semi-transparent.
    """

    for (y1, y2), label, color in zip(yy, labels, colors):
        opaque = (not special_label or label == special_label)
        tikz_rectangle(x1, y1, x2, y2, label, color, opaque)


def label_column(x1, x2, label):
    """Prints a tikz instruction to add a column label."""

    label_x = .5 * (x1 + x2)
    label_y = -1/16
    print(f'\t\\node at ({label_x},{label_y}) {{{label}}};')


def tikz_square_diagram(widths,
                        heights_matrix,
                        col_labels=None,
                        rect_labels=None,
                        colors=None,
                        special_label=None):
    """Prints tikz instructions for making a square diagram.

    Args:
        widths: List of floats, representing the column widths.
        heights_matrix: List of lists of floats.
          The i,j entry is the height of rectangle j in column i.
        col_labels: List of strings. The column labels.
        rect_labels: List of strings. The rectangle labels.
        colors: List of strings. The rectangle colors.
        special_label: Label of special rectangle, if any, else None.
          If there is a special rectangle, all the other rectangles should be
          semi-transparent.
    """

    if col_labels is None:
        num_cols = len(widths)
        col_labels = [f'$h_{{{i}}}$' for i in range(1, num_cols + 1)]

    if rect_labels is None:
        num_rectangles = len(heights_matrix[0])
        rect_labels = [str(i) for i in range(1, num_rectangles + 1)]

    if colors is None:
        colors = ['red', 'green', 'blue', 'yellow', 'magenta', 'olive',
                  'violet', 'brown', 'teal', 'orange', 'purple', 'cyan']

    print('\\begin{tikzpicture}[scale=8]\n')

    xx = cum_steps(widths)

    for (x1, x2), heights, col_label in zip(xx, heights_matrix, col_labels):
        yy = cum_steps(heights)
        make_column(x1, x2, yy, rect_labels, colors, special_label)
        label_column(x1, x2, col_label)
        print()

    print('\\end{tikzpicture}')


### PLT SQUARE DIAGRAMS ###


def plt_square_diagram(widths,
                       heights_matrix,
                       col_labels=None,
                       rect_labels=None,
                       colors=None,
                       special_label=None):
    """Makes square diagram with matplotlib.

    Args:
        widths: List of floats. The widths of the columns.
        heights_matrix: List of lists of floats.
          The i,j entry is the height of rectangle j in column i.
        col_labels: List of strings. The column labels.
        rect_labels: List of strings. The rectangle labels.
        colors: List of strings. The rectangle colors.
        special_label: Label of special rectangle, if any, else None.
          If there is a special rectangle, all the other rectangles should be
          semi-transparent.
    """
    if col_labels is None:
        num_cols = len(widths)
        col_labels = [str(i) for i in range(1, num_cols + 1)]

    if rect_labels is None:
        num_rectangles = len(heights_matrix[0])
        rect_labels = [str(i) for i in range(num_rectangles)]

    if colors is None:
        colors = ['orange', 'lightgreen', 'yellow', 'hotpink',
                  'lightseagreen', 'tomato', 'beige', 'khaki',
                  'cyan', 'lightsalmon', 'thistle', 'gainsboro',
                  'lavenderblush', 'goldenrod', 'lightskyblue', 'greenyellow']

    fig, ax = plt.subplots()

    xx = cum_steps(widths)

    for (x1, x2), heights, col_label in zip(xx, heights_matrix, col_labels):

        ax.text(
            .5 * (x1 + x2),
            -.2,
            col_label,
            fontsize=14,
            horizontalalignment='center',
        )

        yy = cum_steps(heights)

        for (y1, y2), rect_label, color in zip(yy, rect_labels, colors):

            if y2 > y1:
                alpha = .1 if (special_label and rect_label != special_label) else .8
                ax.fill_between(
                    [x1, x2],
                    y1,
                    y2,
                    color=color,
                    edgecolor='black',
                    alpha=alpha,
                )
                ax.text(.5 * (x1 + x2),
                        .5 * (y1 + y2),
                        rect_label,
                        horizontalalignment='center',
                        verticalalignment='center',
                )

    ax.set_aspect('equal')
    ax.autoscale(tight=True)

    return fig, ax


# EXAMPLE

# list_of_priors = [4/8, 1/8, 3/8]
# matrix_of_likelihoods = [[.092, .299, .368, .200, .041],
#                          [.063, .250, .375, .250, .063],
#                          [.041, .200, .368, .299, .092]]
# tikz_square_diagram(list_of_priors, matrix_of_likelihoods)
# plt_square_diagram(list_of_priors, matrix_of_likelihoods)

