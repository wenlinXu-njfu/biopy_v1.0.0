#!/usr/bin/env python
"""
File: PCC.py
Description: Calculation of Pearson correlation coefficient from gene expression.
Date: 2022/9/10
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from scipy.stats import pearsonr
from Biolib.statistics import *
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(exp_matrix_file, out_prefix):
    df = read_in_gene_expression_as_dataframe(exp_matrix_file)
    if isinstance(df, str):
        click.echo(df, err=True)
        exit()
    else:
        i = 0
        j = 1
        content = 'Query\tSubject\tPCC\tP_value\n'
        if not out_prefix:
            print(content)
        while i < len(df.index.tolist()):
            while j < len(df.index.tolist()):
                x = df.iloc[i]
                y = df.iloc[j]
                r, p = pearsonr(x, y)
                if out_prefix:
                    content += f'{x.name}\t{y.name}\t{r}\t{p}\n'
                else:
                    print(f'{x.name}\t{y.name}\t{r}\t{p}')
                j += 1
            i += 1
            j = i + 1
        if out_prefix:
            with open(f'{out_prefix}.txt', 'w') as o:
                o.write(content)
        df = df.T
        df.columns.name = None
        df = df.corr()
        if out_prefix:
            df.to_excel(f'./{out_prefix}.xlsx')
        else:
            print(df)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input gene expression matrix file (including header). '
                                     'Supported formats: txt, xls, xlsx, csv')
@click.option('-out', help='[optional] Output file prefix, if not specified, print results to terminal as stdout.')
def run(in_file, out):
    """Calculation of Pearson correlation coefficient from gene expression."""
    main(in_file, out)


if __name__ == '__main__':
    run()
