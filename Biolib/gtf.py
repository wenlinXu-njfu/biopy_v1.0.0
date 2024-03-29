"""
File: gtf.py
Description: Instantiate a GTF file object
Date: 2021/12/1
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
from typing import Dict, List
import click
from Biolib.fasta import Fasta
from Biolib.sequence import Nucleotide


class Gtf:
    def __init__(self, path: str):
        self.path = path

# Basic method==========================================================================================================
    def parse(self):
        """Parse information of each column of GTF file line by line."""
        for line in open(self.path):
            if not line.startswith('#') and line.strip():
                split = line.strip().split('\t')
                chr_num, source, feature = split[0], split[1], split[2]
                start, end, score, strand, frame = split[3], split[4], split[5], split[6], split[7]
                attr_list = split[8].replace('"', '').split(';')
                attr_dict = {attr.strip().split(' ')[0]: attr.strip().split(' ')[1]
                             for attr in attr_list if attr}
                yield chr_num, source, feature, start, end, score, strand, frame, attr_dict

    def get_exon_dict(self) -> Dict[str, List[dict]]:
        """Save all exons' information in the GTF file into the dictionary."""
        # exon_dict = {
        #              Chr_num: [{transcript_id: str, start: int, end: int, strand: str}, {}, ...],
        #              Chr_num: [{exon}, {exon}, ...], ...
        #              }
        exon_dict = {}
        for line in self.parse():
            if line[2] == 'exon':
                item = {'id': line[8]['transcript_id'], 'start': int(line[3]), 'end': int(line[4]), 'strand': line[6]}
                if line[0] in exon_dict:
                    exon_dict[line[0]].append(item)
                else:
                    exon_dict[line[0]] = [item]
        return exon_dict

    def get_non_redundant_exon(self) -> Dict[str, List[dict]]:
        """Get non-redundant exon of each gene."""
        # non_redundant_exon_dict = {
        #                            Chr_num: [{gene_id: str, start: int, end: int, strand: str}, {}, ...],
        #                            Chr_num: [{exon}, {exon}, ...], ...
        #                            }
        non_redundant_exon_dict = {}
        gene_id = ''
        raw_exon_list = []
        line_num = sum(1 for _ in open(self.path) if not _.startswith('#'))
        line_count = 0
        for line in self.parse():
            line_count += 1
            if line[0] not in non_redundant_exon_dict:
                non_redundant_exon_dict[line[0]] = []
            if line[2] == 'exon':
                item = {'id': line[8]['gene_id'], 'start': int(line[3]), 'end': int(line[4]), 'strand': line[6]}
                if gene_id:
                    if gene_id == line[8]['gene_id']:
                        raw_exon_list.append(item)
                    else:
                        i = 0
                        while i + 1 < len(raw_exon_list):
                            raw_exon_list.sort(key=lambda d: (d['start'], d['end']))
                            if raw_exon_list[i]['end'] >= raw_exon_list[i + 1]['start']:
                                raw_exon_list[i + 1]['start'] = raw_exon_list[i]['start']
                                del raw_exon_list[i]
                                raw_exon_list.sort(key=lambda d: (d['start'], d['end']))
                                i = 0
                            elif raw_exon_list[i + 1]['end'] <= raw_exon_list[i]['end']:
                                del raw_exon_list[i + 1]
                                raw_exon_list.sort(key=lambda d: (d['start'], d['end']))
                                i = 0
                            else:
                                i += 1
                        non_redundant_exon_dict[line[0]].extend(raw_exon_list)
                        gene_id = line[8]['gene_id']
                        raw_exon_list = [item]
                else:
                    gene_id = line[8]['gene_id']
                    raw_exon_list.append(item)
                if line_count == line_num:
                    i = 0
                    while i + 1 < len(raw_exon_list):
                        raw_exon_list.sort(key=lambda d: (d['start'], d['end']))
                        if raw_exon_list[i]['end'] >= raw_exon_list[i + 1]['start']:
                            raw_exon_list[i + 1]['start'] = raw_exon_list[i]['start']
                            del raw_exon_list[i]
                            raw_exon_list.sort(key=lambda d: (d['start'], d['end']))
                            i = 0
                        elif raw_exon_list[i + 1]['end'] <= raw_exon_list[i]['end']:
                            del raw_exon_list[i + 1]
                            raw_exon_list.sort(key=lambda d: (d['start'], d['end']))
                            i = 0
                        else:
                            i += 1
                    non_redundant_exon_dict[line[0]].extend(raw_exon_list)
        return non_redundant_exon_dict

    def get_gene_dict(self):
        """Get gene dict. The start and end based on gene length, not based on chromosome length."""
        gene_dict = {}  # {gene_id: [{start: int, end: int, strand: str}, {}, ...], ...}
        non_redundant_exon_dict = self.get_non_redundant_exon()
        for chr_num, l in non_redundant_exon_dict.items():
            gene_id = gene_start = None
            raw_exon_list = []
            l.sort(key=lambda i: (
                i['id'], i['start'], i['end']))  # [{gene_id: str, start: int, end: int, strand: str}, ...]
            for exon_dict in l:  # {gene_id: str, start: int, end: int, strand: str}
                if gene_id:
                    if exon_dict['id'] == gene_id:
                        item = {'start': exon_dict['start'] - gene_start, 'end': exon_dict['end'] - gene_start,
                                'strand': exon_dict['strand']}
                        raw_exon_list.append(item)
                        if exon_dict == l[-1]:
                            if raw_exon_list[0]['strand'] == '-':
                                raw_exon_list.sort(key=lambda i: -i['end'])
                                gene_length = raw_exon_list[0]['end']
                                for d in raw_exon_list:
                                    start = gene_length - d['end']
                                    end = gene_length - d['start']
                                    d['start'] = start
                                    d['end'] = end
                            gene_dict[gene_id] = raw_exon_list
                    else:
                        if raw_exon_list[0]['strand'] == '-':
                            raw_exon_list.sort(key=lambda i: -i['end'])
                            gene_length = raw_exon_list[0]['end']
                            for d in raw_exon_list:
                                start = gene_length - d['end']
                                end = gene_length - d['start']
                                d['start'] = start
                                d['end'] = end
                        gene_dict[gene_id] = raw_exon_list
                        gene_id = exon_dict['id']
                        gene_start = exon_dict['start']
                        item = {'start': exon_dict['start'] - gene_start, 'end': exon_dict['end'] - gene_start,
                                'strand': exon_dict['strand']}
                        raw_exon_list = [item]
                        if exon_dict == l[-1]:
                            gene_dict[gene_id] = raw_exon_list
                else:
                    gene_id = exon_dict['id']
                    gene_start = exon_dict['start']
                    item = {'start': exon_dict['start'] - gene_start, 'end': exon_dict['end'] - gene_start,
                            'strand': exon_dict['strand']}
                    raw_exon_list.append(item)
                    if exon_dict == l[-1]:
                        if raw_exon_list[0]['strand'] == '-':
                            raw_exon_list.sort(key=lambda i: -i['end'])
                            gene_length = raw_exon_list[0]['end']
                            for d in raw_exon_list:
                                start = gene_length - d['end']
                                end = gene_length - d['start']
                                d['start'] = start
                                d['end'] = end
                        gene_dict[gene_id] = raw_exon_list
        return gene_dict

# Sequence extraction method============================================================================================
    def get_cDNA(self, fasta_file: str) -> Nucleotide:  # return Nucleotide objet generator
        """Extract cDNA sequence from GTF file according large reference sequence."""
        exon_dict = self.get_exon_dict()  # {chr_num: [{tid: str, start: int, end: int, strand: str}, {}, ...], ...}
        for nucl_obj in Fasta(fasta_file).FASTA_generator():
            cDNA_id = None
            cDNA_seq = ''
            cDNA_strand = None
            try:
                exon_list = exon_dict[nucl_obj.id]  # [{id: str, start: int, end: int, strand: str}, {}, ...]
                exon_list.sort(key=lambda item: (item['id'], item['start'], item['end']))
            except KeyError:
                pass  # Some sequences (eg. scaffold, contig) may not have annotation
            else:
                for exon in exon_list:  # {id: str, start: int, end: int, strand: str}
                    exon_seq = nucl_obj.seq[exon['start'] - 1:exon['end']]
                    if cDNA_id and cDNA_id == exon['id']:
                        cDNA_seq += exon_seq
                        if exon == exon_list[-1]:
                            cDNA_nucl_obj = Nucleotide(cDNA_id, cDNA_seq)
                            if cDNA_strand == '-':
                                cDNA_nucl_obj = -cDNA_nucl_obj
                            cDNA_nucl_obj.id = cDNA_id
                            yield cDNA_nucl_obj
                    elif cDNA_id and cDNA_id != exon['id']:
                        cDNA_nucl_obj = Nucleotide(cDNA_id, cDNA_seq)
                        if cDNA_strand == '-':
                            cDNA_nucl_obj = -cDNA_nucl_obj
                        cDNA_nucl_obj.id = cDNA_id
                        yield cDNA_nucl_obj
                        cDNA_seq = exon_seq
                        cDNA_id = exon['id']
                        cDNA_strand = exon['strand']
                        if exon == exon_list[-1]:
                            cDNA_nucl_obj = Nucleotide(cDNA_id, cDNA_seq)
                            if cDNA_strand == '-':
                                cDNA_nucl_obj = -cDNA_nucl_obj
                            cDNA_nucl_obj.id = cDNA_id
                            yield cDNA_nucl_obj
                    elif not cDNA_id:
                        cDNA_seq = exon_seq
                        cDNA_id = exon['id']
                        cDNA_strand = exon['strand']
                        if exon == exon_list[-1]:
                            cDNA_nucl_obj = Nucleotide(cDNA_id, cDNA_seq)
                            if cDNA_strand == '-':
                                cDNA_nucl_obj = -cDNA_nucl_obj
                            cDNA_nucl_obj.id = cDNA_id
                            yield cDNA_nucl_obj

# File format conversion method=========================================================================================
    def GTF_to_BED(self, feature_type: str = 'exon') -> str:
        """Convert the file format from GTF to BED."""
        content = ''
        for line in self.parse():
            if line[2] == feature_type != 'gene':
                content += f"{line[0]}\t{int(line[3]) - 1}\t{line[4]}\t{line[8]['transcript_id']}\t{line[7]}\t{line[6]}\n"
            elif line[2] == feature_type == 'gene':
                content += f"{line[0]}\t{int(line[3]) - 1}\t{line[4]}\t{line[8]['gene_id']}\t{line[7]}\t{line[6]}\n"
        return content

    def GTF_to_GSDS(self, feature_type: click.Choice(['gene', 'transcript']) = 'transcript') -> str:
        """Convert the file format from GTF to GSDS."""
        content = ''
        if feature_type == 'gene':
            exon_dict = self.get_non_redundant_exon()
        else:
            exon_dict = self.get_exon_dict()
        parent_id = parent_start = None
        for _, l in exon_dict.items():
            l.sort(key=lambda d: (d['id'], d['start'], d['end']))
            for exon in l:
                if not parent_id:
                    parent_id = exon['id']
                    parent_start = exon['start']
                    content += f"{exon['id']}\t{exon['start'] - parent_start}\t{exon['end'] - parent_start}\texon\t.\n"
                else:
                    if parent_id == exon['id']:
                        content += f"{exon['id']}\t{exon['start'] - parent_start}\t{exon['end'] - parent_start}\texon\t.\n"
                    else:
                        parent_id = exon['id']
                        parent_start = exon['start']
                        content += f"{exon['id']}\t{exon['start'] - parent_start}\t{exon['end'] - parent_start}\texon\t.\n"
        return content
