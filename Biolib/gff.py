"""
File: gff.py
Description: Instantiate a GFF file object
Date: 2021/11/27
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from typing import Union, List, Tuple, Dict
import re
import click
import numpy as np
import pandas as pd
from Biolib.fasta import Fasta
from Biolib.sequence import Nucleotide


class Gff:
    def __init__(self, path: str):
        self.path = path

# Basic method==========================================================================================================
    def parse_GFF(self) -> Tuple[str]:
        """Parse information of each column of GFF file line by line."""
        for line in open(self.path):
            if not line.startswith('#') and line.strip():
                split = line.strip().split('\t')
                chr_num, source, feature = split[0], split[1], split[2]
                start, end, score, strand, frame = split[3], split[4], split[5], split[6], split[7]
                attr = split[-1].replace('=', ';').split(';')
                try:
                    feature_id = attr[attr.index('ID') + 1]
                except ValueError:
                    feature_id = None
                try:
                    feature_name = attr[attr.index('Name') + 1]
                except ValueError:
                    feature_name = None
                try:
                    parent_id = attr[attr.index('Parent') + 1]
                except ValueError:
                    parent_id = None
                yield chr_num, source, feature, start, end, score, strand, frame, feature_id, feature_name, parent_id

    def get_gff_dict(self, feature_type: str = None) -> Dict[str, List[Dict[str, Union[str, int]]]]:
        """Save the feature information in the GFF file into the dictionary."""
        # gff_dict = {
        #             Chr_num: [{id: str, start: int, end: int, strand: str}, {}, ...],
        #             Chr_num: [{}, {}, ...], ...
        #             }
        gff_dict = {}
        for line in self.parse_GFF():
            if line[2] == feature_type or feature_type is None:
                item = {'id': line[8], 'start': int(line[3]), 'end': int(line[4]), 'strand': line[6]}
                if line[0] in gff_dict:
                    gff_dict[line[0]].append(item)
                else:
                    gff_dict[line[0]] = [item]
        return gff_dict

    def get_mRNA_dict(self) -> dict:
        """Get mRNA dict. The start and end based on mRNA length, not based on chromosome length."""
        mRNA_dict = {}  # {mRNA_id: [{feature_type: str, start: int, end: int, strand: str}, {}, ...], ...}
        mRNA_id = None
        mRNA_start = 0
        mRNA_len = 0
        for line in self.parse_GFF():
            if line[2] == 'mRNA':
                mRNA_id = line[8]
                mRNA_start = int(line[3])
                mRNA_len = int(line[4]) - int(line[3]) + 1
                if mRNA_id not in mRNA_dict:
                    mRNA_dict[mRNA_id] = []
                else:
                    click.echo(f'\033[31mError: The GFF file has repeat id {mRNA_id}.\033[0m')
                    exit()
            elif line[2] == 'CDS' or 'UTR' in line[2]:
                if line[10] == mRNA_id:
                    if line[6] == '-':
                        start = mRNA_len - (int(line[4])-mRNA_start) - 1
                        end = mRNA_len - (int(line[3])-mRNA_start) - 1
                        item = {'feature_type': line[2], 'start': start, 'end': end, 'strand': line[6]}
                    else:
                        item = {'feature_type': line[2], 'start': int(line[3])-mRNA_start,
                                'end': int(line[4])-mRNA_start, 'strand': line[6]}
                    mRNA_dict[mRNA_id].append(item)
                else:
                    click.echo('\033[31mError: GFF file is not sorted by mRNA ID.\033[0m', err=True)
                    exit()
        return mRNA_dict

    def summary(self) -> str:
        """A peek at the genome."""
        feature_dict = {}
        for line in self.parse_GFF():
            if line[2] not in feature_dict:
                feature_dict[line[2]] = np.array([])
            feature_dict[line[2]] = np.append(feature_dict[line[2]], int(line[4]) - int(line[3]) + 1)
        content = f"## Summary of {self.path.split('/')[-1]}\nfeature\ttotal\tmin_len\tmax_len\tmedian_len\tmean_len\n"
        for key, value in feature_dict.items():
            try:
                content += f"{key}\t{len(value)}\t{value.min()}\t{value.max()}\t{np.median(value)}\t{'%.3f' % np.mean(value)}\n"
            except ValueError:
                content += f"{key}\t-\t-\t-\t-\t-\n"
        return content

# GFF file sorted by id method==========================================================================================
    @staticmethod
    def sort_by_chr_num(line):
        chr_num = int(re.findall(r'\d+', line.split('\t')[0])[0])
        return chr_num

    @staticmethod
    def sort_by_level1_id(line):
        split = line.strip().split('\t')
        attr = split[8].replace('=', ';').split(';')
        if split[2] == 'gene':
            level1_id = max(re.findall(r'\d+', attr[attr.index('ID') + 1]), key=len)
        else:
            level1_id = max(re.findall(r'\d+', attr[attr.index('Parent') + 1]), key=len)
        return level1_id

    @staticmethod
    def sort_by_level2_id(line):
        split = line.strip().split('\t')
        attr = split[8].replace('=', ';').split(';')
        if split[2] == 'gene':
            level2_id = '0'
        elif split[2] == 'mRNA':
            level2_id = re.findall(r'\.\d+\.', attr[attr.index('ID') + 1])[0].replace('.', '')
        else:
            level2_id = re.findall(r'\.\d+\.', attr[attr.index('Parent') + 1])[0].replace('.', '')
        return level2_id

    @staticmethod
    def sort_by_level3_id(line):
        split = line.strip().split('\t')
        attr = split[8].replace('=', ';').split(';')
        if split[2] == 'gene':
            level3_id = '0'
        elif split[2] == 'mRNA':
            level3_id = '0'
        else:
            level3_id = re.findall(r'\.\d+\.', attr[attr.index('ID') + 1])[1].replace('.', '')
        return level3_id

    def sort_by_id(self) -> str:
        """Sort the GFF file by sequence ID."""
        content = ''
        with open(self.path) as f:
            l = f.readlines()
            chr_list = [i for i in l if i.startswith('chr') or i.startswith('Chr')]
            contig_list = [i for i in l if
                           not i.startswith('chr') and not i.startswith('Chr') and not i.startswith('#')]
            chr_list.sort(
                key=lambda item: (int(self.sort_by_chr_num(item)), int(self.sort_by_level1_id(item)),
                                  int(self.sort_by_level2_id(item)), int(self.sort_by_level3_id(item)),
                                  int(item.split('\t')[3]), -int(item.split('\t')[4])))
            contig_list.sort(
                key=lambda item: (int(self.sort_by_chr_num(item)), int(self.sort_by_level1_id(item)),
                                  int(self.sort_by_level2_id(item)), int(self.sort_by_level3_id(item)),
                                  int(item.split('\t')[3]), -int(item.split('\t')[4])))
            content += ''.join(chr_list)
            content += ''.join(contig_list)
        return content

# Sequence extraction method============================================================================================
    def gff_extract_seq(self, fasta_file: str,
                        feature_type: click.Choice(['gene', 'mRNA', 'exon', 'five_prime_UTR', 'CDS', 'three_prime_UTR']) = 'gene',
                        feature_id_list: list = None) -> Nucleotide:
        """Extract sequences of specified feature type from GFF file."""
        gff_dict = self.get_gff_dict(feature_type)
        fa_file_obj = Fasta(fasta_file)
        for nucl_obj in fa_file_obj.FASTA_generator():
            try:
                features = gff_dict[nucl_obj.id]  # features = [{feature1}, {feature2}, ...]
            except KeyError:
                pass  # Some sequences (eg. scaffold, contig) may not have annotation
            else:
                for feature in features:  # feature = {id: str, start: int, end: int, strand: str}
                    if feature_id_list and feature['id'] in feature_id_list:
                        sub_seq_obj = nucl_obj[feature['start'] - 1:feature['end']]
                        sub_seq_obj.id = feature['id']
                        yield sub_seq_obj
                    elif not feature_id_list:
                        sub_seq_obj = nucl_obj[feature['start'] - 1:feature['end']]
                        sub_seq_obj.id = feature['id']
                        yield sub_seq_obj

    def miRNA_extraction(self) -> Nucleotide:
        """Extract miRNA sequence from GFF file."""
        for line in open(self.path):
            if not line.startswith('#'):
                split = line.strip().split('\t')
                attr = split[8].replace('=', ';').split(';')
                seq_id = attr[attr.index('ID') + 1]
                seq = attr[attr.index('seq') + 1]
                yield Nucleotide(seq_id, seq)

# File format conversion method=========================================================================================
    @staticmethod
    def filter_none_attr(is_gene: bool, gene_id: str, gene_name: str, transcript_id: str, transcript_name: str):
        d = {'gene_id': gene_id, 'gene_name': gene_name,
             'transcript_id': transcript_id, 'transcript_name': transcript_name}
        attr = ''
        for key, value in d.items():
            if value:
                if is_gene:
                    if key == list(d.keys())[1]:
                        attr += f'''{key} "{value}";'''
                    else:
                        attr += f'''{key} "{value}"; '''
                else:
                    if key == list(d.keys())[-1]:
                        attr += f'''{key} "{value}";'''
                    else:
                        attr += f'''{key} "{value}"; '''
        return attr + '\n'

    def GFF_to_GTF(self) -> str:
        """Convert the file format from GFF to GTF."""
        last_line = None
        gene_id = gene_name = transcript_id = transcript_name = None
        content = f"## gff_to_gtf\n## Convert from {self.path.split('/')[-1]}\n"
        line_num = sum(1 for _ in open(self.path) if not _.startswith('#') and _)
        i = 0
        for line in self.parse_GFF():
            i += 1
            current_line = list(line)
            if current_line[2] == 'gene':
                if last_line:
                    non_attr = '\t'.join(last_line[:8]) + '\t'
                    attr = self.filter_none_attr(False, gene_id, gene_name, transcript_id, transcript_name)
                    content += non_attr + attr
                    last_line = None
                    transcript_id = transcript_name = None
                gene_id, gene_name = current_line[8], current_line[9]
                non_attr = '\t'.join(current_line[:8]) + '\t'
                attr = self.filter_none_attr(True, gene_id, gene_name, transcript_id, transcript_name)
                content += non_attr + attr
            elif current_line[2] == 'mRNA':
                if last_line:
                    non_attr = '\t'.join(last_line[:8]) + '\t'
                    attr = self.filter_none_attr(False, gene_id, gene_name, transcript_id, transcript_name)
                    content += non_attr + attr
                    last_line = None
                transcript_id, transcript_name = current_line[8], current_line[9]
                current_line[2] = 'transcript'
                non_attr = '\t'.join(current_line[:8]) + '\t'
                attr = self.filter_none_attr(False, gene_id, gene_name, transcript_id,  transcript_name)
                content += non_attr + attr
            elif 'UTR' in current_line[2] or 'CDS' in current_line[2]:
                current_line[2] = 'exon'
                current_line[7] = '.'
                if last_line:
                    if int(last_line[4]) + 1 == int(current_line[3]):
                        last_line[4] = current_line[4]
                        if i == line_num:
                            non_attr = '\t'.join(last_line[:8]) + '\t'
                            attr = self.filter_none_attr(False, gene_id, gene_name, transcript_id, transcript_name)
                            content += non_attr + attr
                    else:
                        non_attr = '\t'.join(last_line[:8]) + '\t'
                        attr = self.filter_none_attr(False, gene_id, gene_name, transcript_id, transcript_name)
                        content += non_attr + attr
                        last_line = current_line
                        if i == line_num:
                            non_attr = '\t'.join(last_line[:8]) + '\t'
                            attr = self.filter_none_attr(False, gene_id, gene_name, transcript_id, transcript_name)
                            content += non_attr + attr
                else:
                    last_line = current_line
                    if i == line_num:
                        non_attr = '\t'.join(last_line[:8]) + '\t'
                        attr = self.filter_none_attr(False, gene_id, gene_name, transcript_id, transcript_name)
                        content += non_attr + attr
        return content

    def GFF_to_BED(self, feature_type: Union[str, list] = None) -> str:
        """Convert the file format from GFF to BED."""
        generator = self.parse_GFF()
        content = ''
        for line in generator:
            line = [str(i) for i in line if i]  # remove None attr
            if feature_type:
                if line[2] == feature_type or line[2] in feature_type:
                    content += f"{line[0]}\t{int(line[3])-1}\t{line[4]}\t{line[8]}\t{line[7]}\t{line[6]}\n"
            elif not feature_type:
                content += f"{line[0]}\t{int(line[3])-1}\t{line[4]}\t{line[8]}\t{line[7]}\t{line[6]}\n"
        return content

    def GFF_to_GSDS(self) -> str:
        """Convert the file format from GFF to GSDS."""
        content = ''
        transcript_id, transcript_start = None, 0
        for line in self.parse_GFF():
            line = list(line)
            if line[2] == 'mRNA':
                transcript_id = line[8]
                transcript_start = int(line[3])
            elif line[2] == 'CDS' or 'UTR' in line[2]:
                if line[10] == transcript_id:
                    line[3] = str(int(line[3]) - transcript_start)
                    line[4] = (int(line[4]) - transcript_start)
                    content += f"{transcript_id}\t{line[3]}\t{line[4]}\t{line[2]}\t{line[7]}\n"
                else:
                    click.echo(f'\033[33mWarning: The order of GFF file is wrong, '
                               f'this will cause some information to be lost.\033[0m', err=True)
        return content

# Feature density count=================================================================================================
    def get_feature_density(self, chr_len_dict: Dict[str, int], feature_type: str = 'gene', span: int = 100000):
        if min(list(chr_len_dict.values())) / span < 1:
            click.echo('\033[33mError: Density statistical interval is too large.\033[0m', err=True)
            exit()
        skip_rows = sum(1 for line in open(self.path) if line.startswith('#'))
        gff_dataframe = pd.read_table(self.path, skiprows=skip_rows, header=None)
        new_cols = ['Chr', 'Source', 'Feature', 'Start', 'End', 'Score', 'Strand', 'Frame', 'Attribute']
        d = {i: new_cols[i] for i in range(9)}
        gff_dataframe.rename(columns=d, inplace=True)
        gff_dataframe['Site'] = (gff_dataframe['Start'] + gff_dataframe['End']) / 2
        content = ''
        for chr_num, length in chr_len_dict.items():
            df = gff_dataframe[(gff_dataframe['Chr'] == chr_num) & (gff_dataframe['Feature'] == feature_type)]
            sites = df['Site']
            for i in range(span, length, span):
                count = len(sites[(sites <= i) & (sites >= i - span + 1)])
                content += f'{chr_num}\t{i - span + 1}\t{i}\t{count}\n'
            if length % span != 0:
                count = len(sites[(sites <= length) & (sites >= length // span * span + 1)])
                content += f'{chr_num}\t{length // span * span + 1}\t{length}\t{count}\n'
        return content
