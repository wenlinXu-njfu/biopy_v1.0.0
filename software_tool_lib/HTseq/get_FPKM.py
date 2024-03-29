#!/usr/bin/env python
"""
File: get_FPKM.py
Description: Standardize gene expression with FPKM based on HTSeq results.
Date: 2023/6/15
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from Biolib.statistics import click, pd, get_FPKM
from Biolib.gtf import Gtf
from Biolib.gff import Gff
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(header_file: str, htseq_file: str, anno_file: str, min_exp: float, out_prefix: str):
    parse_anno_file = {'gff': Gff, 'gff3': Gff, 'gtf': Gtf}
    file_obj = parse_anno_file[anno_file.split('.')[-1]](anno_file)
    length_dict = {}
    for line in file_obj.parse():
        if line[2] == 'exon':
            length = int(line[4]) - int(line[3]) + 1
            if isinstance(file_obj, Gff):
                transcript_id = line[-1]
            else:
                transcript_id = line[-2]
            if transcript_id in length_dict:
                length_dict[transcript_id] += length
            else:
                length_dict[transcript_id] = length
    columns = [line.strip() for line in open(header_file)]
    df = pd.read_table(htseq_file, index_col=0, names=columns).iloc[:-5]
    df.insert(0, 'length', 0)
    for transcript_id in df.index.tolist():
        df.loc[transcript_id, 'length'] = length_dict[transcript_id]
    print(df)
    FPKM = get_FPKM(df, min_exp)
    FPKM.to_csv(f'./{out_prefix}.csv')


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-header', help='Input header file. (eg. Gene_id\\nSample1\\nSample2\\netc\\n)')
@click.option('-htseq', help='Input Htseq output file.')
@click.option('-anno', help='Input genome annotation GFF or GTF file, must contain exon information.')
@click.option('-min', 'min_exp', type=float, default=0,
              help='[optional] Gene minimum expression threshold in all samples. {default=0}')
@click.option('-out', help='Prefix of output file.')
def run(header, htseq, anno, min_exp, out):
    """Standardize gene expression with FPKM based on HTSeq results."""
    main(header, htseq, anno, min_exp, out)


if __name__ == '__main__':
    run()
