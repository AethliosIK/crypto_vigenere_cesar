#!/usr/bin/env python3
# coding: utf-8

from source.const import *
from source.coincidence import *
from source.kasiski import kasiski
from source.encrypt_decrypt import encrypt_cesar, decrypt_vigenere
from source.define_space import define_space
from source.attacks_cesar import bruteforce_attack_cesar, indexOfMostFrequentLetter
from source.dico import *
from source.util import put_punc
import itertools
import re

LEN_ALPHABET = 26
ERREUR = -1

# Calul indice relatif entre t1 et t2 pour trouver le decalage
# entre les lettres t1 et t2 de key
def relative(t1, t2_o, s_auth):
    t1_occ = l_counter(t1)
    dec_possi = []
    for g in range(0, LEN_ALPHABET):
        t2 = encrypt_cesar(t2_o, g, s_auth, "", "", "")
        t2_occ = l_counter(t2)
        som = 0
        for i in range(0, LEN_ALPHABET):
            som += (t1_occ[i] * t2_occ[i]) / (nb_all(t1_occ) * nb_all(t2_occ))
        dec_possi.append(som)
    maxi = max(dec_possi) # indice le plus grand
    if maxi < LIMITE_MIN_BENCH:
        return (ERREUR, dec_possi)
    dec = dec_possi.index(maxi)
    return (dec, dec_possi)

# Calcul le décalage entre toutes les lettres
# à partir des sous-textes dans la liste lt
# retourne un dictionaire dico(i,j) = d avec i et j indice des lettres dans key
def offsets(lt, len_key, s_auth, verbose):
    i = 0
    dico_dec = {}
    dico_l_i = {}
    while i < len_key - 1:
        j = i + 1
        while j < len_key:
            (r, l_indice) = relative(lt[i], lt[j], s_auth)
            if r == ERREUR:
                return {}
            dico_dec[(i,j)] = r
            dico_l_i[(i,j)] = l_indice
            j += 1
        i += 1
    for ind in range(1,len_key):
        som = 0
        for k in range(0,ind):
            som += dico_dec[(k,k+1)]
        if dico_dec[(0,ind)] != (som % LEN_ALPHABET):
            if dico_l_i[(0,ind)][som % LEN_ALPHABET] >= LIMITE_MIN_BENCH:
                dico_dec[(0,ind)] = som % LEN_ALPHABET
    if verbose >= LEVEL_ONE_VERBOSE:
        print("Calcul le décalage entre toutes les lettres")
        if verbose == LEVEL_TWO_VERBOSE:
            print("Les premiers décalages", dict(itertools.islice(dico_dec.items(), 15)))
    return dico_dec


# Retourne la clé dont la 1ere lettre est A et les autres le décalage
# par rapport à A sous forme de liste de décalage
def find_key(dico, len_key, verbose):
    l_letter = sorted(dico)
    i = 0
    j = i + 1
    list_d = []
    list_d.append(i)
    key = 'a'
    while j < len_key:
        d = LEN_ALPHABET - dico[(i,j)]
        if verbose == LEVEL_TWO_VERBOSE:
            print(LEN_ALPHABET, " - ", dico[(i,j)], " = ", d)
        list_d.append(d)
        key += chr(ord('a') + (d % LEN_ALPHABET))
        j += 1
    if verbose >= LEVEL_ONE_VERBOSE:
        print("décalages lettres de la clé:", list_d, "soit", key)
    return key

# Décoder avec attaque brute de cesar en decalant le texte original
# avec decrypt_vigenere et la clé théorique
def mutual(text, possi_key, punc, len_key, s_auth, dictio, per, verbose=DEFAULT_LEVEL_VERBOSE):
    text = text.lower().replace(" ", "")
    l_text = inter_text(text, len_key)
    dico = offsets(l_text, len_key, s_auth, verbose)
    if dico == {}:
        print("wrong key length chosen, changed length.")
        len_key = 0
        if (possi_key != []):
            max(possi_key)
        l_text = inter_text(text, len_key)
        dico = offsets(l_text, len_key, s_auth, verbose)
    theory_key = find_key(dico, len_key, verbose)
    text_w_p = put_punc(text, punc)
    text_d = decrypt_vigenere(text_w_p, theory_key, s_auth)
    if verbose >= LEVEL_ONE_VERBOSE:
        print("Bruteforce attack to find 1st key's letter offset")
    # teste les 26 clés avec attaque brute
    (att,key_c) = bruteforce_attack_cesar(text_d, dictio, s_auth, per)
    str_k = encrypt_cesar(theory_key, key_c, s_auth, "", "", "")
    if verbose >= LEVEL_ONE_VERBOSE:
        print("key :", str_k, "\n")
    return (str_k, att)

###### ATTAQUE ANALYSE FREQUENCIELLE #####

def list_most_freq(text):
    lmf = []
    l_occ = l_counter(text)
    most = max(l_occ)
    i = 0
    while i < len(l_occ):
        if l_occ[i] == most:
            lmf.append(i)
        i += 1
    return lmf

def is_in_lang(text, dic, percent_min, percent_max):
    compteur = 0.0
    splits = re.split("[, \!?':.\n]+", text)
    for s in splits:
        if s != '' and s in dic.getList(s[0]):
            compteur += len(s) - 1
    percent = (compteur / len(text)) * 100.0
    if percent >= percent_min:
        return (True, percent)
    elif percent >= percent_max:
        print(percent)
        return (False, percent)
    else:
        return (False, ERREUR)

# dechiffre le texte avec la clé trouvée et met les espaces;
def decrypt_n_sp(text, key, s_auth, punc, dic, verbose):
    decrypt_v = decrypt_vigenere(text, key, s_auth)
    text_w_p = put_punc(decrypt_v, punc)
    return define_space(text_w_p, dic, s_auth)

#test les autres lettres les plus fréquentes du livre
def other_keys(l_lmf, text, key, verbose, s_auth, key_len, dic, punc, per, percent_max, index):
    j = 1
    while j < len(s_auth):
        k = 0
        most = (dic.getTab())[j]
        most_ind = s_auth.index(most)
        while k < key_len:
            index = (l_lmf[k])[0]
            dec = (index - most_ind) % len(s_auth)
            c = key[k]
            rep = s_auth[dec]
            key = key[:k] + rep + key[(k+1):]
            space = decrypt_n_sp(text, key, s_auth, punc, dic, verbose)
            (b, per_m) = is_in_lang(space, dic, per, percent_max)
            if b == True:
                if verbose >= LEVEL_ONE_VERBOSE:
                        if verbose == LEVEL_TWO_VERBOSE:
                            print(c, "->", rep)
                        print("new key :", key)
                        print("On déchiffre le texte avec la clé trouvée.\n")
                return (key, space)
            elif per_m >= percent_max:
                if verbose >= LEVEL_ONE_VERBOSE:
                    print("Une des lettres de la clé a été changée.")
                    if verbose == LEVEL_TWO_VERBOSE:
                        print(c, "->", rep)
                percent_max = per_m
            else:
                key = key[:k] + c + key[(k+1):]
            k += 1
        j += 1
    return (key, "")

# teste les autres lettres les plus fréquentee des sous-textes
def other_mosts(l_lmf, most_ind, s_auth, key, verbose, text, punc, dic, per, percent_max):
    for l in l_lmf:
        if len(l) > 1 :
            i = 1
            while i < len(l):
                ind = l_lmf.index(l)
                index = l[i]
                dec = (index - most_ind) % len(s_auth)
                rep = s_auth[dec]
                c = key[ind]
                key = key[:ind] + rep + key[(ind+1):]
                space = decrypt_n_sp(text, key, s_auth, punc, dic, verbose)
                (b, per_m) = is_in_lang(space, dic, per, percent_max)
                if b == True:
                    if verbose >= LEVEL_ONE_VERBOSE:
                        if verbose == LEVEL_TWO_VERBOSE:
                            print(c, "->", rep)
                        print("new key :", key)
                        print("On déchiffre le texte avec la clé trouvée.\n")
                    return (key, space)
                elif per_m >= percent_max:
                    if verbose >= LEVEL_ONE_VERBOSE:
                        print("Une des lettres de la clé a été changée.")
                        if verbose == LEVEL_TWO_VERBOSE:
                            print(c, "->", rep)
                    percent_max = per_m
                else:
                    key = key[:ind] + c + key[(ind+1):]
                i += 1
    return (key, "")

def analysis(text, punc, key_len, s_auth, dic, per, verbose=DEFAULT_LEVEL_VERBOSE):
    text = text.lower().replace(" ", "")
    text_l = inter_text(text, key_len)
    key = ""
    most = (dic.getTab())[0] # tab[0] = la lettre la plus fréquente du livre
    most_ind = s_auth.index(most)
    if verbose == LEVEL_TWO_VERBOSE:
        print("most", most)
    i = 0
    l_lmf = []
    while i < len(text_l):
        lmf = list_most_freq(text_l[i])
        index = lmf[0]
        l_lmf.append(lmf)
        if verbose == LEVEL_TWO_VERBOSE:
            print("plus frequente du ss-txt",s_auth[index])
        dec = (index - most_ind) % len(s_auth)
        key += s_auth[dec]
        i += 1
        if verbose >= LEVEL_ONE_VERBOSE:
            print("key :",key, "\n")
    space = decrypt_n_sp(text, key, s_auth, punc, dic, verbose)
    # teste si le texte déchiffré appartient à la langue
    (b, per_m) = is_in_lang(space, dic, per, 0.0)
    if b == False:
        if verbose == LEVEL_TWO_VERBOSE:
            print("une (ou plusieurs) des lettres la plus fréquente n'étai(ent)t pas le e")
            print("Teste pour d'autres lettres que e")
        (key, space) = other_mosts(l_lmf,  most_ind, s_auth, key, verbose, text, punc, dic, per, per_m)
        if space == "":
            (key, space) = other_keys(l_lmf, text, key, verbose, s_auth, key_len, dic, punc, per, per_m, index)
            if space == "":
                print("The exact key couldn't be found. Maybe the text is too short")
                space = decrypt_n_sp(text, key, s_auth, punc, dic, verbose)
    return (key, space)
