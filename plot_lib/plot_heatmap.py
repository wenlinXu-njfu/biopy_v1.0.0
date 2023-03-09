#!/usr/bin/env python
"""
File: plot_heatmap.py
Description: Plot gene expression heatmap
Date: 2022/4/15
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(gene_exp_file: str, index_col: str, out_file: str):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Arial'
    df = pd.read_table(gene_exp_file, index_col=index_col)
    df = df + 1
    df = np.log2(df)
    sns.clustermap(df, cmap='Pastel1', yticklabels=False, col_cluster=False, z_score=0, figsize=(10, 20))
    plt.savefig(out_file)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input gene expression file. (TAB split)')
@click.option('-index_col', help='Specify column name of gene id.')
# @click.option('-cmap', default='vlag', help='[optional] Color map. {default=vlag}')
@click.option('-out', default='heatmap.pdf', help='[optional] Output file. {default=heatmap.pdf}')
def run(in_file, index_col, out):
    """Plot gene expression heatmap."""
    main(in_file, index_col, out)


if __name__ == '__main__':
    run()
