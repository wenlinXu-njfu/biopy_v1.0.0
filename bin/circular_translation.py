#!/usr/bin/env python
"""
File: circular_translation.py
Description: 
Date: 2022/5/5
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.sequence import Nucleotide
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(fa_file, parse_seqids: click.Choice(['yes', 'no']), out_file_prefix, min_len: int = None):
    if parse_seqids == 'yes':
        parse_seqids = True
    else:
        parse_seqids = False
    content1 = content2 = ''
    for nucl in Fasta(fa_file).FASTA_generator(parse_seqids):
        _id = nucl.id
        nucl.id = f"{_id} | plus"
        generator1 = nucl.circular_translation()
        rev = Nucleotide(f"{_id} | minus", nucl.seq[::-1])
        generator2 = rev.circular_translation()
        for t in generator1:
            cds, pep = t[0], t[1]
            cds = cds.display_set()
            pep = pep.display_set()
            if not min_len:
                if len(pep) >= len(nucl):
                    if out_file_prefix:
                        content1 += f">{cds.id}\n{cds.seq}"
                        content2 += f">{pep.id}\n{pep.seq}"
                    else:
                        print(cds.display_set())
                        print(pep.display_set())
            else:
                if len(pep) >= min_len:
                    if out_file_prefix:
                        content1 += f">{cds.id}\n{cds.seq}"
                        content2 += f">{pep.id}\n{pep.seq}"
                    else:
                        print(cds.display_set())
                        print(pep.display_set())
        for t in generator2:
            cds, pep = t[0], t[1]
            cds = cds.display_set()
            pep = pep.display_set()
            if not min_len:
                if len(pep) >= len(nucl):
                    if out_file_prefix:
                        content1 += f">{cds.id}\n{cds.seq}"
                        content2 += f">{pep.id}\n{pep.seq}"
                    else:
                        print(cds.display_set())
                        print(pep.display_set())
            else:
                if len(pep) >= min_len:
                    if out_file_prefix:
                        content1 += f">{cds.id}\n{cds.seq}"
                        content2 += f">{pep.id}\n{pep.seq}"
                    else:
                        print(cds.display_set())
                        print(pep.display_set())
    if out_file_prefix:
        with open(f'{out_file_prefix}_cds.fa', 'w') as o:
            o.write(content1)
        with open(f'{out_file_prefix}_pep.fa', 'w') as o:
            o.write(content2)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input nucleotide sequence FASTA file.')
@click.option('-parse_seqids', type=click.Choice(['yes', 'no']), default='yes',
              help='[optional] Specify whether parse sequence IDs. {default=yes}')
@click.option('-min', 'minimal', type=int,
              help='[optional] Specify minimal length of peptide chain. {default=length of sequence itself}')
@click.option('-out', help='[optional] Output file prefix, if not specified, print results to terminal as stdout.')
def run(in_file, parse_seqids, out, minimal):
    main(in_file, parse_seqids, out, minimal)


if __name__ == '__main__':
    run()
