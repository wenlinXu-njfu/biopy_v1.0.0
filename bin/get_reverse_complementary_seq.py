#!/usr/bin/env python
"""
File: get_reverse_complementary_seq.py
Description: Get reverse complementary sequence
Date: 2022/6/8
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_file, out_file):
    content = ''
    for nucl_obj in Fasta(in_file).FASTA_generator(False):
        rev_com_seq = -nucl_obj
        if out_file:
            content += f">{rev_com_seq.id}\n{rev_com_seq.seq}\n"
        else:
            print(rev_com_seq)
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input FASTA sequence file.')
@click.option('-out', help='[optional] Output file, if not specified, print results to terminal as stdout.')
def run(in_file, out):
    """Get reverse complementary sequence."""
    main(in_file, out)


if __name__ == '__main__':
    run()
