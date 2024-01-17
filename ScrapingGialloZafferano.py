import json
import os
import re

import pandas as pd
from string import digits
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


debug = False
path_dataset = "Dataset/GialloZafferanoDataset.csv"
pattern = r'[-+]?\d*\.\d+|\d+'


def cancellaRicetteIngredientiNull():
    df = pd.read_csv(path_dataset)

    dizionarioIngredienti = json.load(open("../dizionario.json"))
    for index, ricetta in df.iterrows():
        for chiave in dizionarioIngredienti:
            if dizionarioIngredienti[chiave] is None:
                if chiave in ricetta["Ingredienti"]:
                    df = df.drop(index)
                    index = 0
                    ricetta = df.iloc[index]

    return dizionarioIngredienti, df

def findGlutine(soup):
    glutine = '0'
    for tag in soup.find_all(attrs={"class": "gz-icon gz-icon-benessere-senza-glutine"}):
        glutine = '1'
        break
    return glutine
def findLattosio(soup):
    lattosio = '0'
    for tag in soup.find_all(attrs={"class": "gz-icon gz-icon-benessere-senza-lattosio"}):
        lattosio = '1'
        break
    return lattosio
def findVegano(soup):
    vegano = '0'
    for tag in soup.find_all(attrs={"class": "gz-icon gz-icon-benessere-vegetariane"}):
        vegano = '1'
        break
    return vegano

def saveRecipe(linkRecipeToDownload, df):
    soup = downloadPage(linkRecipeToDownload)

    title = findTitle(soup)
    ingredients = findIngredients(soup)
    description = findDescription(soup)
    allInformation = findInformation(soup)
    valoriNutrizionali = findVal(soup)
    glutine = findGlutine(soup)
    lattosio = findLattosio(soup)
    vegano = findVegano(soup)
    tipo = findTipo(soup)
    interazione = findInterazioni(soup)
    raiting = findRaiting(soup)
    if allInformation is not None:
        df.loc[len(df)] = {"Titolo": title, "Descrizione": description, "Raiting": raiting, "Interazioni": interazione, "TipologiaPietanza": tipo, "Ingredienti": ingredients,
                           "Difficoltà": allInformation[0][1], "Preparazione": allInformation[1][1], "Cottura": allInformation[2][1], "Dosi": allInformation[3][1], "Energia(kcal)": valoriNutrizionali[0],
                           "Carboidrati(g)": valoriNutrizionali[1], "Zuccheri(g)": valoriNutrizionali[2], "Proteine(g)": valoriNutrizionali[3], "Grassi(g)": valoriNutrizionali[4], "GrassiSaturi(g)": valoriNutrizionali[5],
                           "Fibre(g)": valoriNutrizionali[6], "Colesterolo(mg)": valoriNutrizionali[7], "Sodio(mg)": valoriNutrizionali[8], "SenzaGlutine": glutine,"SenzaLattosio": lattosio, "Vegano": vegano}

def findTitle(soup):
    titleRecipe = ""
    for title in soup.find_all(attrs={"class": "gz-title-recipe gz-mBottom2x"}):
        titleRecipe = title.text
    return titleRecipe

def findIngredients(soup):
    allIngredients = []
    for tag in soup.find_all(attrs={"class": "gz-ingredient"}):
        link = tag.a.get("href")
        nameIngredient = tag.a.string
        contents = tag.span.contents[0]
        quantityProduct = re.sub(r"\s+", " ", contents).strip()
        allIngredients.append([nameIngredient, quantityProduct])
    return allIngredients

def findVal(soup):
    allVal = {0:"0", 1:"0", 2:"0", 3:"0", 4:"0", 5:"0", 6:"0", 7:"0", 8:"0"}
    cont = -1
    cont2 = -1

    for tag in soup.find_all(attrs={"class": "gz-list-macros-name"}):
        cont += 1
        for tag in soup.find_all(attrs={"class": "gz-list-macros-value"}):
            cont2 += 1
            if cont == cont2:
                value = tag.text
                allVal[cont] = value
                cont2 = -1
                break
    return allVal


def findInformation(soup):
    allInformation = []

    for tag in soup.find_all(attrs={"class": "gz-name-featured-data"}):
        information = tag.text.split(":")
        if information[0] != tag.text:
            if information[0] == 'Costo':
                break;
            allInformation.append([information[0], information[1].replace(" ", "")])

    if (len(allInformation) == 2 or len(allInformation) == 1 or len(allInformation) == 0):
        return

    allInformation[1][1] = re.sub(r"[a-zA-Z]", "", allInformation[1][1])
    if (len(allInformation) >= 2):
        allInformation[2][1] = re.sub(r"[a-zA-Z]", "", allInformation[2][1])

    if (len(allInformation) <= 3):
        allInformation.append(["Dosi", allInformation[2][1]])
        allInformation[2][0] = "Cottura"
        allInformation[2][1] = "0"
    elif (len(allInformation) == 4):
        allInformation[3][0] = "Dosi"
        allInformation[3][1] = re.sub(r"[a-zA-Z]", "", allInformation[3][1])

    if (len(allInformation) == 6):
        allInformation.pop(6)

    return allInformation;


def findDescription(soup):
    allDescription = ""
    for tag in soup.find_all(attrs={"class": "gz-content-recipe-step"}):
        removeNumbers = str.maketrans("", "", digits)
        if hasattr(tag.p, "text"):
            description = tag.p.text.translate(removeNumbers)
            allDescription = allDescription + description
    return allDescription


def downloadPage(linkToDownload):
    response = requests.get(linkToDownload)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
def findTipo(soup):
    for tag in soup.find_all(attrs={"class": "gz-breadcrumb"}):
        break
    list_items = (tag.find('li'))

    tipo = ""
    if list_items != None:
        elementi = list_items.find_all('a')
        for elemento in elementi:
            tipo = elemento.get('title')
            if tipo == None:
                tipo = 0
            elif "Antipasti" in tipo:
                tipo = 1
            elif "Primi Piatti" in tipo:
                tipo = 2
            elif "Secondi piatti" in tipo:
                tipo = 3
            elif "Lievitati" in tipo:
                tipo = 4
            elif "Contorni" in tipo:
                tipo = 5
            elif "Insalate" in tipo:
                tipo = 5
            elif "Salse e Sughi" in tipo:
                tipo = 6
            elif "Dolci" in tipo:
                tipo = 7
            elif "Piatti Unici" in tipo:
                tipo = 8
            elif "Torte salate" in tipo:
                tipo = 9
            elif "Bevande" in tipo:
                tipo = 10
            elif "Marmellate e Conserve" in tipo:
                tipo = 11
            elif "nan" in tipo:
                tipo = 0
    else:
        tipo = 0
    return tipo

def findInterazioni(soup):
    div_tags = soup.find_all('div', class_='rating_rate')
    for div_tag in div_tags:
        title = div_tag.get('title')
        if title is not None:
            votes_value = int(title.split()[0])
        else:
            votes_value = 0

    return votes_value

def findRaiting(soup):
    div_elements = soup.find_all('div', class_='gz-rating-panel', id='rating_panel_top')
    for div_element in div_elements:
        # Estrai il valore dell'attributo data-content-rate
        content_rate = div_element['data-content-rate']
        if content_rate != '':
            content_rate = float(content_rate.replace(",","."))
        else:
            content_rate = 0
    return content_rate

def downloadAllRecipesFromGialloZafferano():
    totalPages = countTotalPages() + 1
    features = ["Titolo", "Descrizione", "Raiting", "Interazioni", "TipologiaPietanza", "Ingredienti", "Difficoltà", "Preparazione", "Cottura", "Dosi", "Energia(kcal)", "Carboidrati(g)",
                "Zuccheri(g)", "Proteine(g)", "Grassi(g)", "GrassiSaturi(g)", "Fibre(g)", "Colesterolo(mg)", "Sodio(mg)", "SenzaGlutine", "SenzaLattosio", "Vegano"]
    df = pd.DataFrame(columns=features)
    # for pageNumber in range(1,totalPages):
    for pageNumber in tqdm(range(1, totalPages), desc="pages…", ascii=False, ncols=75):
        linkList = "https://www.giallozafferano.it/ricette-cat/page" + str(pageNumber)
        response = requests.get(linkList)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup.find_all(attrs={"class": "gz-title"}):
            link = tag.a.get("href")
            saveRecipe(link, df)
            df.to_csv(path_dataset)
            if debug:
                break
        if debug:
            break

    df.to_csv(path_dataset)
    print("Salvataggio ricette in GialloZafferanoDataset.csv completato con successo!")


def countTotalPages():
    numberOfPages = 0
    linkList = "https://www.giallozafferano.it/ricette-cat"
    response = requests.get(linkList)
    soup = BeautifulSoup(response.text, "html.parser")
    for tag in soup.find_all(attrs={"class": "disabled total-pages"}):
        numberOfPages = int(tag.text)
    return numberOfPages


def salvataggioDizionario(dizionario):
    with open("dizionario.json", "w") as fp:
        json.dump(dizionario, fp)
    return

def rimuoviParentesi(dizionarioAppoggio):
    for chiave in dizionarioAppoggio:
        if ')' in dizionarioAppoggio[chiave]:
            dizionarioAppoggio[chiave] = dizionarioAppoggio[chiave].replace(")", "")
    return dizionarioAppoggio

def sostituisciValore(df):
    df['GrassiSaturi(g)'] = df['GrassiSaturi(g)'].astype(str)
    for indice, riga in df.iterrows():
        stringa = riga['GrassiSaturi(g)']
        if '*' in stringa:
            df.loc[indice, 'GrassiSaturi(g)'] = stringa.replace('*', '')
        elif re.match(r'\b\d+(\.\d+){2}\b', stringa):
            posizioneSecondoPunto = stringa.find(".", stringa.find(".") + 1)
            df.loc[indice, 'GrassiSaturi(g)'] = stringa[:posizioneSecondoPunto]
        if re.match(r'[a-z]',stringa):
            df = df.drop(indice, axis=0)
        if re.match(r'\b\d+\.{2}\d+\b',stringa):
            df.loc[indice, 'GrassiSaturi(g)'] = stringa.replace('.', '')

    df['Zuccheri(g)'] = df['Zuccheri(g)'].astype(str)
    for indice, riga in df.iterrows():
        stringa = riga['Zuccheri(g)']
        if '*' in stringa:
            df.loc[indice, 'Zuccheri(g)'] = stringa.replace('*', '')
        elif re.match(r'\b\d+(\.\d+){2}\b', stringa):
            posizioneSecondoPunto = stringa.find(".", stringa.find(".") + 1)
            df.loc[indice, 'Zuccheri(g)'] = stringa[:posizioneSecondoPunto]

    df['Carboidrati(g)'] = df['Carboidrati(g)'].astype(str)

    for indice, riga in df.iterrows():
        stringa = riga['Carboidrati(g)']
        if '*' in stringa:
            df.loc[indice, 'Carboidrati(g)'] = stringa.replace('*', '')
        elif re.match(r'\b\d+(\.\d+){2}\b', stringa):
            posizioneSecondoPunto = stringa.find(".", stringa.find(".") + 1)
            df.loc[indice, 'Carboidrati(g)'] = stringa[:posizioneSecondoPunto]

    return df


if __name__ == "__main__":
    ingredienti = []
    if os.path.exists(path_dataset):
        print("Dataset di ricette precedentemente scaricato!")

    else:
        print("Scarico dati da Giallo Zafferano...")
        downloadAllRecipesFromGialloZafferano()
        print("Terminato scaricamento dati da Giallo Zafferano con successo!")

        df = pd.read_csv(path_dataset)

        df = sostituisciValore(df)
        df['Preparazione'] = df['Preparazione'].astype(float)
        df['Difficoltà'] = df['Difficoltà'].astype(str)
        df['Cottura'] = df['Cottura'].astype(float)
        df['Dosi'] = df['Dosi'].astype(float)
        df['Energia(kcal)'] = df['Energia(kcal)'].astype(float)
        df['Carboidrati(g)'] = df['Carboidrati(g)'].astype(float)
        df['Zuccheri(g)'] = df['Zuccheri(g)'].astype(float)
        df['Proteine(g)'] = df['Proteine(g)'].astype(float)
        df['Grassi(g)'] = df['Grassi(g)'].astype(float)
        df['GrassiSaturi(g)'] = df['GrassiSaturi(g)'].astype(float)
        df['Fibre(g)'] = df['Fibre(g)'].astype(float)
        df['Colesterolo(mg)'] = df['Colesterolo(mg)'].astype(float)
        df['Sodio(mg)'] = df['Sodio(mg)'].astype(float)

        # Moltofacile -> 0, Facile = 1, Media = 2, Difficile = 3, Moltodifficile = 4
        for indice, riga in df.iterrows():
            if riga['Difficoltà'] == "Moltofacile":
                df.loc[indice, 'Difficoltà'] = "0"
            elif riga['Difficoltà'] == "Facile":
                df.loc[indice, 'Difficoltà'] = "1"
            elif riga['Difficoltà'] == "Media":
                df.loc[indice, 'Difficoltà'] = "2"
            elif riga['Difficoltà'] == "Difficile":
                df.loc[indice, 'Difficoltà'] = "3"
            elif riga['Difficoltà'] == "Moltodifficile":
                df.loc[indice, 'Difficoltà'] = "4"
            else:
                if "min" in riga['Difficoltà']:
                    stringa = riga['Difficoltà']
                    df.loc[indice, 'Cottura'] = stringa.replace('min', '')
                    df.loc[indice, 'Difficoltà'] = "2"

        numero_valori_nan_per_colonna = df.isna().sum()

        df = df.dropna(inplace=False)

        df['Colesterolo(mg)'] = df['Colesterolo(mg)'] / 1000
        df['Sodio(mg)'] = df['Sodio(mg)'] / 1000

        df = df.rename(columns={'Colesterolo(mg)': 'Colesterolo(g)',
                                'Sodio(mg)': 'Sodio(g)'})

        df.to_csv(path_dataset, index=False)