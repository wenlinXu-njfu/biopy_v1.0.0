#!/usr/bin/env python
"""
File: extract_seq_id.py
Description: Extract sequence IDs from hmmsearch results
Date: 2022/4/12
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import re
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(hmmseqrch_result_file, out_file):
    id_list = []
    for line in open(hmmseqrch_result_file):
        if line.startswith(' ') and not line.strip().startswith('---') and not line.strip().startswith('E-value'):
            split = re.sub(r' +', ' ', line.strip()).split(' ')
            seq_id = split[8]
            if seq_id not in id_list:
                id_list.append(seq_id)
        elif line.startswith('Domain'):
            break
    if out_file and id_list:
        with open(out_file, 'w') as o:
            o.write('\n'.join(id_list) + '\n')
    else:
        print('\n'.join(id_list))


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input hmmsearch results file.')
@click.option('-out', help='[optional] Output file, if not specified, print sequences id to terminal as stdout.')
def run(in_file, out):
    """Extract sequence IDs from hmmsearch results"""
    main(in_file, out)


if __name__ == '__main__':
    run()
