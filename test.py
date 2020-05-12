#!/usr/bin/python3

import os, sys, re, argparse, fileinput
import json

data = ''
data = json.load(data)
data = json.update('[arributes]')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--dummy', help='dummy argument')
    parser.add_argument('files', metavar='FILE', nargs='*', help='files to read, if empty, stdin is used')
    args = parser.parse_args()

    for line in fileinput.input(files=args.files if len(args.files) > 0 else ('-', )):
        if( "standard::display-name:" in line ):
            prog = re.split("standard::display-name:",line)
            print( prog[1].strip() )
            data.append({'standard::display-name:', prog[1].strip() })
        if( "metadata::icon-scale:" in line ):
            prog = re.split("metadata::icon-scale:",line)
            print( prog[1].strip() )            
        if( "metadata::nautilus-icon-position:" in line ):
            prog = re.split("metadata::nautilus-icon-position:",line)
            print( prog[1].strip() )            
