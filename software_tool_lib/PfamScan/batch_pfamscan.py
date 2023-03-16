#!/usr/bin/env python
"""
File: batch_pfamscan.py
Description: Batch pfamscan with multiple FASTA files
Date: 2022/4/28
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import os
import click
from tqdm import tqdm
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(in_dir, pfamscan_database, out_dir):
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    files = os.listdir(in_dir)
    with tqdm(total=len(files)) as pbar:
        for file in files:
            os.system(command=f"pfam_scan.pl -fasta {in_dir}/{file} -dir {pfamscan_database} "
                              f"-outfile {out_dir}/{file}_pfamsacn_out.txt")
            pbar.update()


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_dir', help='Input FASTA file directory.')
@click.option('-db', help='Input PfamScan database.')
@click.option('-out', help='[optional] Output directory, if not exits, create automatically.')
def run(in_dir, db, out):
    """Batch pfamscan with multiple FASTA files."""
    main(in_dir, db, out)


if __name__ == '__main__':
    run()
