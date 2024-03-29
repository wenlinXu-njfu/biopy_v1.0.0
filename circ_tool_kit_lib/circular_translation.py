#!/usr/bin/env python
"""
File: circular_translation.py
Description: Prediction of circRNAs translation.
Date: 2022/5/5
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.sequence import Nucleotide
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(fa_file, out_file_prefix, min_len: int = None):
    content1 = content2 = ''
    for nucl in Fasta(fa_file).FASTA_generator():
        raw_id = nucl.id
        nucl.id = f"{raw_id} strand=forward"
        generator1 = nucl.circular_translation()
        rev = Nucleotide(f"{raw_id} strand=reverse", nucl.seq[::-1])
        generator2 = rev.circular_translation()
        isoform_num = 0
        for t in generator1:
            cds, pep = t[0], t[1]
            cds = cds.display_set()
            pep = pep.display_set()
            if not min_len:
                if len(pep) >= len(nucl):
                    isoform_num += 1
                    cds.id = cds.id.replace(raw_id, f'{raw_id}.{isoform_num}')
                    pep.id = pep.id.replace(raw_id, f'{raw_id}.{isoform_num}')
                    if out_file_prefix:
                        content1 += f">{cds.id}\n{cds.seq}"
                        content2 += f">{pep.id}\n{pep.seq}"
                    else:
                        print(cds.display_set())
                        print(pep.display_set())
            else:
                if len(pep) >= min_len:
                    isoform_num += 1
                    cds.id = cds.id.replace(raw_id, f'{raw_id}.{isoform_num}')
                    pep.id = pep.id.replace(raw_id, f'{raw_id}.{isoform_num}')
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
                    isoform_num += 1
                    cds.id = cds.id.replace(raw_id, f'{raw_id}.{isoform_num}')
                    pep.id = pep.id.replace(raw_id, f'{raw_id}.{isoform_num}')
                    if out_file_prefix:
                        content1 += f">{cds.id}\n{cds.seq}"
                        content2 += f">{pep.id}\n{pep.seq}"
                    else:
                        print(cds.display_set())
                        print(pep.display_set())
            else:
                if len(pep) >= min_len:
                    isoform_num += 1
                    cds.id = cds.id.replace(raw_id, f'{raw_id}.{isoform_num}')
                    pep.id = pep.id.replace(raw_id, f'{raw_id}.{isoform_num}')
                    if out_file_prefix:
                        content1 += f">{cds.id}\n{cds.seq}"
                        content2 += f">{pep.id}\n{pep.seq}"
                    else:
                        print(cds.display_set())
                        print(pep.display_set())
    if out_file_prefix:
        with open(f'./{out_file_prefix}_cds.fa', 'w') as o:
            o.write(content1)
        with open(f'./{out_file_prefix}_pep.fa', 'w') as o:
            o.write(content2)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input circRNA nucleotide sequence FASTA file.')
@click.option('-min', 'minimal', type=int,
              help='[optional] Specify minimal length of peptide chain. {default=length of sequence itself}')
@click.option('-out', help='[optional] Output file prefix, if not specified, print results to terminal as stdout.')
def run(in_file, out, minimal):
    """Prediction of circRNAs translation."""
    main(in_file, out, minimal)


if __name__ == '__main__':
    run()
