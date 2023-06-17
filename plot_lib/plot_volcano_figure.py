#!/usr/bin/env python
"""
File: plot_volcano_figure.py
Description: Plot the volcano of differentially expressed genes
Date: 2022/2/22
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, List, Union

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_file: str, log2fc: float, padj: float, figure_size: Union[Tuple, List], out_prefix: str, fmt: str):
    plt.rcParams['pdf.fonttype'] = 42
    plt.rcParams['font.family'] = 'Arial'
    df = pd.read_table(in_file, index_col='gene_id')
    df['-lg_p'] = -np.log10(df['padj'])  # calculate -log10(padj) for each gene
    # mark gene
    df['sig'] = 'normal'
    df.loc[(df.log2FoldChange > log2fc) & (df.padj < padj), 'sig'] = 'up'
    df.loc[(df.log2FoldChange < -log2fc) & (df.padj < padj), 'sig'] = 'down'
    # plot_figure scatter figure
    fig = plt.figure(figsize=figure_size)
    plt.scatter(df[df['sig'] == 'up']['log2FoldChange'], df[df['sig'] == 'up']['-lg_p'],
                color='salmon', marker='o', label='up', s=5)
    plt.scatter(df[df['sig'] == 'normal']['log2FoldChange'], df[df['sig'] == 'normal']['-lg_p'],
                color='lightgrey', marker='o', label='normal', s=5)
    plt.scatter(df[df['sig'] == 'down']['log2FoldChange'], df[df['sig'] == 'down']['-lg_p'],
                color='lightgreen', marker='o', label='down', s=5)
    plt.xlabel(r'$log_2Fold$' + ' Change')
    plt.ylabel(r'$-log_{10}P$' + ' adjust')
    plt.xlim([-max(abs(df['log2FoldChange'])), max(abs(df['log2FoldChange']))])
    plt.legend(loc='upper center')
    plt.savefig(f'{out_prefix}.{fmt}', bbox_inches='tight')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help="Expression matrix file. (header must including 'gene_id', 'padj' and 'log2FoldChange')")
@click.option('-log2fc', type=float, default=1.5, help='[optional] Set log2(fold change) as the threshold. {default=1.5}')
@click.option('-padj', type=float, default=0.05, help='[optional] Set padj as the threshold. {default=0.05}')
@click.option('-figsize', default='6,8', help='[optional] Specify figure size. {default=6,8}')
@click.option('-out', default='out', help='Prefix of output file. {default=out}')
@click.option('-fmt', default='pdf', help='Specify the format of output file. {default=pdf}')
def run(in_file, log2fc, padj, figsize, out, fmt):
    """Plot the volcano of differentially expressed genes."""
    figsize = [float(i) for i in figsize.split(',')]
    main(in_file, log2fc, padj, figsize, out, fmt)


if __name__ == '__main__':
    run()
