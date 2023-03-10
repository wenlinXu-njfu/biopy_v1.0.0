#!/usr/bin/env python
"""
File: extract_miRNA.py
Description: Extract miRNA sequence from miRNA GFF file
Date: 2022/3/24
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import os
import click
from Biolib.gff import Gff
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(miRNA_gff_file, out_dir):
    if out_dir and not os.path.exists(out_dir):
        os.mkdir(out_dir)
    elif not out_dir:
        out_dir = './'
    gff_file_obj = Gff(miRNA_gff_file)
    primary = star = mature = ''
    for nucl_obj in gff_file_obj.miRNA_extraction():
        if 'star' in nucl_obj.id:
            star += f">{nucl_obj.id}\n{nucl_obj.seq}\n"
        elif 'mature' in nucl_obj.id:
            mature += f">{nucl_obj.id}\n{nucl_obj.seq}\n"
        else:
            primary += f">{nucl_obj.id}\n{nucl_obj.seq}\n"
    with open(f"{out_dir}/primary.fa", 'w') as o1:
        o1.write(primary)
    with open(f"{out_dir}/star.fa", 'w') as o2:
        o2.write(star)
    with open(f"{out_dir}/mature.fa", 'w') as o3:
        o3.write(mature)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input miRNA GFF file.')
@click.option('-out', help='[optional] Output directory, if the output directory does not exist, '
                           'it will be created automatically. {default=./}')
def run(in_file, out):
    """Extract miRNA sequence from miRNA GFF file"""
    main(in_file, out)


if __name__ == '__main__':
    run()
