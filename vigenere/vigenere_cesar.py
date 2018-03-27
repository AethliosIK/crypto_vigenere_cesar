#!/usr/bin/env python3
# coding: utf-8

import sys, getopt, argparse

from source.encrypt_decrypt import encrypt_cesar, decrypt_cesar, encrypt_vigenere, decrypt_vigenere
from source.define_space import define_space
from source.dico import *
from source.util import extract_in_file, write_in_file

LEVEL_ZERO_VERBOSE = 0
LEVEL_ONE_VERBOSE = 1
LEVEL_TWO_VERBOSE = 2
DEFAULT_LEVEL_VERBOSE = LEVEL_ZERO_VERBOSE

if __name__ == "__main__":
    str_a = "abcdefghijklmnopqrstuvwxyz"
    str_r = " \n\t"
    str_c = "éèêë|àâä|ç|ùüû|ïî|ôö"
    str_t = "eacuio"
    str_dico = "Dictionnaires/French_ascii.txt"
    outfilename = "output.txt"
    level_verbose = DEFAULT_LEVEL_VERBOSE

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cesar", help="For encrypt/decrypt with cesar",
                    action="store_true")
    parser.add_argument("-d", "--decrypt", help="For decrypt",
                    action="store_true")
    parser.add_argument("-a", "--authorize", help="Characters authorized for encrypt. Default = " +
                        str_a.replace("\n", "\\n").replace("\t", "\\t"))
    parser.add_argument("-r", "--remove", help="Characters removed for encrypt. Default = " +
                        str_r.replace("\n", "\\n").replace("\t", "\\t"))
    parser.add_argument('-l', '--language', help="filename dico for message language. Default file = " + str_dico)
    parser.add_argument('-v', '--verbose', help="verbose level 1", action="store_true")
    parser.add_argument('-w', '--verbose2', help="verbose level 2", action="store_true")
    parser.add_argument('key', help="Key to encrypt/decrypt")
    parser.add_argument('filename', help="Filename input to encrypt/decrypt")
    parser.add_argument('-o', '--output', help="Filename ouput")

    args = parser.parse_args()

    s = extract_in_file(args.filename)

    if (args.authorize != None):
        str_a = (str(args.authorize)).replace("\\n", "\n").replace("\\t", "\t")
    if (args.remove != None):
        str_r = (str(args.remove)).replace("\\n", "\n").replace("\\t", "\t")
    if (args.language != None):
        str_dico = args.language
    if (args.verbose):
        level_verbose = LEVEL_ONE_VERBOSE
    if (args.verbose2):
        level_verbose = LEVEL_TWO_VERBOSE
    if (args.output != None):
        outfilename = args.output
        
    d = dico(str_dico, "")

    if (args.cesar):
        if (args.decrypt):
            result = decrypt_cesar(s, int(args.key), str_a, level_verbose)
            if (' ' in str_r):
                result = define_space(result, d, str_a, level_verbose)
        else :
            result = encrypt_cesar(s, int(args.key), str_a, str_r, str_c, str_t, level_verbose)
    else :
        if (args.decrypt):
            result = decrypt_vigenere(s, args.key, str_a, level_verbose)
            if (' ' in str_r):
                result = define_space(result, d, str_a, level_verbose)
        else :
            result = encrypt_vigenere(s, args.key, str_a, str_r, str_c, str_t, level_verbose)

    write_in_file(outfilename, result)
