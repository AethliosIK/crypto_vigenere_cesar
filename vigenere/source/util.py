#!/usr/bin/env python3
# coding: utf-8

# Teste si le caractère c est une lettre minuscule.
def is_alpha_min(c):
    return (ord(c) >= ord('a') and ord(c) <= ord('z'))

# Teste si le caracère c est une lettre majuscule.
def is_alpha_maj(c):
    return (ord(c) >= ord('A') and ord(c) <= ord('Z'))

# Teste si le caractère c est une lettre.
def is_alpha(c):
    return is_alpha_maj(c) or is_alpha_min(c)

# Renvoie la string s sans ses espaces
def clean_espace(s):
    tmp = ""
    for c in s:
        if c != ' ':
            tmp += c
    return tmp

# Retourne le contenue de filename dans une chaîne de caractère
def extract_in_file(filename):
    f = open(filename, "r")
    s = ""
    for line in f.readlines():
        s += line
    f.close()
    return s

# Ecrit la chaîne s dans filename.
def write_in_file(filename, s):
    f = open(filename, "w")
    bufsize = 50
    i = 0
    while (i < len(s)):
        f.write(s[i:(i + bufsize)])
        i += bufsize
    f.close

# Retire la ponctuation du texte
def without_punc(text):
    punc_dict = {}
    tmp = text
    i = 0
    while i < len(text):
        c = text[i]
        if is_alpha_min(c) == False:
            punc_dict[i] = c
            tmp = tmp.replace(c, "")
        i += 1
    return (tmp, punc_dict)


# Remet la ponctuation du texte
def put_punc(tmp, dico):
    l_ind = list(dico)
    i = 0
    text = tmp
    while i < len(tmp) + len(l_ind):
        if i in l_ind:
            text = text[:i] + dico[i] + text[i:]
        i += 1
    return text
