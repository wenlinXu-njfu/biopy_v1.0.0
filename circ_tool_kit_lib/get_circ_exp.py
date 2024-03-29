#!/usr/bin/env python
"""
File: get_circ_exp.py
Description: Standardize circRNAs expression with CPM.
Date: 2023/3/4
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.statistics import read_in_gene_expression_as_dataframe
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(BSJ_matrix_file, out_file):
    df = read_in_gene_expression_as_dataframe(BSJ_matrix_file)
    if isinstance(df, str):
        click.echo(df, err=True)
        exit()
    read_sum = df.sum(axis=0)
    df = df.div(read_sum, axis=1) * 10 ** 6
    df.to_csv(f'./{out_file}.csv')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input BSJ matrix file. (support format: txt, xls, xlsx, csv)')
@click.option('-out', default='circ_CPM', help='[optional] Output file prefix. {default=circ_CPM}')
def run(in_file, out):
    """Standardize circRNAs expression with CPM."""
    main(in_file, out)


if __name__ == '__main__':
    run()
