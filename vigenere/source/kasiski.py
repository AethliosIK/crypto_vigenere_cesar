#!/usr/bin/env python3
# coding: utf-8

from source.const import *
from source.util import without_punc
import itertools
import operator

# Calcul la distance entre deux chaînes de caractères, de 3 lettres, identiques
# retourne une liste de toutes les distances trouvées
def calc_dist(text, verbose):
    seg = []
    list_k = []
    ld = []
    dist = 0
    i = 0
    while i < len(text):
        seg = text[i:i+3]
        for ind in range(i+1, len(text)):
            if seg == text[ind:ind+3]:
                dist = ind - i
                list_k.append(seg)
                ld.append(dist)
                seg = []
                break
        i += 1
    if verbose >= LEVEL_ONE_VERBOSE:
        print("Recherche répétition de triplets")
        if verbose == LEVEL_TWO_VERBOSE:
            if len(list_k) >= 15:
                print("Les 15 premiers triplets trouvés :\n", list_k[:15])
            else:
                print("Liste des triplets trouvés :\n", list_k)
    if list_k == []:
        print("WARNING: The text is too short for Kasiski's attack. Change it or the key.")
        exit(1)
    ld = list(set(ld))
    if verbose >= LEVEL_ONE_VERBOSE:
        print("Ajout des distances")
        if verbose == LEVEL_TWO_VERBOSE:
            if len(ld) >= 15:
                print("Les 15 premières distances :\n", ld[:15])
            else:
                print("liste des distances :\n", ld)
        print("\n")
    return ld

# Prend la liste des distances en argument,
# calcul tous les diviseurs de ces distances
# et retourne la liste de ces diviseurs
def dividers(ldist):
    list_d = []
    div = []
    for n in ldist:
        i = 2
        for i in range(2, n+1):
            if n % i == 0:
                div.append(i)
        list_d.append(div)
        div = []
    return list_d

# Prend en argument la liste des diviseurs,
# calcul l'occurrence de chaque diviseurs
# et retourne un dictionaire diviseur:occurence
def count_occ(ldiv, verbose):
    occ = {}
    for l in ldiv:
        for d in l:
            if d in occ:
                occ[d] += 1
            else:
                occ[d] = 1
    if verbose >= LEVEL_ONE_VERBOSE:
        print("Calcul l'occurrences des diviseurs")
        if verbose == LEVEL_TWO_VERBOSE:
            if len(occ) > 15:
                d_trunc = dict(itertools.islice(occ.items(), 15))
                print("15 premiers diviseurs et leur occurence (div:occ) :\n", d_trunc)
            else:
                print("Les diviseurs et leur occurence (div:occ) :\n", occ)
    return occ

# Prend en argument la liste des diviseurs possibles,
# calcul le diviseurs le plus logique en fonction du nombre
# et retourne la taille de la clé
def most_plausible(occ_div, most, verbose):
    max1 = max(most)
    most.remove(max1)
    max2 = max(most)
    if occ_div.get(max1) > occ_div.get(max2):
        len_key = max1
    else:
        len_key = max2
        most.append(max1)
        most.remove(max2)
    if verbose >= LEVEL_ONE_VERBOSE:
        print("longueurs de la clé :", len_key)
    return (len_key, most)

## Prend en argument le dictionnaire div:occ,
## calcul l'occurence la plus importante et donc plus grand diviseur
## et retourne la longueur de la clé
#def most_common_div(occ_div, verbose):
def most_common_div(occ_div, verbose):
    l_div = sorted(occ_div, key=occ_div.__getitem__) #trier les div par leur occ
    l_div.reverse()
    most = []
    occ1 = occ_div.get(l_div[0])
    i = 1
    most.append(l_div[0])
    while i < len(l_div):
        if occ_div.get(l_div[i]) == occ1:
            most.append(l_div[i])
            i = len(l_div)
        elif occ_div.get(l_div[i]) > occ1 / 2:
            most.append(l_div[i])
        else:
            i = len(l_div)
        i += 1
    if verbose >= LEVEL_ONE_VERBOSE:
        print("longueurs de clé possible :", most)
    if len(most) == 1:
        return (most[0], [])
    else:
        return most_plausible(occ_div, most, verbose)

def kasiski(text_o, verbose):
    text_o = text_o.lower().replace(" ", "")
    (text, punc) = without_punc(text_o)
    ldist = []
    ldiv = []
    occ_div = {}
    ldist = calc_dist(text, verbose)
    ldiv = dividers(ldist)
    occ_div = count_occ(ldiv, verbose)
    (len_key, possi_key) = most_common_div(occ_div, verbose)
    if verbose >= LEVEL_ONE_VERBOSE:
        print("longueur de la cle:", len_key, "\n")
    return (len_key, possi_key, text, punc)
