import sys, os
from . import fasta


def chunkseq(seq, length):
    return (seq[0+i:length+i] for i in range(0, len(seq), length))


def sanitize_id(identifier, replacement_char):
    id_chars = [replacement_char
                if identifier[0] in ('*', '=') else
                identifier[0]]
    for c in identifier[1:]:
        id_chars.append(c if 32 < ord(c) < 127 else
                        replacement_char)
    return ''.join(id_chars)


def sanitize_fasta(ifile, ofile,
                   replacement_char = '_', seq_block_length = 80):    
    with open(ifile, 'r') as ifo, open(ofile, 'w') as ofo:
        for identifier, seq in fasta.FastaReader(ifo).sequences():
            # write sanitized identifier line
            ofo.write('>')
            ofo.write(sanitize_id(identifier, replacement_char))
            ofo.write('\n')
            # write sanitized sequence block
            for subseq in chunkseq(seq, seq_block_length):
                ofo.write(subseq)
                ofo.write('\n')


if __name__ == '__main__':
    inputfile = os.path.expanduser(sys.argv[1])
    outputfile = os.path.expanduser(sys.argv[2])
    replacement_char = '_'
    seq_block_length = 80
    print()
    print('sanitizing', inputfile, '...')
    sanitize_fasta(inputfile, outputfile, '_', 80)


