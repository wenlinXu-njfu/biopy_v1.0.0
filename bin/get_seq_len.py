#!/usr/bin/env python
"""
File: get_seq_len.py
Description: Get each sequence length of FASTA file
Date: 2022/3/25
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(fa_file, parse_seqids: click.Choice(['yes', 'no']), out_file):
    if parse_seqids == 'yes':
        parse_seqids = True
    else:
        parse_seqids = False
    content = ''
    for nucl_obj in Fasta(fa_file).FASTA_generator(parse_seqids):
        if out_file:
            content += nucl_obj.get_seq_len_info() + '\n'
        else:
            print(nucl_obj.get_seq_len_info())
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input FASTA file.')
@click.option('-parse_seqids', type=click.Choice(['yes', 'no']), default='yes',
              help='[optional] Specify whether parse sequence IDs. {default=yes}')
@click.option('-out', help='[optional] Output file(seq_id\\tseq_len\\n), if not specified, print results to terminal as stdout.')
def run(in_file, parse_seqids, out):
    """Get each sequence length of FASTA file"""
    main(in_file, parse_seqids, out)


if __name__ == '__main__':
    run()
