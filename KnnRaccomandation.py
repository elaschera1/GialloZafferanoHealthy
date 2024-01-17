import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

path_dataset = "Dataset/GialloZafferanoDataset.csv"

MAX_ZUCCHERI_DIABETE = 25
MAX_CARBOIDRATI_DIABETE = 150
MAX_SODIO_DIABETE = 2.4
MAX_SODIO_IPERTENSIONE = 2
MAX_COLESTEROLO_IPERCOLESTEROLO = 300
MAX_ZUCCHERI_NESSUNAPATOLOGIA = 50
MAX_SODIO_NESSUNAPATOLOGIA = 2
MAX_CARBOIDRATI_NESSUNAPATOLOGIA = 300
class Utente:
    def categoriaRischioMalattie(self):
        if (self.bmi > 0) and (self.bmi < 18.50):
            self.rischio = "Basso (ma aumentato rischio di altre patologie)"
            self.classificazionePeso = 'Sottopeso'
        elif (self.bmi >= 18.50) and (self.bmi <= 24.99):
            self.rischio = "Medio"
            self.classificazionePeso = 'Peso normale'
        elif (self.bmi >= 25.00) and (self.bmi <= 29.99):
            self.rischio = "Abbastanza moderato"
            self.classificazionePeso = 'Sovrappeso'
        elif (self.bmi >= 30.00) and (self.bmi <= 34.99):
            self.rischio = "Moderato"
            self.classificazionePeso = 'Obeso Classe I'
        elif (self.bmi >= 35.00) and (self.bmi <= 39.99):
            self.rischio = "Grave"
            self.classificazionePeso = 'Obeso Classe II'
        elif (self.bmi > 39.99):
            self.rischio = "Molto grave"
            self.classificazionePeso = 'Obeso Classe III'

        return self.rischio

    def fabbisognoCaloricoM(self):
        energia = 0

        if (self.eta >= 0) and (self.eta <= 3):
            energia = (59.9 * self.peso) - 31
        elif (self.eta >= 4) and (self.eta <= 9):
            energia = (22.7 * self.peso) + 504
        elif (self.eta >= 10) and (self.eta <= 17):
            energia = (17.7 * self.peso) + 650
        elif (self.eta >= 18) and (self.eta <= 29):
            energia = (15.3 * self.peso) + 679
        elif (self.eta >= 30) and (self.eta <= 59):
            energia = (11.6 * self.peso) + 879
        elif (self.eta >= 60) and (self.eta <= 99):
            energia = ((11.9 * self.peso) + 700)

        return energia

    def fabbisognoCaloricoF(self):
        energia = 0
        if (self.eta >= 0) and (self.eta <= 3):
            energia = (58.3 * self.peso) - 31
        elif (self.eta >= 4) and (self.eta <= 9):
            energia = (20.3 * self.peso) + 485
        elif (self.eta >= 10) and (self.eta <= 17):
            energia = (13.4 * self.peso) + 693
        elif (self.eta >= 18) and (self.eta <= 29):
            energia = (14.7 * self.peso) + 496
        elif (self.eta >= 30) and (self.eta <= 59):
            energia = (8.7 * self.peso) + 829
        elif (self.eta >= 60) and (self.eta <= 99):
            energia = ((9.2 * self.peso) + 688)

        return energia

    def calcoloAttivitaFisica(self):
        if (self.eta >= 18) and (self.eta <= 59):
            if self.sesso == 0:  # maschio
                if self.sport == 0:  # leggero
                    return 1.55
                elif self.sport == 1:  # moderato
                    return 1.78
                elif self.sport == 2:  # pesante
                    return 2.10
            elif self.sesso == 1:  # femmina
                if self.sport == 0:  # leggero
                    return 1.56
                elif self.sport == 1:  # moderato
                    return 1.64
                elif self.sport == 2:  # pesante
                    return 1.82
        elif self.eta >= 60:
            if self.sesso == 0:  # maschio
                return 1.55
            elif self.sesso == 1:  # femmina
                return 1.56

    def calcoloKcal(self):
        costanteSport = self.calcoloAttivitaFisica()
        if self.sesso == 0:
            self.kcal = (self.fabbisognoCaloricoM() * costanteSport)
        elif self.sesso == 1:
            self.kcal = (self.fabbisognoCaloricoF() * costanteSport)
        return self.kcal

    def __init__(self):
        self.nome = input("Inserisci il nome: ")
        self.cognome = input("Inserisci il cognome: ")
        self.sesso = int(input("Inserisci il sesso(M: 0/F: 1): "))
        self.eta = int(input("Inserisci la tua età: "))
        self.altezza = float(input("Inserisci la tua altezza in metri: "))
        self.peso = float(input("Inserisci il tuo peso in Kg: "))
        self.patologia = int(input("Inserisci la tua patologia(0:Diabete, 1:Ipertensione, 2:Ipercolesterolo, "
                                   "3:Nessuna): "))
        self.vegano = int(input("Sei vegano? (1:Si, 0:No): "))
        self.senzaLattosio = int(input("Sei intollerante al lattosio? (1:Si, 0:No): "))
        self.senzaGlutine = int(input("Sei intollerante al glutine? (1:Si, 0:No): "))
        self.bmi = (self.peso / (self.altezza * self.altezza))
        self.sport = int(input("Inserisci il livello di attività fisica praticata(0:Leggero, 1:Moderato, 2:Pesante): "))
        self.rischio = self.categoriaRischioMalattie()
        self.classificazionePeso = self.classificazionePeso
        self.kcal = self.calcoloKcal()


def knnAddestramento(utente):
    df = pd.read_csv(path_dataset)
    kcalPranzoCena = utente.kcal * (1 - 20 / 100)
    print("Kcal Pranzo e cena: ", kcalPranzoCena, " Kcal")
    kcalPorzionePranzoCena = kcalPranzoCena * (1 - 40 / 100)
    kcalPorzionePrimoSecondo = kcalPorzionePranzoCena * (1 - 20 / 100)
    print("Kcal un pasto:", kcalPorzionePrimoSecondo, " Kcal\n")

    colonne = []
    if utente.patologia == 3:
        if utente.vegano == 1 and utente.senzaLattosio == 1 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Vegano', 'SenzaLattosio', 'SenzaGlutine']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 1, 1, 1]).reshape(-1, 4)
            df = df.query('`Vegano` == 1')
            df = df.query('`SenzaLattosio` == 1')
            df = df.query('`SenzaGlutine` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 0 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo]).reshape(-1, 1)
        elif utente.vegano == 1 and utente.senzaLattosio == 0 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 1]).reshape(-1, 2)
            df = df.query('`Vegano` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 1 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)','SenzaLattosio']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 1]).reshape(-1, 2)
            df = df.query('`SenzaLattosio` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 0 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'SenzaGlutine']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 1]).reshape(-1, 2)
            df = df.query('`SenzaGlutine` == 1')
        elif utente.vegano == 1 and utente.senzaLattosio == 1 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'SenzaLattosio', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaLattosio` == 1')
            df = df.query('`Vegano` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 1 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'SenzaGlutine', 'SenzaLattosio']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
            df = df.query('`SenzaLattosio` == 1')
        elif utente.vegano == 1 and utente.senzaLattosio == 0 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'SenzaGlutine', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
            df = df.query('`Vegano` == 1')
    elif utente.patologia == 0: # Diabete
        if utente.vegano == 1 and utente.senzaLattosio == 1 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Carboidrati(g)', 'Zuccheri(g)', 'Sodio(g)', 'Vegano', 'SenzaLattosio', 'SenzaGlutine']
            df = df.query('`Vegano` == 1')
            df = df.query('`SenzaLattosio` == 1')
            df = df.query('`SenzaGlutine` == 1')
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 30, 5, 0.5, 1, 1, 1]).reshape(-1, 7)
        elif utente.vegano == 0 and utente.senzaLattosio == 0 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Carboidrati(g)', 'Zuccheri(g)', 'Sodio(g)']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 30, 5, 0.5]).reshape(-1, 4)
        elif utente.vegano == 1 and utente.senzaLattosio == 0 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Carboidrati(g)', 'Zuccheri(g)', 'Sodio(g)', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 30, 5, 0.5, 1]).reshape(-1, 5)
            df = df.query('`Vegano` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 1 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Carboidrati(g)', 'Zuccheri(g)', 'Sodio(g)', 'SenzaLattosio']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 30, 5, 0.5, 1]).reshape(-1, 5)
            df = df.query('`SenzaLattosio` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 0 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Carboidrati(g)', 'Zuccheri(g)', 'Sodio(g)', 'SenzaGlutine']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 30, 5, 0.5, 1]).reshape(-1, 5)
            df = df.query('`SenzaGlutine` == 1')
        elif utente.vegano == 1 and utente.senzaLattosio == 1 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Carboidrati(g)', 'Zuccheri(g)', 'Sodio(g)','SenzaLattosio', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaLattosio` == 1')
            df = df.query('`Vegano` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 1 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Carboidrati(g)', 'Zuccheri(g)', 'Sodio(g)', 'SenzaGlutine', 'SenzaLattosio']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
            df = df.query('`SenzaLattosio` == 1')
        elif utente.vegano == 1 and utente.senzaLattosio == 0 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Carboidrati(g)', 'Zuccheri(g)', 'Sodio(g)', 'SenzaGlutine', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
            df = df.query('`Vegano` == 1')
        df = df.query(f'{0} <= `Zuccheri(g)` <= {MAX_ZUCCHERI_DIABETE}')  # 25 grammi massimo al giorno
        df = df.query(f'{0} <= `Carboidrati(g)` <= {MAX_CARBOIDRATI_DIABETE}') # 150g massimi al giorno
        df = df.query(f'{0} <= `Sodio(g)` <= {MAX_SODIO_DIABETE}') # 2.4 grammi massimo al giorno
    elif utente.patologia == 1: # Ipertensione
        if utente.vegano == 1 and utente.senzaLattosio == 1 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Sodio(g)', 'Vegano', 'SenzaLattosio', 'SenzaGlutine']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.5,1,1,1]).reshape(-1, 5)
            df = df.query('`Vegano` == 1')
            df = df.query('`SenzaLattosio` == 1')
            df = df.query('`SenzaGlutine` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 0 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Sodio(g)']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.5]).reshape(-1, 2)
        elif utente.vegano == 1 and utente.senzaLattosio == 0 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Sodio(g)', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.5, 1]).reshape(-1, 3)
            df = df.query('`Vegano` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 1 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Sodio(g)', 'SenzaLattosio']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.5, 1]).reshape(-1, 3)
            df = df.query('`SenzaLattosio` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 0 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Sodio(g)','SenzaGlutine']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.5, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
        elif utente.vegano == 1 and utente.senzaLattosio == 1 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Sodio(g)', 'SenzaLattosio', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaLattosio` == 1')
            df = df.query('`Vegano` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 1 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Sodio(g)', 'SenzaGlutine', 'SenzaLattosio']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
            df = df.query('`SenzaLattosio` == 1')
        elif utente.vegano == 1 and utente.senzaLattosio == 0 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Sodio(g)', 'SenzaGlutine', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
            df = df.query('`Vegano` == 1')

        df = df.query(f'{0} <= `Sodio(g)` <= {MAX_SODIO_IPERTENSIONE}') # 2 grammi massimo al giorno
    elif utente.patologia == 2:
        if utente.vegano == 1 and utente.senzaLattosio == 1 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Colesterolo(g)', 'Vegano', 'SenzaLattosio', 'SenzaGlutine']
            df = df.query('`Vegano` == 1')
            df = df.query('`SenzaLattosio` == 1')
            df = df.query('`SenzaGlutine` == 1')
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1, 1, 1]).reshape(-1, 5)
        elif utente.vegano == 0 and utente.senzaLattosio == 0 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Colesterolo(g)']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60]).reshape(-1, 2)
        elif utente.vegano == 1 and utente.senzaLattosio == 0 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Colesterolo(g)', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`Vegano` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 1 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Colesterolo(g)', 'SenzaLattosio']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaLattosio` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 0 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Colesterolo(g)', 'SenzaGlutine']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
        elif utente.vegano == 1 and utente.senzaLattosio == 1 and utente.senzaGlutine == 0:
            colonne = ['Energia(kcal)', 'Colesterolo(g)', 'SenzaLattosio', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaLattosio` == 1')
            df = df.query('`Vegano` == 1')
        elif utente.vegano == 0 and utente.senzaLattosio == 1 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Colesterolo(g)', 'SenzaGlutine', 'SenzaLattosio']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
            df = df.query('`SenzaLattosio` == 1')
        elif utente.vegano == 1 and utente.senzaLattosio == 0 and utente.senzaGlutine == 1:
            colonne = ['Energia(kcal)', 'Colesterolo(g)', 'SenzaGlutine', 'Vegano']
            preferenzeUtentePranzo = np.array([kcalPorzionePrimoSecondo, 0.60, 1]).reshape(-1, 3)
            df = df.query('`SenzaGlutine` == 1')
            df = df.query('`Vegano` == 1')

        df = df.query(f'{0} <= `Colesterolo(g)` <= {MAX_COLESTEROLO_IPERCOLESTEROLO}') # 300 al giorno

    knn_model = NearestNeighbors(n_neighbors=10, metric='cosine')
    knn_model.fit(df[colonne])
    distanze, indici = knn_model.kneighbors(preferenzeUtentePranzo)

    features = ["Titolo", "Descrizione", "Raiting", "Interazioni", "TipologiaPietanza", "Ingredienti", "Difficoltà",
                "Preparazione", "Cottura", "Dosi", "Energia(kcal)", "Carboidrati(g)",
                "Zuccheri(g)", "Proteine(g)", "Grassi(g)", "GrassiSaturi(g)", "Fibre(g)", "Colesterolo(g)",
                "Sodio(g)", "SenzaGlutine", "SenzaLattosio", "Vegano"]
    dfRaccomandazioni = pd.DataFrame(columns=features)

    if utente.patologia == 0:
        sommaZuccheri = 0
        sommaCarboidrati = 0
        sommaColesterolo = 0
        sommaSodio = 0
        sommaKcal = 0
        for indice in indici[0]:
            if (sommaKcal + df.iloc[indice]['Energia(kcal)'] < kcalPranzoCena
                    and sommaZuccheri + df.iloc[indice]['Zuccheri(g)'] < MAX_ZUCCHERI_DIABETE

                    and sommaSodio + df.iloc[indice]['Sodio(g)'] < MAX_SODIO_NESSUNAPATOLOGIA
                    and sommaCarboidrati + df.iloc[indice]['Carboidrati(g)'] < MAX_CARBOIDRATI_NESSUNAPATOLOGIA
            ):
                print(f"Ricetta {indice, df.iloc[indice]['Titolo']}")
                dfRaccomandazioni.loc[len(dfRaccomandazioni)] = df.iloc[indice]
                sommaKcal = sommaKcal + df.iloc[indice]['Energia(kcal)']
                sommaZuccheri = sommaZuccheri + df.iloc[indice]['Zuccheri(g)']
                sommaCarboidrati = sommaCarboidrati + df.iloc[indice]['Carboidrati(g)']
                sommaColesterolo = sommaColesterolo + df.iloc[indice]['Colesterolo(g)']
                sommaSodio = sommaSodio + df.iloc[indice]['Sodio(g)']

    elif utente.patologia == 1:
        sommaZuccheri = 0
        sommaCarboidrati = 0
        sommaColesterolo = 0
        sommaSodio = 0
        sommaKcal = 0
        for indice in indici[0]:
            if (sommaKcal + df.iloc[indice]['Energia(kcal)'] < kcalPranzoCena
                    and sommaSodio + df.iloc[indice]['Sodio(g)'] <  MAX_SODIO_IPERTENSIONE
                    and sommaZuccheri + df.iloc[indice]['Zuccheri(g)'] < MAX_ZUCCHERI_NESSUNAPATOLOGIA
                    and sommaCarboidrati + df.iloc[indice]['Carboidrati(g)'] < MAX_CARBOIDRATI_NESSUNAPATOLOGIA
            ):
                print(f"Ricetta {indice, df.iloc[indice]['Titolo']}")
                dfRaccomandazioni.loc[len(dfRaccomandazioni)] = df.iloc[indice]
                sommaKcal = sommaKcal + df.iloc[indice]['Energia(kcal)']
                sommaSodio = sommaSodio + df.iloc[indice]['Sodio(g)']
                sommaZuccheri = sommaZuccheri + df.iloc[indice]['Zuccheri(g)']
                sommaCarboidrati = sommaCarboidrati + df.iloc[indice]['Carboidrati(g)']
                sommaColesterolo = sommaColesterolo + df.iloc[indice]['Colesterolo(g)']
    elif utente.patologia == 2:
        sommaZuccheri = 0
        sommaCarboidrati = 0
        sommaColesterolo = 0
        sommaSodio = 0
        sommaKcal = 0
        for indice in indici[0]:
            if (sommaKcal + df.iloc[indice]['Energia(kcal)'] < kcalPranzoCena
                    and sommaColesterolo + df.iloc[indice]['Colesterolo(g)'] < MAX_COLESTEROLO_IPERCOLESTEROLO
                    and sommaZuccheri + df.iloc[indice]['Zuccheri(g)'] < MAX_ZUCCHERI_NESSUNAPATOLOGIA
                    and sommaSodio + df.iloc[indice]['Sodio(g)'] < MAX_SODIO_NESSUNAPATOLOGIA
                    and sommaCarboidrati + df.iloc[indice]['Carboidrati(g)'] < MAX_CARBOIDRATI_NESSUNAPATOLOGIA):
                print(f"Ricetta {indice, df.iloc[indice]['Titolo']}")
                dfRaccomandazioni.loc[len(dfRaccomandazioni)] = df.iloc[indice]
                sommaKcal = sommaKcal + df.iloc[indice]['Energia(kcal)']
                sommaColesterolo = sommaColesterolo + df.iloc[indice]['Colesterolo(g)']
                sommaSodio = sommaSodio + df.iloc[indice]['Sodio(g)']
                sommaCarboidrati = sommaCarboidrati + df.iloc[indice]['Carboidrati(g)']
                sommaZuccheri = sommaZuccheri + df.iloc[indice]['Zuccheri(g)']
    elif utente.patologia == 3:
        sommaZuccheri = 0
        sommaCarboidrati = 0
        sommaSodio = 0
        sommaColesterolo = 0
        sommaKcal = 0

        for indice in indici[0]:
            if (sommaKcal + df.iloc[indice]['Energia(kcal)'] < kcalPranzoCena
                    and sommaZuccheri + df.iloc[indice]['Zuccheri(g)'] < MAX_ZUCCHERI_NESSUNAPATOLOGIA
                    and sommaSodio + df.iloc[indice]['Sodio(g)'] < MAX_SODIO_NESSUNAPATOLOGIA
                    and sommaCarboidrati + df.iloc[indice]['Carboidrati(g)'] < MAX_CARBOIDRATI_NESSUNAPATOLOGIA):
                print(f"Ricetta {indice, df.iloc[indice]['Titolo']}")
                dfRaccomandazioni.loc[len(dfRaccomandazioni)] = df.iloc[indice]
                sommaKcal = sommaKcal + df.iloc[indice]['Energia(kcal)']
                sommaColesterolo = sommaColesterolo + df.iloc[indice]['Colesterolo(g)']
                sommaSodio = sommaSodio + df.iloc[indice]['Sodio(g)']
                sommaCarboidrati = sommaCarboidrati + df.iloc[indice]['Carboidrati(g)']
                sommaZuccheri = sommaZuccheri + df.iloc[indice]['Zuccheri(g)']

    dfRaccomandazioni.to_csv("Dataset/ricetteRaccomandate.csv")

    print("Salvataggio raccomandazioni in 'ricetteRaccomandate.csv' avvenuto con successo!")

paziente = Utente()

print("\n Rischio Malattie: ", paziente.rischio)
print("Classificazione peso: ", paziente.classificazionePeso)
print("Apporto calorico giornaliero consigliato: ", paziente.kcal, "Kcal")

knnAddestramento(paziente)



