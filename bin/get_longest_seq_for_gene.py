#!/usr/bin/env python
"""
File: get_longest_seq_for_gene.py
Description: Get the longest transcript of each gene
Date: 2022/3/26
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(fasta_file, regula_exp, inplace_id, out_file):
    fa_file_obj = Fasta(fasta_file)
    if inplace_id == 'yes':
        inplace_id = True
    elif inplace_id == 'no':
        inplace_id = False
    seq_dict = fa_file_obj.get_longest_seq(regula_exp, inplace_id)
    content = ''
    for seq_id, seq in seq_dict.items():
        if out_file:
            content += f">{seq_id}\n{seq}\n"
        else:
            print(f">{seq_id}\n{seq}")
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input FASTA file.')
@click.option('-r', help='The name of a gene represented by a regular expression.')
@click.option('-inplace_id', type=click.Choice(['yes', 'no']), default='no',
              help='[optional] Replace the longest sequence ID with unique ID {default=no}')
@click.option('-out', help='[optional] Output file, if not specified, print results to terminal as stdout.')
def run(in_file, r, inplace_id, out):
    """Get the longest transcript of each gene."""
    main(in_file, r, inplace_id, out)


if __name__ == '__main__':
    run()
