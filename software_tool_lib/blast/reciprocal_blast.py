#!/usr/bin/env python
"""
File: reciprocal_blast.py
Description: By reciprocal blast, obtain sequence pair that best match each other
Date: 2022/4/27
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.blast import Blast
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(blast1, blast2, top, out_file):
    pair_dict1 = Blast(blast1).get_pair_dict(top)  # {query1: {sbject1: [], sbject2: [], ...}, query2: {}, ...}
    pair_dict2 = Blast(blast2).get_pair_dict(top)  # {query1: {sbject1: [], sbject2: [], ...}, query2: {}, ...}
    content = ''
    for query, d1 in pair_dict1.items():
        for sbject, info in d1.items():
            try:
                queries = list(pair_dict2[sbject].keys())  # queries that sbject best align
            except KeyError:
                pass
            else:
                if query in queries:
                    if out_file:
                        content += f'{query}\t{sbject}\n'
                    else:
                        print(f'{query}\t{sbject}')
    if out_file and content:
        with open(out_file, 'w') as o:
            o.write(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in1', help='Input blast result file.')
@click.option('-in2', help='Input another blast result file.')
@click.option('-top', type=int, default=3, help='[optional] Specify max alignment num of each sequence. {default=3}')
@click.option('-out', help='[optional] Output file, if not specified, print result to terminal as stdout.')
def run(in1, in2, top, out):
    """By reciprocal blast, obtain sequence pair that best match each other."""
    main(in1, in2, top, out)


if __name__ == '__main__':
    run()
