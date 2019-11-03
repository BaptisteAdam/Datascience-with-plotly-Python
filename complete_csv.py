import json
import requests

import pandas as pd
import numpy as np

import plan_b

# ------------------------------------------------------------------------------------
# Fonctions
# ------------------------------------------------------------------------------------

def sentence_split(sentence):
    new_sentence = sentence[:]
    for letter in sentence:
        if not letter.isalnum():
            new_sentence = new_sentence.replace(letter, ' ')
    return new_sentence.split()

def build_geoloc_data(csv):
    doc = {'N':'north', 'S':'south', 'E':'east', 'W':'west'}
    prob = {
        'S MC VICKER AVE':'south%20MCVICKER%20AVE',
        'W FIFTH AVE':'W%205TH%20AVE',
        'S DR MARTIN LUTHER KING JR DR':'S%20KING%20DR'
    }
    lats = []
    longs = []
    debut_url = "https://nominatim.openstreetmap.org/search/"
    fin_url = ",%20chicago?format=json&addressdetails=1&limit=1&polygon_svg=1&email=baptiste.adam@edu.esiee.fr"
    for location in csv['block']:
        new_location = ''
        # adapter l'adresse a l'API
        if location[6:] in prob.keys():
            # tricher pour les adresses qui posent probleme
            new_location = prob[location[6:]]
        else:
            split = sentence_split(location[6:])
            for j, mot in enumerate(split[:2]):
                if mot in doc.keys():
                    split[j] = doc[mot]
            for mot in split:
                new_location += mot+'%20'
            new_location = new_location[:len(new_location)-3]
        # obtenir la reponse de l'API
        url = debut_url + new_location + fin_url
        req = requests.get(url)
        datas = json.loads(req.text)
        # sauvegarder lat et lon
        lats.append(float(datas[0]['lat']))
        longs.append(float(datas[0]['lon']))
    csv['lat'] = np.array(lats)
    csv['lon'] = np.array(longs)

# ------------------------------------------------------------------------------------
# Data
# ------------------------------------------------------------------------------------

print("Chargement des donnees")
CSV = pd.read_csv("Sex_Offenders.csv")

print("Preparation des donnees")
# enlever le Caps Lock des noms de colonnes
LISTE = []
for elem in CSV.columns:
    LISTE.append(elem.lower())
CSV.columns = LISTE

# enlever le Caps Lock des colonnes concernees
    # garder la premier majuscule des prenoms
for i in range(len(CSV['first'])):
    CSV.loc[i, 'first'] = CSV.loc[i, 'first'][0]+CSV.loc[i, 'first'][1:].lower()

    # completement "de-caps lock" les autres colonnes
COLUMNS = CSV.columns[3:5]
for column in COLUMNS:
    for i in range(len(CSV[column])):
        CSV.loc[i, column] = CSV.loc[i, column].lower()

# Corriger les erreurs humaines detectee manuellement
    # ligne 74 est un inversement de colonne
WEIGHT = CSV.loc[343, 'height']
CSV.loc[74, 'height'] = CSV.loc[74, 'weight']
CSV.loc[74, 'weight'] = WEIGHT
    # ligne 343 est un inversement de colonne
WEIGHT = CSV.loc[343, 'height']
CSV.loc[343, 'height'] = CSV.loc[343, 'weight']
CSV.loc[343, 'weight'] = WEIGHT
    # ligne 754 est un oublie de 0 lors de la saisie
CSV.loc[754, 'height'] *= 10

print("Completion des donnees")
# update les ages pour 2019
AGES = CSV["age"]+2
CSV['age'] = AGES

# obtenir le nom complet dans un seul champs
CSV['name'] = CSV['first']+' '+CSV['last']

# convertir les tailles (pieds, pouces vers metres)
PIEDS = (CSV['height']/100).apply(round)
POUCES = CSV['height'] - PIEDS*100
CSV['height (m)'] = (PIEDS/3.281 + POUCES/39.37).apply(lambda x: round(x, 2))

# convertir les masses (livres vers kilogrammes)
CSV['weight (Kg)'] = (CSV['weight']/2.205).apply((lambda x: round(x, 2)))

# obtenir une classification des victimes plus parlante que Y/N
for i, victim  in enumerate(CSV["victim minor"]):
    if victim != 'Y':
        CSV.loc[i, 'victim'] = 'major'
    else:
        CSV.loc[i, 'victim'] = 'minor'

print("Obtention des coordonnees geograpthique")
# ajouter les coordonnees
#build_geoloc_data(CSV)
plan_b.get_coord(CSV)

#
CSV['total'] = np.array(['offence' for i in CSV["victim minor"]])

CSV.to_csv(path_or_buf="Sex_Offenders_completed.csv")