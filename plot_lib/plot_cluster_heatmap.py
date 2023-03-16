#!/usr/bin/env python
"""
File: plot_cluster_heatmap.py
Description: Plot gene expression cluster heatmap
Date: 2022/4/27
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(gene_exp_file: str, index_col: str, color_map: str, out_file: str):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Arial'
    df = pd.read_table(gene_exp_file, index_col=index_col)
    sns.clustermap(df, cmap=color_map, standard_scale=0)
    plt.savefig(out_file)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input gene expression file. (TAB split)')
@click.option('-index_col', help='Specify column name of gene id.')
@click.option('-cmap', default='vlag', help='[optional] Color map. {default=vlag}')
@click.option('-out', default='cluster_heatmap.pdf', help='[optional] Output file. {default=cluster_heatmap.pdf}')
def run(in_file, index_col, cmap, out):
    """Plot gene expression cluster heatmap."""
    main(in_file, index_col, cmap, out)


if __name__ == '__main__':
    run()
