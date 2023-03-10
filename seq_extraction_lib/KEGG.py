#!/usr/bin/env python
"""
File: KEGG.py
Description: Extract sequences from KEGG url.
Date: 2022/6/19
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import os
import click
import requests
from tqdm import tqdm
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_file, seq_type: click.Choice(['aaseq', 'ntseq']), out_file):
    set1 = set([line.strip() for line in open(in_file) if line.strip()])
    if os.path.exists(out_file):
        set2 = set(line.split(' ')[0].replace('>', '') for line in open(out_file) if line.startswith('>'))
        l = list(set1 - set2)
    else:
        l = list(set1)
    l.sort()
    with open(out_file, 'a') as o:
        with tqdm(total=len(l)) as pbar:
            for gene_id in l:
                url = f'https://rest.kegg.jp/get/{gene_id}/{seq_type}'
                response = requests.get(url)
                o.write(response.text)
                pbar.update()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input KEGG list file, one id per line. (eg. pop:112323434\\npop:112323435)')
@click.option('-type', 'seq_type', type=click.Choice(['aaseq', 'ntseq']), default='aaseq',
              help='Specified sequence type. {default=aaseq}')
@click.option('-out', help='Output FASTA file.')
def run(in_file, seq_type, out):
    """Extract sequences from KEGG url."""
    main(in_file, seq_type, out)


if __name__ == '__main__':
    run()
