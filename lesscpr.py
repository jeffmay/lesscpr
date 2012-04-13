#!/usr/bin/env python

import argparse
import os
import sys

from os.path import *

def main(args):
    parser = argparse.ArgumentParser("lesscpr", description="Recursively compile LESS files.")
    parser.add_argument('source', type=abspath, nargs='?', default=join(os.getcwd(), 'less'),
            help="path to less source files (default: ./less)")
    parser.add_argument('destination', type=abspath, nargs='?', default=None,
            help="destination path for css files (default: ./css)")
    parser.add_argument('-x', '--compress', action='store_true', default=False,
            help="minify output css")
    parser.add_argument('--noop', action='store_true', default=False,
            help="do not actually compile")
    opts = parser.parse_args()
    if opts.destination is None:
        opts.destination = join(dirname(opts.source), 'css')
    print(opts)
    compiled = compile_all(src=opts.source, dst=opts.destination,
            compress=opts.compress, noop=opts.noop)
    print("%s files compiled" % compiled)

def compile_all(src, dst, compress=True, noop=False):
    try:
        os.makedirs(dst)
    except:
        pass
    compiled=0
    for dirpath, dirnames, filenames in os.walk(src):
        print("compiling %s" % dirpath)
        srcfiles = [filename for filename in filenames if filename.endswith('.less')]
        for srcfile in srcfiles:
            srcpath = relpath(join(dirpath, srcfile))
            # replace the file extension
            dstfile = srcfile[:-len('less')] + 'css'
            # get the relative path to the less file from the src dir
            # join the destination dir with that relative path
            # get the relative path to the dst file from that path 
            dstpath = normpath(join(join(dst, relpath(dirpath, src)), dstfile))
            cmd = 'lessc{compress} {source} > {destination}'.format(
                    source=srcpath,
                    destination=dstpath,
                    compress=' -x' if compress else '')
            if noop is False:
                print(cmd)
                os.system(cmd)
            else:
                print('[NOOP] ' + cmd)
            compiled += 1
    return compiled

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

