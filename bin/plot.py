#!/usr/bin/env python
"""
File: plot_figure.py
Description: 
Date: 2022/2/24
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from plot_lib.plot_venn import run as run1
from plot_lib.plot_volcano_figure import run as run2
from plot_lib.plot_heatmap import run as run3
from plot_lib.plot_cluster_heatmap import run as run4
from plot_lib.plot_gene_structure import run as run5
from plot_lib.plot_circos import run as run6
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def plot():
    """
    Program: Plot tools\n
    Version: 1.0.0\n
    Contact: WenlinXu \033[1m(wenlinxu.njfu@outlook.com)\033[0m
    """
    pass


plot.add_command(run1, name='venn')
plot.add_command(run2, name='volcano')
plot.add_command(run3, name='heatmap')
plot.add_command(run4, name='cluster_heatmap')
plot.add_command(run5, name='gene_structure')
plot.add_command(run6, name='circos')


if __name__ == '__main__':
    plot()
