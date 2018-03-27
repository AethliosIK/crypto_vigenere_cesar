#!/usr/bin/env python3
# coding: utf-8

from source.const import *
from source.util import clean_espace

#   Permet d'effectuer la transformation de c en caratère autorisé et indiqué
#       par str_to_changed : si c est compris dans la partie i séparée par des |
#       On change c par le caractère str_to_changed[i]
def changed_char(c, str_changed, str_to_changed, level_verbose):
    tab = str_changed.split(SEPARATOR)
    size_to_changed = len(str_to_changed)
    i = 0
    for letters_to_changed in tab:
        if c in letters_to_changed:
            if (level_verbose >= LEVEL_TWO_VERBOSE):
                print("Character {} are changed to {}".format(c, str_to_changed[i]))
            return str_to_changed[i]
        i += 1
        if (i > size_to_changed):
            print("Problem in your str_to_changed or str_changed")
            exit(1)
    return c

#   Retourne la position du caractère c dans str_authorized, -1 si erreur
def extract(c, str_authorized):
    if (not (c in str_authorized)):
        return -1
    return str_authorized.index(c)

#   Supprime dans s les caractères présents dans str_removed et effectue le
#       changement pour tous les caractère dans str_changed grâce à changed_char
def clean(s, str_removed, str_changed, str_to_changed, level_verbose):
    tmp = ""
    for c in s:
        c = c.lower()
        if c in str_changed:
            c = changed_char(c, str_changed, str_to_changed, level_verbose)
        elif c in str_removed:
            if (level_verbose >= LEVEL_TWO_VERBOSE):
                print("Character {} are removed".format(c))
            c = ''
        tmp += c
    return tmp

# Retourne la chaîne s chiffrée par vigenère grâce à la clé s_key pour l'alphabet
#   str_authorized en supprimant les caractères str_removed et en changeant
#   les caractères de str_changed par les caractères correspondant
#   dans str_to_changed
def encrypt_vigenere(s, s_key, str_authorized, str_removed, str_changed, str_to_changed, level_verbose=DEFAULT_LEVEL_VERBOSE):
    tmp = ""
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("Character forbidden are removed or changed.")
    s = clean(s, str_removed, str_changed, str_to_changed, level_verbose)
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("Spaces are cleaned and uppercases are changed in key.")
    s_key = clean_espace(s_key).lower()
    i = 0
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("For all characters of string input, it's encryptd.")
    for c in s:
        key = extract(s_key[i], str_authorized)
        if (key == -1):
            print("Error in key")
            exit(1)
        new_c = c
        if c in str_authorized:
            ord_c = extract(c, str_authorized)
            new_c = str_authorized[(ord_c + key) % len(str_authorized)]
            i = (i + 1) % len(s_key)
            if (level_verbose >= LEVEL_TWO_VERBOSE):
                print("{} - {} -> {}".format(c, key, new_c))
        else:
            #le caractère est ignoré
            if (level_verbose >= LEVEL_TWO_VERBOSE):
                print("{} -> {}".format(c, new_c))
        tmp += new_c
    return tmp

# Retourne la chaîne s déchiffrée par vigenère grâce à la clé s_key pour l'alphabet
#   str_authorized
def decrypt_vigenere(s, s_key, str_authorized, level_verbose=DEFAULT_LEVEL_VERBOSE):
    tmp = ""
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("Space are cleaned in key.")
    s_key = clean_espace(s_key).lower()
    i = 0
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("For all characters in string, they are decrypt with key.")
    for c in s:
        key = extract(s_key[i], str_authorized)
        new_c = c
        if (key == -1):
            print("Error in key")
            exit(1)
        if c in str_authorized:
            ord_c = extract(c, str_authorized)
            new_c = str_authorized[(ord_c - key) % len(str_authorized)]
            if (level_verbose >= LEVEL_TWO_VERBOSE):
                print("{} - {} -> {}".format(c, key, new_c))
            i = (i + 1) % len(s_key)
        else:
            #le caractère est ignoré
            if (level_verbose >= LEVEL_TWO_VERBOSE):
                print("{} -> {}".format(c, new_c))
        tmp += new_c
    return tmp

# Retourne la chaîne de caractère s chiffrée avec César
#   à l'aide de l'entier key comme clé.
def encrypt_cesar(s, key, str_authorized, str_removed, str_changed, str_to_changed, level_verbose=DEFAULT_LEVEL_VERBOSE):
    return encrypt_vigenere(s, str_authorized[(key % len(str_authorized))], str_authorized, str_removed, str_changed, str_to_changed, level_verbose)

# Retourne la chaîne de caractère s déchiffrée avec César
#   à l'aide de l'entier key comme clé.
def decrypt_cesar(s, key, str_authorized, level_verbose=DEFAULT_LEVEL_VERBOSE):
    return decrypt_vigenere(s, str_authorized[(key % len(str_authorized))], str_authorized, level_verbose)
