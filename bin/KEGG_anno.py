#!/usr/bin/env python
"""
File: KEGG_anno.py
Description: Preprocess xxx00001.keg file
Date: 2022/6/22
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import re
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(keg_file, out_file):
    content = ko = pathway = species = ''
    for line in open(keg_file):
        line = line.strip()
        if not line.startswith('A09160'):
            if line.startswith('C'):
                ko = re.findall(r'[a-z]{3}\d{5}', line)
                if ko:
                    ko = ko[0]
                    species = re.findall(r'[a-z]{3}', ko)[0]
                    ko_num = re.findall(r'\d{5}', ko)[0]
                    ko = f"ko{ko_num}"
                    pathway = ' '.join(line.split('    ')[1].split(' ')[1:])
                else:
                    ko = f"ko{line.split('    ')[1].split(' ')[0]}"
                    pathway = ' '.join(line.split('    ')[1].split(' ')[1:])
                if '[' in pathway:
                    _id = re.findall(r' \[.+]', pathway)[0]
                    pathway = pathway.replace(_id, '')
            elif line.startswith('D'):
                gene_id = f"{species}{line.split('      ')[1].split(' ')[0]}"
                K = line.split('      ')[1].split('\t')[1].split(' ')[0]
                EC = re.findall(r' \[EC:.+]', line)
                if EC:
                    EC = EC[0]
                    KO = line.split('      ')[1].split('\t')[1].split('; ')[1].replace(EC, '')
                else:
                    KO = line.split('      ')[1].split('\t')[1].split('; ')[1]
                if out_file:
                    content += f'{gene_id}\t{K}\t{KO}\t{ko}\t{pathway}\n'
                else:
                    print(f'{gene_id}\t{K}\t{KO}\t{ko}\t{pathway}')
        else:
            break
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'in_file', help='Input keg file. (format=htext)')
@click.option('-out',
              help='[optional] Output file (eg. pop7465650\tK18835\tWRKY transcription factor 2\tko04626\tPlant-pathogen interaction), '
                   'if not specified, print results to terminal as stdout.')
def run(in_file, out):
    """Preprocess xxx00001.keg file"""
    main(in_file, out)


if __name__ == '__main__':
    run()
