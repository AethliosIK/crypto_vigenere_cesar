#!/usr/bin/env python3
# coding: utf-8

from source.const import *
from source.dico import *

#   Retourne un couple : s sans les caractères non autorisés et un tableau de
#       couple tel que, pour tout n, memory[n] == (i, c) :
#           c : le caractère non autorisé retiré    i : le numéro où s[i] == c
def clean_with_memory(s, str_authorized, level_verbose):
    tmp = ""
    memory = []
    size = len(s)
    for i in range(0, size):
        if not s[i] in str_authorized:
            if (level_verbose >= LEVEL_TWO_VERBOSE):
                print("{} memorized and removed.".format(s[i]))
            memory.append((i, s[i]))
        else:
            tmp += s[i]
    return (tmp, memory)

#   Replace les caractères de memory dans s au endroits correspondant
#       en respectant les rêgles de ponctuation.
def recovery_memory(s, memory, level_verbose):
    nb_char = 0
    i = 0
    index_in_memory = 0
    size_memory = len(memory)
    size_s = len(s)
    #On parcourt s, quand on se trouve à la position indiquée dans la mémoire,
    #   on replace le caractère à sa place en respectatn les rêgles de ponctuation
    while (i < len(s)):
        if (index_in_memory == size_memory):
            break
        (position, character) = memory[index_in_memory]
        if (nb_char == position):
            # Rêgles de ponctuation :
            # On doit mettre un espace avant.
            if (character in SPACE_BEFORE):
                if (level_verbose >= LEVEL_TWO_VERBOSE):
                    print("{} recovered with one space before.".format(character))
                if (s[i] != ' '):
                    s = s[:i] + " " + character + s[i:]
                else:
                    s = s[:(i + 1)] + character + s[(i + 1):]
            # On doit mettre un espace après.
            elif (character in SPACE_AFTER):
                if (level_verbose >= LEVEL_TWO_VERBOSE):
                    print("{} recovered with one space after.".format(character))
                if (s[i] != ' '):
                    s = s[:i] + character + " " + s[i:]
                else:
                    s = s[:i] + character + s[i:]
            # On doit avoir aucun espace avant et après.
            elif (character in NO_SPACE_BEFORE_AFTER and s[i] == ' '):
                if (level_verbose >= LEVEL_TWO_VERBOSE):
                    print("{} recovered with no space before and after.".format(character))
                s = s[:i] + character + s[(i + 1):]
            # On recopie tel quel.
            else:
                if (level_verbose >= LEVEL_TWO_VERBOSE):
                    print("{} recovered.".format(character))
                s = s[:i] + character + s[i:]
            #On prendra la prochaine mémoire
            index_in_memory += 1
        if (s[i] != ' '):
            nb_char += 1
        i += 1
    return s

#   Renvoie la chaîne s avant les espaces retrouvés grâce à un système
#       de scoring à l'aide d'un dictionnaire de mots dic.
def define_space(s, d, str_authorized, level_verbose=DEFAULT_LEVEL_VERBOSE):
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("Define spaces in string input :")
    # On retire les caractères non autorisés.
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("Memorise and clean all characters not authorized.")
    (s, memory) = clean_with_memory(s, str_authorized, level_verbose)
    current = 0
    size = len(s)
    biggest_words = [""]*(size + 1)
    tab = [0]*(size + 1)
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("Calculate scores for windows of size = {}".format(SIZE_WINDOW))
    while (current <= size):
        best_score = 0
        # On parcourt un échantillon de caractère de taille 0 à SIZE_WINDOW
        for i in range(max(0, current - SIZE_WINDOW), current):
            size_word = current - i
            word = s[i:current]
            # On récupère la partie du dictionnaire commençant par la première lettre de word.
            dictionnary_first_letter = d.getList(word[0])
            # Si le mot est reconnu dans le dictionnaire, on augmente le score
            if (word in dictionnary_first_letter):
                score = tab[i] + (size_word - 1) * (size_word - 1)
            else:
                score = tab[i]
            # Si le score est meilleur, on stocke le score et le mot
            #   dans le tableau des plus grand mot à l'index current
            #   pour le retrouver lors de la création de la chaîne avec espaces
            if (score > best_score):
                best_score = score
                if (level_verbose >= LEVEL_TWO_VERBOSE):
                    print("Best {} =\t'{}'".format(current, word))
                biggest_words[current] = word
            elif (level_verbose >= LEVEL_TWO_VERBOSE):
                    print("\t\t'{}'".format(word))
        # Si on n'a pas trouvé de plus grand mot pour l'échantillon, on stocke
        #   le mot tel quel.
        if (biggest_words[current] == ""):
            biggest_words[current] = s[max(0, current - SIZE_WINDOW):current]
        if (level_verbose >= LEVEL_TWO_VERBOSE):
            print("Calculate best score for window [{},{}] = {}".format(max(0, current - SIZE_WINDOW), current, best_score))
        tab[current] = best_score
        current += 1
    # Ici on va reconstruire la chaîne avec les espaces en décrémentant current
    #   de la taille de chaque mot que l'on a trouvé de plus grand.
    #   Result va ainsi se créer en partant de la fin et en ajoutant un espace
    #       entre chaque mots.
    result = ""
    current -= 1
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("Recompose string with words which have the best score.")
    while (current > 0):
        if (level_verbose >= LEVEL_TWO_VERBOSE):
            print("The word : \"{}\" is added before.".format(biggest_words[current]))
        result = biggest_words[current] + " " + result
        current -= len(biggest_words[current])
    # On retrouve la mémoire des caractères non autorisés
    if (level_verbose >= LEVEL_ONE_VERBOSE):
        print("Recovery the memory of forbidden characters")
    result = recovery_memory(result, memory, level_verbose)
    return result
