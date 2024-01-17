raiting(0, 3.7).
interazioni(0, 100).
difficolta(0, 1).
preparazione(0, 20).
cottura(0, 20).
senzaLattosio(0, 0).
senzaGlutine(0, 0).
vegana(0, 0).

raitingBasso(IdRicetta):- raiting(IdRicetta,ValoreRaiting), ValoreRaiting > 0, ValoreRaiting < 1.6.
raitingMedio(IdRicetta):- raiting(IdRicetta,ValoreRaiting), ValoreRaiting >= 1.6, ValoreRaiting < 3.2.
raitingAlto(IdRicetta):- raiting(IdRicetta,ValoreRaiting), ValoreRaiting >= 3.2, ValoreRaiting < 5.1.
difficoltaMoltoFacile(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 0.
difficoltaFacile(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 1.
difficoltaMedia(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 2.
difficoltaDifficile(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 3.
difficoltaMoltoDifficile(IdRicetta):- difficolta(IdRicetta,ValoreDifficolta),ValoreDifficolta == 4.
successoBasso(IdRicetta) :- raitingBasso(IdRicetta), difficoltaMedio(IdRicetta).
successoBasso(IdRicetta) :- raitingBasso(IdRicetta), difficoltaDifficile(IdRicetta).
successoBasso(IdRicetta) :- raitingMedio(IdRicetta), difficoltaDifficile(IdRicetta).
successoBasso(IdRicetta) :- raitingBasso(IdRicetta), difficoltaMoltoDifficile(IdRicetta).
successoBasso(IdRicetta) :- raitingMedio(IdRicetta), difficoltaMoltoDifficile(IdRicetta).
successoMedio(IdRicetta) :- raitingAlto(IdRicetta), difficoltaDifficile(IdRicetta).
successoMedio(IdRicetta) :- raitingAlto(IdRicetta), difficoltaMoltoDifficile(IdRicetta).
successoMedio(IdRicetta) :- raitingBasso(IdRicetta), difficoltaFacile(IdRicetta).
successoMedio(IdRicetta) :- raitingBasso(IdRicetta), difficoltaMoltoFacile(IdRicetta).
successoMedio(IdRicetta) :- raitingMedio(IdRicetta), difficoltaMedia(IdRicetta).
successoAlto(IdRicetta) :-  raitingAlto(IdRicetta), difficoltaMedia(IdRicetta).
successoAlto(IdRicetta) :-  raitingAlto(IdRicetta), difficoltaFacile(IdRicetta).
successoAlto(IdRicetta) :-  raitingMedio(IdRicetta), difficoltaFacile(IdRicetta).
successoAlto(IdRicetta) :-  raitingMedio(IdRicetta), difficoltaMoltoFacile(IdRicetta).
successoAlto(IdRicetta) :-  raitingAlto(IdRicetta), difficoltaMoltoFacile(IdRicetta).
numero_interazioni_alto(IdRicetta):- interazioni(IdRicetta, Numero_interazioni), Numero_interazioni > 20.
ricetta_salutare(IdRicetta):- vegana(IdRicetta,Valore_vegana),senzaGlutine(IdRicetta,Valore_glutine),senzaLattosio(IdRicetta,Valore_lattosio), 
    Valore_vegana == 1, Valore_glutine == 1, Valore_lattosio == 1.
ricetta_popolare(IdRicetta):- raitingAlto(IdRicetta), numero_interazioni_alto(IdRicetta).
ricetta_Universitari(IdRicetta):- cottura(IdRicetta, ValoreTempoCottura), preparazione(IdRicetta, ValoreTempoPreparazione), 
    ValoreTempoCottura =< 20, ValoreTempoPreparazione =< 20, ricetta_popolare(IdRicetta), difficoltaMoltoFacile(IdRicetta); difficoltaFacile(IdRicetta).