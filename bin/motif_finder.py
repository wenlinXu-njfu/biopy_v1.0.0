#!/usr/bin/env python
"""
File: motif_finder.py
Description: Find the motif in the sequence
Date: 2022/3/29
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(fasta_file, motif, log_file, out_file):
    fasta_file_obj = Fasta(fasta_file)
    content = 'Seq_id\tStart\tEnd\tMotif\n'
    for nucl_obj in fasta_file_obj.FASTA_generator():
        ret = nucl_obj.find_motif(motif)
        if 'not found' not in ret:
            content += ret
        else:
            click.echo(f"\033[33m{ret}\033[0m", err=True, file=open(log_file, 'a')) if log_file else \
                click.echo(f"\033[33m{ret}\033[0m", err=True)
    if out_file and len(content) > 23:
        with open(out_file, 'w') as o:
            o.write(content)
    elif not out_file and len(content) > 23:
        print(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input FASTA file.')
@click.option('-motif', help='Specify motif sequence, support for regular expressions.')
@click.option('-log', help='[optional] Output log file, if not specified, print log to terminal as stderr.')
@click.option('-out', help='[optional] Output file (seq_id\\tstart\\tend\\tmotif), if not specified, print results to '
                           'terminal as stdout.')
def run(in_file, motif, log, out):
    """Find the motif in the sequence."""
    main(in_file, motif, log, out)


if __name__ == '__main__':
    run()
