#!/usr/bin/env python
"""
File: FPKM.py
Description: Standardize gene expression with FPKM.
Date: 2022/12/2
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
import pandas as pd
from Biolib.statistics import merge_duplicate_indexes, filter_by_min_value
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
file_content = """
Geneid  Length Sample1 Sample2 Sample3 ...\n
gene1   2000     1       0       0    ...\n
gene2   1000     21      51      34   ...\n
......  ...... ....... ....... ....... ...\n
gene100 2100    2345    2137    1987  ...\n
"""


def get_FPKM(exp_matrix_file: str, out_file_prefix: str, min_value: float = None) -> None:
    """
    Standardize gene expression with FPKM
    :param exp_matrix_file: Gene expression matrix file (txt, xls, xlsx, or csv format).

            Geneid     Length   Sample1   Sample2   Sample3
            gene1      200         1         0         0
            gene2      1000       21        51        34
            ......     .......   .......   .......   .......
            gene1000   2100      2345      2137      1987

    :param min_value: Gene minimum expression (genes whose expression is less than the specified value in all samples
            are filtered out).
    :param out_file_prefix: Output file prefix. {default=FPKM}
    :return: None
    """
    df_dict = {'txt': pd.read_table, 'xls': pd.read_excel, 'xlsx': pd.read_excel, 'csv': pd.read_csv}
    df = df_dict[exp_matrix_file.split('.')[-1]](exp_matrix_file, index_col=0)
    df = merge_duplicate_indexes(df)
    div_gene_length = df.div(df['Length'], axis=0)
    read_sum = df.sum(axis=0)
    div_gene_length.loc['sum'] = read_sum
    div_read_num = div_gene_length.div(div_gene_length.loc['sum'].T, axis=1) * 1000000000
    FPKM = div_read_num.iloc[0:-1, 1:]
    raw_gene_num = len(FPKM.index.tolist())
    if min_value:
        FPKM = filter_by_min_value(FPKM, min_value=min_value)
        new_gene_num = len(FPKM.index.tolist())
        click.echo(f"{raw_gene_num - new_gene_num} genes have been filtered out", err=True)
    FPKM.to_excel(f'./{out_file_prefix}.xlsx')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'exp', help=f"""Gene expression matrix file (txt, xls, xlsx, or csv format).
                                 \033[33m\n{file_content}\033[0m""")
@click.option('-min', 'min_exp', type=float, default=0,
              help='[optional] Gene minimum expression threshold in all samples. {default=0}')
@click.option('-out', default='FPKM', help='[optional] Output file prefix. {default=FPKM}')
def run(exp, min_exp, out):
    """Standardize gene expression with FPKM."""
    get_FPKM(exp, out, min_exp)


if __name__ == '__main__':
    run()
