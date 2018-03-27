#!/usr/bin/env python3
# coding: utf-8

import operator
from source.const import *
from source.util import is_alpha_min, without_punc

LEN_ALPHABET = 26
OK = 0
ERREUR = -1

# COINCIDENCE
# compte l'occurence de chaque lettre dans le texte text.
# retourne une liste des ces occurences,  t[0] = t['a']
def l_counter(text):
    t = [0] * LEN_ALPHABET
    i = 0
    while i < len(text):
        c = text[i]
        if is_alpha_min(c):
            asc = ord(c)
            t[asc - ord('a')] += 1
        i += 1
    #print("tab occ des lettres", t)
    return t

# additionne toutes les valeurs du tableau d'occ :retourne le nb de lettres total
def nb_all(l_occ):
    nl = 0
    for value in l_occ:
        nl += value
    return nl

# Calcul de l'indice de coincidence du texte text.
def index(text):
    t = l_counter(text)
    nl = nb_all(t)
    if nl <= 1:
        return ERREUR
    som = 0
    for nc in t:
        som += (nc * (nc - 1)) / (nl * (nl - 1))
    return som

# SOUS-TEXTES
# Prend un texte en argument et retourne un liste des textes contenant
# les lettres à un intervalle de inter.
def inter_text(text, inter):
    list_txts = []
    for i in range(0, inter):
        sub_t = ""
        c = i
        while c < len(text):
            sub_t += text[c]
            c += inter
        list_txts.append(sub_t)
    return list_txts

# Test si l'indice de chaque sous-texte est assez élévé
def is_enough(l_txts, benchmark, verbose):
    dic_ind = {True: 0, False: 0}
    acc = 0
    for t in l_txts:
        indice = index(t)
        if indice == ERREUR:
            return (False, ERREUR)
        if indice == 0.00:
            acc += 1
        if acc == len(l_txts):
            return (True, ERREUR)
        if verbose == LEVEL_TWO_VERBOSE:
            print(indice)
        if indice >= benchmark:
            dic_ind[True] += 1
        else:
            dic_ind[False] += 1
    # retourne la clé du dictionnaire (true ou false) dont la valeur est la plus grande
    if (dic_ind[True] >= dic_ind[False]):
        return (True, OK)
    else:
        return (False, OK)

# Calcul la longueur de la clé en créant des sous-textes à un intervalle
# à partir de 2
# puis calcul si ces sous-textes ont un indice de coincidence >= benchmark
def coincidence(text_o, benchmark, verbose=DEFAULT_LEVEL_VERBOSE):
    text_o = text_o.lower().replace(" ", "")
    (text, punc) = without_punc(text_o)
    if verbose >= LEVEL_ONE_VERBOSE:
        print("Index of text:", index(text))
    limite = 10
    k_len = 0
    inter = 2
    while inter < limite and inter < len(text):
        if verbose >= LEVEL_ONE_VERBOSE:
            print("teste pour longueur :", inter)
        lt = inter_text(text, inter)
        (b, test) = is_enough(lt, benchmark, verbose)
        if test == OK:
            if b == True:
                k_len = inter
                limite = inter + 2
            inter += 1
            if inter == limite and k_len == 0: # si la clé fait plus de 10 lettres
                limite *= 2 # on double la limite de la boucle
            if verbose >= LEVEL_ONE_VERBOSE:
                print("\n")
        else:
            if b == True:
                print("WARNING: Text is too short, so the key length may be wrong.")
                k_len = inter - 1
                print("longueur de la clé :", k_len, "\n")
                return (k_len, text, punc)
            else:
                print("WARNING: Key too long for this text, try a shorter one.")
                exit(1)
    if verbose >= LEVEL_ONE_VERBOSE:
        print("longueur de la clé :", k_len, "\n")
    return (k_len, text, punc)
