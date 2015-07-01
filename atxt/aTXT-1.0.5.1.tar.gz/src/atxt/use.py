#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""aTXT for text extraction data mining tool

Usage:
    aTXT [-h]
    aTXT [--check] [--log PATH]
    aTXT [-ihvo] [--log PATH] [--use-temp] [-l LANG]
    aTXT <source>... [-hvo] [-d DEPTH] [--log PATH] [--from PATH] [--to PATH] [--format EXT] [--use-temp] [-l LANG]
    aTXT --file <file>... [-hvo] [--log PATH] [--from PATH] [--to PATH] [--format EXT] [--use-temp] [-l LANG]
    aTXT --path <path>... [-d DEPTH] [-hvuo] [--log PATH] [--to PATH] [--format EXT] [--use-temp] [-l LANG]

Arguments:
    <source>...         It can be files, foldres or mix of them.
    <file>...           Just files paths
    <path>...           Just paths to directories

Options:
    -i                  Launch the graphical interface 
    -h                  Show help
    -o                  Overwrite result files. [default: False].
    --format EXT        string \"...\" separte with ',' of formats or extension to
                        consider when it will process the files
    --log PATH          Specify a path to save the log [default: ./].
    -v                  Show the version. [default:False].
    -d, --depth DEPTH   Integer for depth for trasvering path using 
                        Depth-first-search on folders @int for path of files in <source>
                        [default: 0]
    --from PATH         root path of the files [default: ./].
    --to PATH           root path of save the result files [default: ./].
    --check             check the system for requirements: Xpdf, Tesseract
    --ocr               Use OCR for extract text from hard pdf, if you have a language package
                        installed, you could use option -l LANGSPEC [default: False].
    --use-temp          use the generation of temporary files for 
                        avoid problems with filepaths. [default: False].
    -l LANG             option of a language for tesseract OCR, please be sure that 
                        thes package is installed. [default: spa].

Examples:

    $ atxt -i
    $ atxt prueba.html
    $ atxt --file ~/Documents/prueba.html
    $ atxt ~ -d 2
    $ atxt --path ~ -d 2 --format 'txt,html'
"""