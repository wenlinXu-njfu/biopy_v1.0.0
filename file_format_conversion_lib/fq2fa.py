#!/usr/bin/env python
"""
File: fq2fa.py
Description: Convert FASTQ to FASTA
Date: 2022/4/22
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
import gzip
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(fq_file, out_file):
    content = ''
    if fq_file.endswith('gz'):
        iter_obj = gzip.GzipFile(fq_file).__iter__()
        while True:
            try:
                line1 = str(iter_obj.__next__()).replace('b', '').replace("'", '')
                line2 = str(iter_obj.__next__()).replace('b', '').replace("'", '')
                str(iter_obj.__next__()).replace('b', '').replace("'", '')
                str(iter_obj.__next__()).replace('b', '').replace("'", '')
            except StopIteration:
                break
            else:
                if out_file:
                    content += line1.replace('@', '>').replace('\\n', '\n')
                    content += line2.replace('\\n', '\n')
                else:
                    print(line1.replace('@', '>').replace('\\n', ''))
                    print(line2.replace('\\n', ''))
    else:
        with open(fq_file) as f:
            while True:
                id_line = f.readline()
                seq_line = f.readline()
                f.readline()
                f.readline()
                if not id_line.strip():
                    break
                else:
                    if out_file:
                        content += f"{id_line.replace('@', '>')}{seq_line}"
                    else:
                        print(f"{id_line.replace('@', '>')}{seq_line.strip()}")
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input FASTQ file(XXX.fq) or FASTQ compressed files(XXX.fq.gz).')
@click.option('-out', help='[optional] Output file, if not specified, print results to terminal as stdout.')
def run(in_file, out):
    """Convert FASTQ to FASTA."""
    main(in_file, out)


if __name__ == '__main__':
    run()
