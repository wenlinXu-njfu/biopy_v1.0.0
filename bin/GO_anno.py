#!/usr/bin/env python
"""
File: GO_anno.py
Description: Preprocess go-basic.obo file
Date: 2022/1/14
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(go_basic_obo_file, out_file):
    content = ''
    d = {}
    is_term = None
    for line in open(go_basic_obo_file):
        if line.startswith('data-version'):
            content += f'##{line}##ID\tChild_id\tName\tNamespace\tDefinition\n'
        elif line.startswith('[Term]'):
            is_term = True
        elif line.startswith('id: '):
            if is_term:
                d[1] = f"{line.strip().replace('id: ', '')}"
        elif line.startswith('name: '):
            if is_term:
                d[3] = f"{line.strip().replace('name: ', '')}"
        elif line.startswith('namespace: '):
            if is_term:
                d[4] = f"{line.strip().replace('namespace: ', '')}"
        elif line.startswith('alt_id: '):
            if is_term:
                if 2 in d:
                    d[2] = d[2] + f",{line.strip().replace('alt_id: ', '')}"
                else:
                    d[2] = f"{line.strip().replace('alt_id: ', '')}"
        elif line.startswith('def: '):
            if is_term:
                d[5] = f"{line.strip().replace('def: ', '')}"
        elif not line.strip():
            if d:
                try:
                    content += f'{d[1]}\t{d[2]}\t{d[3]}\t{d[4]}\t{d[5]}\n'
                except KeyError:
                    content += f'{d[1]}\tNull\t{d[3]}\t{d[4]}\t{d[5]}\n'
            is_term = False
            d = {}
    if out_file:
        with open(out_file, 'w') as o:
            o.write(content)
    else:
        print(content)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-in', 'go', help='Input GO annotation file (go-basic.obo).')
@click.option('-out', help='[optional] Output file (##Id\\tChild_id\\tName\\tNamespace\\tDefinition), '
                           'if not specified, print results to terminal as stdout.')
def run(go, out):
    """Preprocess go-basic.obo file."""
    main(go, out)


if __name__ == '__main__':
    run()
