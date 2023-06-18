#!/usr/bin/env python
"""
File: id_index_seq.py
Description: Extract sequences from FASTA file based on the id provided
Date: 2022/3/25
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import click
from Biolib.fasta import Fasta
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


def main(fa_file, parse_seqids: click.Choice(['yes', 'no']), id_file, match: bool, log, out_file):
    parse_seqids = {'yes': True, 'no': False}[parse_seqids]
    content = ''
    id_list = list(set([i.strip() for i in open(id_file).readlines() if i.strip()]))  # remove repeat IDs
    id_list_index = list(range(len(id_list)))  # Create a subscript for each ID
    for nucl_obj in Fasta(fa_file).FASTA_generator(parse_seqids):
        if match and nucl_obj.id in id_list:
            del id_list[id_list.index(nucl_obj.id)]
            if out_file:
                content += f">{nucl_obj.id}\n{nucl_obj.seq}\n"
            else:
                print(nucl_obj)
        elif not match:
            for _id in id_list:
                if nucl_obj.id in _id or _id in nucl_obj.id:
                    index = id_list.index(_id)
                    id_list_index[index] = True  # Mark sequence that has been found
                    if out_file:
                        content += f">{nucl_obj.id}\n{nucl_obj.seq}\n"
                    else:
                        print(nucl_obj)
    if content:
        with open(out_file, 'w') as o:
            o.write(content)
    # report sequence that not match
    if match and id_list:
        msg = ' not found\n'.join(id_list) + ' not found\n'
        click.echo(f'\033[33m{msg}\033[0m', err=True, file=open(log, 'a')) if log else \
            click.echo(f'\033[33m{msg}\033[0m', err=True)
    # report sequence that not contain
    if not match:
        not_found = [i for i in id_list_index if i is not True]
        not_found = [id_list[i] for i in not_found]
        if not_found:
            msg = ' not found\n'.join(not_found) + ' not found\n'
            click.echo(f'\033[33m{msg}\033[0m', err=True, file=open(log, 'a')) if log else \
                click.echo(f'\033[33m{msg}\033[0m', err=True)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-fa', help='Input FASTA file.')
@click.option('-parse_seqids', default='no', type=click.Choice(['yes', 'no']), help='Parse FASTA file sequence id. {default=no}')
@click.option('-id', 'id_file', help='Input id TEXT file. (one id per line)')
@click.option('-match/-contain', help='Whether the id supplied should exactly match the ID of the sequence '
                                      '(default: match)', default=True)
@click.option('-log', help='[optional] Log file, if not specified, the log will print to terminal')
@click.option('-out', help='[optional] Output file, if not specified, print results to terminal as stdout.')
def run(fa, parse_seqids, id_file, match, log, out):
    """Extract sequences from FASTA file based on the id provided."""
    main(fa, parse_seqids, id_file, match, log, out)


if __name__ == '__main__':
    run()
