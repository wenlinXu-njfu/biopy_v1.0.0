"""
File: sequence.py
Description: Instantiate a sequence object (including nucleotide and amino acid sequences)
Date: 2021/11/26
Author: xuwenlin
E-mail: wenlinxu.njfu@outlook.com
"""
import re
from typing import Tuple


class Sequence:
    def __init__(self, seq_id: str, sequence: str, strip: bool = True):
        self.id = seq_id.strip().replace('>', '')
        if strip:
            self.seq = sequence.replace('\n', '')
        else:
            self.seq = sequence
        if '*' in sequence:
            self.len = len(sequence.replace('\n', '').replace('*', ''))
        else:
            self.len = len(sequence.replace('\n', ''))

    def __str__(self) -> str:
        return f'>{self.id} length={len(self)}\n{self.seq}'

    def __contains__(self, item) -> bool:
        """
        Define when implement "Sequence_obj1 in Sequence_obj2", if Sequence_obj1.seq in Sequence_obj2.seq, return True,
        otherwise return False.
        """
        return True if item.seq.replace('\n', '') in self.seq.replace('\n', '') else False

    def __ne__(self, other) -> bool:
        """
        Define when implement "Sequence_obj1 != Sequence_obj2", if Sequence_obj1.seq != Sequence_obj2.seq, return True,
        otherwise return False.
        """
        return True if self.seq.replace('\n', '') != other.seq.replace('\n', '') else False

    def __eq__(self, other) -> bool:
        """
        Define when implement "Sequence_obj1 == Sequence_obj2", if Sequence_obj1.seq == Sequence_obj2.seq, return True,
        otherwise return False.
        """
        return True if self.seq.replace('\n', '') == other.seq.replace('\n', '') else False

    def __hash__(self):
        return hash(self.seq)

    def __lt__(self, other) -> bool:
        """
        Define when implement "Sequence_obj1 < Sequence_obj2", if len(Sequence_obj1.seq) < len(Sequence_obj2.seq),
        return True, otherwise return False.
        """
        return True if len(self) < len(other) else False

    def __le__(self, other) -> bool:
        """
        Define when implement "Sequence_obj <= Sequence_obj2", if len(Sequence_obj1.seq) <= len(Sequence_obj2.seq),
        return True, otherwise return False.
        """
        return True if len(self) <= len(other) else False

    def __gt__(self, other) -> bool:
        """
        Define when implement "Sequence_obj > Sequence_obj2", if len(Sequence_obj1.seq) > len(Sequence_obj2.seq),
        return True, otherwise return False.
        """
        return True if len(self) > len(other) else False

    def __ge__(self, other) -> bool:
        """
        Define when implement "Sequence_obj >= Sequence_obj2", if len(Sequence_obj1.seq) >= len(Sequence_obj2.seq),
        return True, otherwise return False.
        """
        return True if len(self) >= len(other) else False

    def __iter__(self) -> str:
        """ Implement "iter(self.seq)". """
        yield from self.seq

    def __getitem__(self, item):
        """
        Define when implement "Sequence_obj[int:int:int].seq", it is equal to "Sequence_obj.seq[int:int:int]",
        but the return value type is same as raw object.
        """
        if item.start is None or item.start == 0:
            start = 1
        else:
            start = item.start
        if item.stop is None or item.stop > self.len:
            stop = self.len
        else:
            stop = item.stop
        if item.step is None:
            step = 1
        else:
            step = item.step
        if isinstance(self, Nucleotide):
            return Nucleotide(f"{self.id} slice({start}:{stop}:{step})", self.seq.replace('\n', '')[item])
        elif isinstance(self, Protein):
            return Protein(f"{self.id} slice({start}:{stop}:{step})", self.seq.replace('\n', '')[item])

    def __len__(self) -> int:
        return len(self.seq.replace('*', '').replace('\n', ''))

    def get_seq_len_info(self) -> str:
        """Get sequence length information."""
        return f'{self.id}\t{self.len}'

    def find_motif(self, motif: str) -> str:
        """Find the motif in the sequence."""
        ret = []
        matched = re.findall(rf'{motif}', self.seq)
        matched = list(set(matched))
        if matched:
            for motif in matched:
                split = self.seq.split(motif)
                end = 0
                for i in split:
                    if i != split[-1]:
                        start = end + len(i) + 1
                        end = start + len(motif) - 1
                        ret.append(f"{self.id}\t{start}\t{end}\t{motif}\n")
                    ret.sort(key=lambda item: (int(item.split('\t')[1]), int(item.split('\t')[2])))
            return ''.join(ret)
        else:
            return f'{self.id} not found motif.'


class Nucleotide(Sequence):
    codon_table = {'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
                   'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
                   'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
                   'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
                   'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
                   'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
                   'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
                   'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
                   'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
                   'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
                   'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
                   'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
                   'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
                   'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
                   'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
                   'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G'}

    def __add__(self, other):
        """
        Define when implement "Nucleotide_obj1 + Nucleotide_obj2",
        it is equal to "Nucleotide_obj1.seq + Nucleotide_obj2.seq",
        but no value is returned, just the seq and len attributes of Nucleotide_obj1 are changed.
        """
        self.seq = self.seq + other.seq
        self.len = len(self)

    def __neg__(self):
        """
        Define when implement "-Nucleotide_obj", it is equal to "Nucleotide_obj.get_reverse_complementary_seq()".
        """
        return self.get_reverse_complementary_seq()

    def get_reverse_complementary_seq(self):
        """Get reverse complementary sequence of DNA or RNA."""
        dna_complementary_dict = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G', 'N': 'N',
                                  'a': 't', 't': 'a', 'g': 'c', 'c': 'g', 'n': 'n'}
        rna_complementary_dict = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G', 'N': 'N',
                                  'a': 'u', 'u': 'a', 'g': 'c', 'c': 'g', 'n': 'n'}
        seq = ''
        if 'T' in self.seq or 't' in self.seq:
            for n in self.seq.replace('\n', ''):
                seq += dna_complementary_dict[n]
        else:
            for n in self.seq.replace('\n', ''):
                seq += rna_complementary_dict[n]
        return Nucleotide(f"{self.id} reverse_complementary_chain", seq[::-1])

    def display_set(self, n: int = 60):
        """Set how many nucleotides are displayed per line."""
        if self.seq.count('\n') >= 1:
            return self
        seq: str = ''
        i = 0
        while i < len(self):
            seq += f'{self.seq[i:i + n]}\n'
            i += n
        return Nucleotide(self.id, seq, False)

    def base_count(self) -> Tuple[str, str, str, str, str]:
        """Get the percentage content of four bases."""
        A = '%.2f' % (self.seq.upper().count('A') / len(self) * 100)
        G = '%.2f' % (self.seq.upper().count('G') / len(self) * 100)
        C = '%.2f' % (self.seq.upper().count('C') / len(self) * 100)
        T = '%.2f' % (self.seq.upper().count('T') / len(self) * 100)
        U = '%.2f' % (self.seq.upper().count('U') / len(self) * 100)
        if 'U' in self.seq or 'u' in self.seq:
            summary = f"Base content statistics of {self.id}\nA: {A}%\nG: {G}%\nC: {C}%\nU: {U}%"
            return A, G, C, U, summary
        else:
            summary = f"Base content statistics of {self.id}\nA: {A}%\nG: {G}%\nC: {C}%\nT: {T}%"
            return A, G, C, T, summary

    def translation(self, complete: bool = True):
        peptide_chain = ''
        for i in range(0, len(self), 3):
            codon = self.seq.upper().replace('T', 'U').replace('\n', '')[i:i + 3]
            try:
                peptide_chain += self.codon_table[codon]
            except KeyError:
                peptide_chain += '-'
        if complete:
            try:
                peptide_chain = max(re.findall(r'M[A-Z]+\*', peptide_chain), key=len)
                return Protein(f"{self.id} peptide_chain", peptide_chain)
            except ValueError:
                return Protein(f"{self.id} peptide_chain", '')
        else:
            peptide_chain = max(re.findall(r'M?[A-Z]+\*?', peptide_chain), key=len)
            return Protein(f"{self.id} peptide_chain", peptide_chain)

    def ORF_prediction(self, min_len: int = 1, complete: bool = True, only_plus: bool = False):
        """
        ORF prediction.
        :param min_len: minimal ORF length (type=int) {default=1}
        :param complete: whether consider ORF integrity (type=bool) {default=True}
        :param only_plus: whether only consider plus chain (type=bool) {default=False}
        :return: longest ORF (type=Protein)
        """
        plus1 = self.translation(complete)
        plus2 = self[1:].translation(complete)
        plus3 = self[2:].translation(complete)
        prot_obj_list = [plus1, plus2, plus3]
        if not only_plus:
            minus1 = (-self).translation(complete)
            minus2 = (-self)[1:].translation(complete)
            minus3 = (-self)[2:].translation(complete)
            prot_obj_list.extend([minus1, minus2, minus3])
        try:
            longest_ORF = max(prot_obj_list, key=len)
            if len(longest_ORF) >= min_len:
                longest_ORF.id = f'{self.id} ORF_prediction'
                return longest_ORF
            else:
                return f"{self.id} not found ORF."
        except ValueError:
            return f"{self.id} not found ORF."

    def circular_translation(self) -> tuple:
        """Translate a nucleotide sequence circularly."""
        for i in range(len(self)):
            cds = pep = ''
            j = i
            while True:
                if j + 3 <= len(self):
                    codon = self.seq[j:j + 3].upper()
                    if cds:
                        cds += codon
                        pep += self.codon_table[codon.replace('T', 'U')]
                        if self.codon_table[codon.replace('T', 'U')] == '*':
                            j += 3
                            break
                    else:
                        if codon == 'ATG':
                            cds += codon
                            pep += self.codon_table[codon.replace('T', 'U')]
                        else:
                            break
                else:
                    if j < len(self):
                        n = len(self) - j
                        codon = self.seq[-n:].upper() + self.seq[:3 - n].upper()
                        if cds:
                            cds += codon
                            pep += self.codon_table[codon.replace('T', 'U')]
                        else:
                            if codon == 'ATG':
                                cds += codon
                                pep += self.codon_table[codon.replace('T', 'U')]
                            else:
                                break
                        if self.codon_table[codon.replace('T', 'U')] == '*':
                            j += 3
                            break
                    else:
                        if (j - i) == len(self):
                            break
                        else:
                            if len(self) - j % len(self) < 3:
                                n = len(self) - j % len(self)
                                codon = self.seq[-n:].upper() + self.seq[:3 - n].upper()
                            else:
                                codon = self.seq[j % len(self):j % len(self) + 3].upper()
                            cds += codon
                            pep += self.codon_table[codon.replace('T', 'U')]
                            if self.codon_table[codon.replace('T', 'U')] == '*':
                                j += 3
                                break
                j += 3
            if cds and pep.endswith('*'):
                if j > len(self):
                    cds = Nucleotide(
                        f'{self.id} circular_translation_cds start={i + 1} end={j % len(self)} circular={j // len(self)}',
                        cds)
                    pep = Protein(
                        f'{self.id} circular_translation_pep start={i + 1} end={j % len(self)} circular={j // len(self)}',
                        pep)
                else:
                    cds = Nucleotide(f'{self.id} circular_translation_cds start={i + 1} end={j} circular=0', cds)
                    pep = Protein(
                        f'{self.id} circular_translation_pep start={i + 1} end={j} circular=0', pep)
                yield cds, pep


class Protein(Sequence):
    def display_set(self, n: int = 60):
        """Set how many amino acid are displayed per line."""
        if self.seq.count('\n') >= 1:
            return self
        seq: str = ''
        i = 0
        while i < len(self):
            seq += f'{self.seq[i:i + n]}\n'
            i += n
        return Protein(self.id, seq, False)
