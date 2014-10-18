obj2mesh
========

usage: obj2mesh [-h] [--no-normalization] infile [outfile]

Convert a .obj file to csv-compatible mesh format.

positional arguments:
  infile              path to .obj
  outfile             path to mesh

optional arguments:
  -h, --help          show this help message and exit
  --no-normalization  Disable rescaling the vertex coordinates
                      to fit in the [0, 1] range. (enabled by default)
