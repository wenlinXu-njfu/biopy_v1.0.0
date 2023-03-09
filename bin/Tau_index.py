#!/usr/bin/env python
"""
File: Tau_index.py
Description: Calculate gene expression tissue-specificity based on Tau index.
Date: 2022/10/27
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
import pandas as pd
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(exp_file, out_file_prefix):
    gene_exp_matrix = None
    exp_file_type_dict = {'txt': pd.read_table, 'xlsx': pd.read_excel, 'xls': pd.read_excel, 'csv': pd.read_csv}
    try:
        gene_exp_matrix = exp_file_type_dict[exp_file.split('.')[-1]](exp_file, index_col=0)
    except KeyError:
        file_format = exp_file.split('.')[-1]
        click.echo(f'\033[31mError: Unsupported format "{file_format}".\033[0m', err=True)
    if gene_exp_matrix is not None:
        df = gene_exp_matrix.copy()
        df['max'] = df.max(axis=1)
        for i in range(len(df.index.tolist())):
            df.iloc[i] = 1 - df.iloc[i] / df.iloc[i].max()
        df['max'] = df.sum(axis=1)
        df['Tau'] = df['max'] / (len(gene_exp_matrix.columns.tolist()) - 1)
        gene_exp_matrix['Tau'] = df['Tau']
        gene_exp_matrix.to_csv(f'{out_file_prefix}.csv')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input gene expression profile file. (support format: txt, xls, xlsx, csv)')
@click.option('-out', help='Output file path and prefix.')
def run(in_file, out):
    """Calculate gene expression tissue-specificity based on Tau index."""
    main(in_file, out)


if __name__ == '__main__':
    run()
