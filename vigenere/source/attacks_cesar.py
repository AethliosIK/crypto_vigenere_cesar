#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from source.const import *
from source.encrypt_decrypt import decrypt_cesar
from source.define_space import define_space
from source.dico import *
from source.util import is_alpha_min, is_alpha_maj
import re

#réalise l'attaque force brute de césar
#les clés sont testées dans l'ordre jusqu'à avoir trouver le résultat
#si aucun résultat n'est trouvé un message d'erreur est envoyé
def bruteforce_attack_cesar(message, dic, str_authorized, percent_min, level_verbose=DEFAULT_LEVEL_VERBOSE):
  i = 0
  max_percent = 0.0
  max_s = ''
  max_key = 0
  message = message.lower().replace(" ", "")
  while i < len(str_authorized):
    compteur = 0.0
    if (level_verbose >= LEVEL_ONE_VERBOSE):
      print("Test key : {}".format(i))
    s1 = define_space(decrypt_cesar(message, i, str_authorized), dic, str_authorized)
    if (level_verbose >= LEVEL_TWO_VERBOSE):
      print("Message : " + s1)
    splits = re.split("[, \!?':.\n]+", s1)
    for s2 in splits:
      if s2 != '' and s2 in dic.getList(s2[0]):
          compteur += len(s2) - 1
    percent = (compteur / len(message)) * 100.0
    if (level_verbose >= LEVEL_TWO_VERBOSE):
      print("Matching percent : {}".format(percent))
    if percent >= percent_min:
      return (s1,i)
    if percent >= max_percent:
      max_percent = percent
      max_s = s1
      max_key = i
    i += 1
  return (max_s,max_key)

LEN_ALPHABET = 26

#renvoie l'indice du maximum du tableau
#le tableau est composé de nombres d'occurences de chaque lettre
#la case 0 correspond au nombre de 'a' trouvés dans le message
#la case 1 correspond au nombre de 'b' trouvés dans le message
#et ainsi de suite jusqu'au nombre de 'z' dans la dernière case
def indexOfMostFrequentLetter(message):
  liste = []
  i = 0
  while i < LEN_ALPHABET:
    liste.append(0)
    i += 1

  for c in message:
    if is_alpha_min(c):
      liste[ord(c) - ord('a')] += 1;

  return liste.index(max(liste))

#réalise l'attaque par fréquence de césar
#les clés sont testées selon la fréquence des caractères dans le message
#si aucun résultat n'est trouvé un message d'erreur est envoyé
def frequency_attack_cesar(message, dic, str_authorized, percent_min, level_verbose=DEFAULT_LEVEL_VERBOSE):
  i = 0
  max_percent = 0.0
  max_s = ''
  max_key = 0
  index = indexOfMostFrequentLetter(message)
  if (level_verbose >= LEVEL_ONE_VERBOSE):
    print("Calculate the index of the most frequent letter")
  if (level_verbose >= LEVEL_TWO_VERBOSE):
    print("{}".format(index))
  message = message.lower().replace(" ", "")
  while i < len(str_authorized):
    compteur = 0.0
    order = ((ord(dic.getTab()[i]) - ord('a')) + len(str_authorized)) % len(str_authorized)
    k = ((index - order) + len(str_authorized)) % len(str_authorized)
    if (level_verbose >= LEVEL_ONE_VERBOSE):
      print("Test key : {}".format(k))
    s1 = define_space(decrypt_cesar(message, k, str_authorized), dic, str_authorized)
    if (level_verbose >= LEVEL_TWO_VERBOSE):
      print("Message : " + s1)
    splits = re.split("[, \!?':.\n]+", s1)
    for s2 in splits:
      if s2 != '' and s2 in dic.getList(s2[0]):
          compteur += len(s2) - 1
    percent = (compteur / len(message)) * 100.0
    if (level_verbose >= LEVEL_TWO_VERBOSE):
      print("Matching percent : {}".format(percent))
    if percent >= percent_min:
      return (s1,k)
    if percent >= max_percent:
      max_percent = percent
      max_s = s1
      max_key = k
    i += 1
  return (max_s,max_key)





