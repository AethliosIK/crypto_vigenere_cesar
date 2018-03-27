#!/usr/bin/env python3
# coding: utf-8

from source.const import *
from source.util import is_alpha_min, is_alpha_maj

ASCII_LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'

#créer la liste associée au dictionnaire à partir du fichier texte contenant les mots
def createList(f):
  fichier = open(f, "r")
  liste = []
  i = 0
  while i < 26:
    liste.append([])
    i += 1

  for line in fichier.readlines():
    line = line.split('\n')[0]
    liste[ord(line[0]) - ord('a')].append(line)
  fichier.close()
  return liste

#analyse le livre associé au dictionnaire et renvoie le tableau des caractères
#triés du plus fréquent au moins fréquent
def analyseBook(book, level_verbose):
  fichier = open(book, "r")
  liste = []
  i = 0
  while i < 26:
    liste.append(0)
    i += 1

  #parcours de tous les caractères du livre
  for e in fichier:
    e = e.split()
    for d in e:
      for c in d:
        if is_alpha_min(c):
          liste[ord(c) - ord('a')] += 1
        elif is_alpha_maj(c):
          liste[ord(c) - ord('A')] += 1
        elif c == 'é' or c == 'ê' or c == 'è' or c == 'È' or c == 'Ê' or c == 'É' or c == 'ë' or c == 'Ë':
          liste[ord('e') - ord('a')] += 1
        elif c == 'î' or c == 'Î' or c == 'ï' or c == 'Ï':
          liste[ord('i') - ord('a')] += 1
        elif c == 'à' or c == 'â' or c == 'Â' or c == 'À' or c == 'ä' or c == 'Ä':
          liste[0] += 1
        elif c == 'ô' or c == 'Ô' or c == 'ö' or c == 'Ö':
          liste[ord('o') - ord('a')] += 1
        elif c == 'ù' or c == 'Û' or c == 'û' or c == 'ü' or c == 'Ü':
          liste[ord('u') - ord('a')] += 1

  fichier.close()
  tab = []

  #on ajoute dans le tableau un couple avec le caractère char et
  #le nombre caractères char trouvés dans le livre
  k = 0
  for cpt in liste:
    char = chr(ord('a') + k)
    tab.append((cpt, char))
    k += 1
  if (level_verbose >= LEVEL_TWO_VERBOSE):
    print("Table of caracters and their number in the book : ")
    print(tab)
  #on tri le tableau en fonction du nombre de caractères
  stab = sorted(tab)
  if (level_verbose >= LEVEL_TWO_VERBOSE):
    print("Sorted table with number of caracters : ")
    print(stab)
  #puis on renverse le tableau stab obtenu puisque sorted donne un tableau
  #trié dans l'ordre croissant
  j = 25
  k = 25
  tab2 = []
  size = 0
  while k >= 0:
    (c, l) = stab[k]
    size += c
    k -= 1
  if (level_verbose >= LEVEL_TWO_VERBOSE):
    print("Sorted table with caracters and percentage of apparition : ")
  while j >= 0:
    (c, l) = stab[j]
    if (level_verbose >= LEVEL_TWO_VERBOSE):
      print("{} - {}%".format(l, (float(c) / float(size)) * 100.0))
    tab2.append(l)
    j -= 1
  if (level_verbose >= LEVEL_ONE_VERBOSE):
    print("Table of caracters sorted most frequent to less : ")
    print(tab2)
  return tab2

#classe dictionnaire
class dico():
  def __init__(self, filename, book, level_verbose=DEFAULT_LEVEL_VERBOSE):
    self.filename = filename
    self.l = []
    if (filename != ""):
      self.l = createList(filename)
    self.tab = []
    if (book != ""):
      self.tab = analyseBook(book, level_verbose)
    self.book = book

  #permet de récupérer le fichier texte contenant les mots du dictionnaire
  def getFile(self):
    return self.fichier

  #permet de récupérer la liste des mots du dictionnaire
  #cette liste est composée de sous listes contenant chacune
  #tous les mots du dictionnaire commencant par la même lettre
  def getList(self, firstLetter):
    if (firstLetter in ASCII_LOWERCASE):
      return self.l[ord(firstLetter)  - ord('a')]
    print("{} is not ascii lowercase.".format(firstLetter))
    exit(1)

  #permet de récupérer le tableau de fréquence des caractères
  #le tableau est composé de caractères, le caractère le plus fréquent
  #est situé en position 0
  def getTab(self):
    return self.tab

  #permet de récupérer le livre associer au dictionnaire
  def getBook(self):
    return self.book
