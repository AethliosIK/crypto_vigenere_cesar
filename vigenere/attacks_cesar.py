#!/usr/bin/env python3
# coding: utf-8

import sys, getopt, argparse

from source.attacks_cesar import frequency_attack_cesar, bruteforce_attack_cesar
from source.dico import *
from source.util import extract_in_file, write_in_file

DEFAULT_PERCENT = 60.0
DEFAULT_LEVEL_VERBOSE = 0
LEVEL_ONE_VERBOSE = 1
LEVEL_TWO_VERBOSE = 2


if __name__ == "__main__":
    str_a = "abcdefghijklmnopqrstuvwxyz"
    percent = DEFAULT_PERCENT
    str_dico = "Dictionnaires/French_ascii.txt"
    book = "Books/Fr-Jules_Verne-20000_Lieues_sous_les_mers.txt"
    outfilename = "output.txt"
    level_verbose = DEFAULT_LEVEL_VERBOSE

    parser = argparse.ArgumentParser(prog="attacks_cesar")
    parser.add_argument('-f', '--frequency', help="For attack frequency.",
                    action="store_true")
    parser.add_argument("-a", "--authorize", help="Characters authorized for encrypt. Default = " +
                        str_a.replace("\n", "\\n").replace("\t", "\\t"))
    parser.add_argument('-p', '--percent', help="matching percent. Default = {}".format(percent))
    parser.add_argument('-l', '--language', help="file path dico for message language. Default file = " + str_dico)
    parser.add_argument('-b', '--book', help="book for message language. Default = " + book)
    parser.add_argument('-v', '--verbose', help="verbose level 1", action="store_true")
    parser.add_argument('-w', '--verbose2', help="verbose level 2", action="store_true")
    parser.add_argument('filename', help="Filename input to attack")
    parser.add_argument('-o', '--output', help="Filename ouput")
    args = parser.parse_args()

    s = extract_in_file(args.filename)

    if (args.authorize != None):
        str_a = args.authorize
    if (args.percent != None):
        percent = float(args.percent)
    if (args.language != None):
        str_dico = args.language
    if (args.book != None):
        book = args.book
    if (args.verbose):
        level_verbose = LEVEL_ONE_VERBOSE
    if (args.verbose2):
        level_verbose = LEVEL_TWO_VERBOSE
    if (args.output != None):
        outfilename = args.output

    d = dico(str_dico, book)

    if (args.frequency):
        (result, key) = frequency_attack_cesar(s, d, str_a, percent, level_verbose)
    else:
        (result, key) = bruteforce_attack_cesar(s, d, str_a, percent, level_verbose)

    write_in_file(outfilename, result)

