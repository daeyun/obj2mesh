import argparse
import sys
import re
import os
from decimal import *


def obj2mesh(filename, isVerbose=True):
    '''
    Return the faces and vertices parsed from an .obj file as n-by-3 lists.
    '''

    with open(filename) as f:
        content = f.readlines()

    if isVerbose:
        print filename

    mesh = {'f': [], 'v': []}

    # set floating point precision
    getcontext().prec = 28

    for line in content:
        pattern = [(mesh['v'], '^v ([^ ]+) ([^ ]+) ([^ ]+)'),
                   (mesh['f'], '^f ([0-9]+)[^ ]* ([0-9]+)[^ ]* ([0-9]+)[^ ]*')]

        for target, pat in pattern:
            match = re.search(pat, line)

            if not match:
                continue

            group = [match.group(1), match.group(2), match.group(3)]
            xyz = [int(g) if g.isdigit() else Decimal(g) for g in group]
            target.append(xyz)
            break

    # initialize with the first value in the list
    min_vals = mesh['v'][0][:]
    max_vals = mesh['v'][0][:]

    # find min and max in each x, y, z component
    for vertex in mesh['v']:
        for i in range(0, 3):
            if vertex[i] < min_vals[i]:
                min_vals[i] = vertex[i]
            elif vertex[i] > max_vals[i]:
                max_vals[i] = vertex[i]

    # rescale to [0, 1] range
    rescale_ratio = Decimal('1')/max([b-a for a, b in zip(min_vals, max_vals)])
    mesh['v'] = [[rescale_ratio*(vertex[i]-min_vals[i]) for i in range(0, 3)]
                 for vertex in mesh['v']]

    return mesh


def main():
    parser = argparse.ArgumentParser(description='Convert .obj to mesh')
    parser.add_argument('infile', nargs=1, help='path to .obj')
    parser.add_argument('outfile', nargs='?', help='path to mesh',
                        default=None)
    parser.add_argument('--no-normalization', default=True,
                        action='store_false', dest='will_normalize',
                        help='Disable rescaling the vertex coordinates to '
                             'fit in the [0, 1] range. (enabled by default)')
    if len(sys.argv) == 1:
        parser.print_help()
        os._exit(1)

    args = parser.parse_args()
    inpath = args.infile[0]

    filename = os.path.basename(os.path.normpath(inpath))
    if args.outfile is None:
        outpath = os.path.basename(os.path.normpath(inpath))
    else:
        outpath = args.outfile
        if os.path.isdir(outpath):
            outpath = os.path.join(outpath, filename)

    mesh = obj2mesh(inpath)

    for name, rows in mesh.iteritems():
        outfile = '{}.{}'.format(outpath, name)
        print outfile
        with open(outfile, 'a') as f:
            lines = [','.join([str(num) for num in row]) for row in rows]
            f.write('\n'.join(lines))
