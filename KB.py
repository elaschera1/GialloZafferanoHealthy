from pyswip import Prolog
import pandas as pd

path_dataset = "Dataset/GialloZafferanoDataset.csv"

prolog = Prolog()
df = pd.read_csv(path_dataset)

print("Definisco la Knowledgebase!")

for index, row in df.iterrows():
    prolog.assertz(f'raiting({index}, {row["Raiting"]})')
    prolog.assertz(f'interazioni({index}, {row["Interazioni"]})')
    prolog.assertz(f'difficolta({index}, {row["Difficoltà"]})')
    prolog.assertz(f'preparazione({index}, {row["Preparazione"]})')
    prolog.assertz(f'cottura({index}, {row["Cottura"]})')
    prolog.assertz(f'senzaLattosio({index}, {row["SenzaLattosio"]})')
    prolog.assertz(f'senzaGlutine({index}, {row["SenzaGlutine"]})')
    prolog.assertz(f'vegana({index}, {row["Vegano"]})')

print("Definisco le regole!")
prolog.assertz("raitingBasso(IdRicetta):- raiting(IdRicetta,ValoreRaiting), ValoreRaiting > 0, ValoreRaiting < 1.6")
prolog.assertz("raitingMedio(IdRicetta):- raiting(IdRicetta,ValoreRaiting), ValoreRaiting >= 1.6, ValoreRaiting < 3.2")
prolog.assertz("raitingAlto(IdRicetta):- raiting(IdRicetta,ValoreRaiting), ValoreRaiting >= 3.2, ValoreRaiting < 5.1")
prolog.assertz("difficoltaMoltoFacile(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 0")
prolog.assertz("difficoltaFacile(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 1")
prolog.assertz("difficoltaMedia(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 2")
prolog.assertz("difficoltaDifficile(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 3")
prolog.assertz("difficoltaMoltoDifficile(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 4")
prolog.assertz("successoBasso(IdRicetta) :-  raitingBasso(IdRicetta), difficoltaMedio(IdRicetta)")
prolog.assertz("successoBasso(IdRicetta) :-  raitingBasso(IdRicetta), difficoltaDifficile(IdRicetta)")
prolog.assertz("successoBasso(IdRicetta) :-  raitingMedio(IdRicetta), difficoltaDifficile(IdRicetta)")
prolog.assertz("successoBasso(IdRicetta) :-  raitingBasso(IdRicetta), difficoltaMoltoDifficile(IdRicetta)")
prolog.assertz("successoBasso(IdRicetta) :-  raitingMedio(IdRicetta), difficoltaMoltoDifficile(IdRicetta)")
prolog.assertz("successoMedio(IdRicetta) :-  raitingAlto(IdRicetta), difficoltaDifficile(IdRicetta)")
prolog.assertz("successoMedio(IdRicetta) :-  raitingAlto(IdRicetta), difficoltaMoltoDifficile(IdRicetta)")
prolog.assertz("successoMedio(IdRicetta) :-  raitingBasso(IdRicetta), difficoltaFacile(IdRicetta)")
prolog.assertz("successoMedio(IdRicetta) :-  raitingBasso(IdRicetta), difficoltaMoltoFacile(IdRicetta)")
prolog.assertz("successoMedio(IdRicetta) :-  raitingMedio(IdRicetta), difficoltaMedia(IdRicetta)")
prolog.assertz("successoAlto(IdRicetta) :-   raitingAlto(IdRicetta), difficoltaMedia(IdRicetta)")
prolog.assertz("successoAlto(IdRicetta) :-   raitingAlto(IdRicetta), difficoltaFacile(IdRicetta)")
prolog.assertz("successoAlto(IdRicetta) :-   raitingMedio(IdRicetta), difficoltaFacile(IdRicetta)")
prolog.assertz("successoAlto(IdRicetta) :-   raitingMedio(IdRicetta), difficoltaMoltoFacile(IdRicetta)")
prolog.assertz("successoAlto(IdRicetta) :-   raitingAlto(IdRicetta), difficoltaMoltoFacile(IdRicetta)")
prolog.assertz("numero_interazioni_alto(IdRicetta):- interazioni(IdRicetta, Numero_interazioni), Numero_interazioni > 20")
prolog.assertz("ricetta_salutare(IdRicetta):- vegana(IdRicetta,Valore_vegana),senzaGlutine(IdRicetta,Valore_glutine),senzaLattosio(IdRicetta,Valore_lattosio), Valore_vegana == 1, Valore_glutine == 1, Valore_lattosio == 1")
prolog.assertz("ricetta_popolare(IdRicetta):- raitingAlto(IdRicetta), numero_interazioni_alto(IdRicetta)")
prolog.assertz("ricetta_Universitari(IdRicetta):- cottura(IdRicetta, ValoreTempoCottura), preparazione(IdRicetta, ValoreTempoPreparazione), ValoreTempoCottura =< 20, ValoreTempoPreparazione =< 20, ricetta_popolare(IdRicetta), difficoltaMoltoFacile(IdRicetta); difficoltaFacile(IdRicetta)")

print("Creo feature ingegnerizzate!")

for index, row in df.iterrows():
    if bool(list(prolog.query(f"ricetta_salutare({index})"))):
        df.at[index, 'ricettaSalutare'] = 1
    else:
        df.at[index, 'ricettaSalutare'] = 0

    if bool(list(prolog.query(f"ricetta_popolare({index})"))):
        df.at[index, 'ricettaPopolare'] = 1
    else:
        df.at[index, 'ricettaPopolare'] = 0

    if bool(list(prolog.query(f"ricetta_Universitari({index})"))):
        df.at[index, 'ricettaUniversitari'] = 1
    else:
        df.at[index, 'ricettaUniversitari'] = 0

print("Feature ingegnerizzate create con successo!")

df.to_csv("Dataset/GialloZafferanoDatasetProlog.csv")

print("Dataset salvato con successo!")