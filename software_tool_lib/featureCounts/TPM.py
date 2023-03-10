#!/usr/bin/env python
"""
File: TPM.py
Description: Standardize gene expression with TPM
Date: 2022/1/15
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import pandas as pd
import click
from Biolib.statistics import merge_duplicate_indexes, filter_by_min_value
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
file_content = """
# featureCounts command\n
Geneid  Chr  Start End Strand Length sample1 sample2 sample3 ...\n
gene1   Chr1  1000 3000   +    2000     1       0       0    ...\n
gene2   Chr2  1000 2000   -    1000     21      51      34   ...\n
......  ....  .... .... ..... ...... ....... ....... ....... ...\n
gene100 Chr19 2100 4200   -    2100    2345    2137    1987  ...
"""


def get_TPM(featureCounts_result_file: str, out_file: str, min_value: float = None) -> None:
    """
    Standardize gene expression with TPM
    :param featureCounts_result_file: gene expression matrix file generated by featureCounts software (TAB delimiters)

                                      # featureCounts command
                                      Geneid     Chr    Start    End    Strand   Length   sample1   sample2   sample3
                                      gene1      Chr01   100     300      +       200        1         0         0
                                      gene2      Chr02   1000    2000     -      1000       21        51        34
                                      ......     ......  .....   .....  ......   ......   .......   .......   .......
                                      gene1000   Chr19   2100    4200     -      2100      2345      2137      1987

    :param out_file: Gene minimum expression (genes whose expression is less than the specified value in all samples
                      are filtered out)
    :param min_value: output file {default=TPM.txt}
    :return: None
    """
    df = pd.read_table(featureCounts_result_file, header=1, index_col='Geneid').iloc[:, 4:]
    df = merge_duplicate_indexes(df)
    div_gene_length = df.div(df['Length'], axis=0)
    sum_df = div_gene_length.sum(axis=0)
    div_gene_length.loc['sum'] = sum_df
    TPM = (div_gene_length.div(div_gene_length.loc['sum'], axis=1) * 1000000).iloc[0:-1, 1:]
    raw_gene_num = len(TPM.index.tolist())
    if min_value:
        TPM = filter_by_min_value(TPM, min_value=min_value)
        new_gene_num = len(TPM.index.tolist())
        click.echo(f"{raw_gene_num - new_gene_num} genes have been filtered out", err=True)
    TPM.to_csv(out_file, sep='\t')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'exp', help=f"""Gene expression matrix file generated by featureCounts software. (TAB delimiters)
                                 \033[33m\n{file_content}\033[0m""")
@click.option('-min', 'min_exp', type=float, default=0,
              help='[optional] Gene minimum expression threshold in all samples. {default=0}')
@click.option('-out', default='TPM.txt', help='[optional] Output file. {default=TPM.txt}')
def run(exp, min_exp, out):
    """Standardize gene expression with TPM."""
    get_TPM(exp, out, min_exp)


if __name__ == '__main__':
    run()
