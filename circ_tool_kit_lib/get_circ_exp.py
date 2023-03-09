#!/usr/bin/env python
"""
File: get_circ_exp.py
Description: Standardize circRNAs expression with CPM.
Date: 2023/3/4
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
import pandas as pd
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(BSJ_matrix_file, BSJ_matrix_file_format, out_file):
    df_dict = {'csv': pd.read_csv, 'xlsx': pd.read_excel, 'txt': pd.read_table}
    df = df_dict[BSJ_matrix_file_format](BSJ_matrix_file, index_col=0)
    read_sum = df.sum(axis=0)
    df = df.div(read_sum, axis=1) * 10 ** 6
    df.to_csv(f'{out_file}.csv')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input BSJ matrix file.')
@click.option('-type', 'input_type', type=click.Choice(['csv', 'xlsx', 'txt']), default='csv',
              help='Specify the format of BSJ matrix file. {default=csv}')
@click.option('-out', default='circ_CPM', help='[optional] Output file prefix. {default=circ_CPM}')
def run(in_file, input_type, out):
    """Standardize circRNAs expression with CPM."""
    main(in_file, input_type, out)


if __name__ == '__main__':
    run()
