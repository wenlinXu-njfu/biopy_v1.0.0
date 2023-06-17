#!/usr/bin/env python
"""
File: extract_single_sequence.py
Description: Extract one sub sequence from reference sequence file
Date: 2022/5/3
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(fasta_file, chr_num, start, end, strand, out_file):
    for nucl in Fasta(fasta_file).FASTA_generator():
        if nucl.id == chr_num:
            sub_seq = nucl[start - 1:end]
            if strand == '-':
                sub_seq = sub_seq.get_reverse_complementary_seq()
            sub_seq.id = f'{chr_num}:{start}-{end}({strand})'
            if out_file:
                with open(out_file, 'w') as o:
                    o.write(f">{sub_seq.id}\n{sub_seq.seq}\n")
            else:
                print(sub_seq)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-ref', help='Input reference sequence file. (format=FASTA)')
@click.option('-chr', 'chromosome', help='Specify chromosome number. (eg:Chr01)')
@click.option('-start', type=int, help='Specify start site on chromosome.')
@click.option('-end', type=int, help='Specify end site on chromosome.')
@click.option('-strand', type=click.Choice(['+', '-']), help='Specify the direction of the chain.')
@click.option('-out', help='[optional] Output file, if not specified, print result to terminal as stdout.')
def run(ref, chromosome, start, end, strand, out):
    """Extract one sub sequence from reference sequence file."""
    main(ref, chromosome, start, end, strand, out)


if __name__ == '__main__':
    run()
