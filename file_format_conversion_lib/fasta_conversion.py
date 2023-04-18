#!/usr/bin/env python
"""
File: fasta_conversion.py
Description: Make each sequence to be displayed on a single line or in multiple lines
Date: 2022/3/23
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_file, mode, out_file):
    fa_file_obj = Fasta(in_file)
    content = ''
    if mode == 'formal':
        for seq in fa_file_obj.merge_sequence():
            if not out_file:
                print(seq.strip())
            else:
                content += seq
    else:
        for line in fa_file_obj.split_sequence():
            if out_file:
                content += line
            else:
                print(line.strip())
    if out_file and content:
        with open(out_file, 'w') as o:
            o.write(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input FASTA file.')
@click.option('-mode', type=click.Choice(['formal', 'informal']),
              help='If formal specified, the FASTA file will show full sequence in one line. Otherwise, each sequence will'
                   ' show in many lines.')
@click.option('-out', help='[optional] Output file, if not specified, print results to terminal as stdout.')
def run(in_file, mode, out):
    """Make each sequence to be displayed on a single line or in multiple lines."""
    main(in_file, mode, out)


if __name__ == '__main__':
    run()
