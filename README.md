# Analiza nogometnih igralcev igre Fifa 19 -- FUTBIN


Analiziral bom prvih 3000 nogometnih igralcev, igre **Fifa 19**, glede na njihovo oceno na strani
[FUTBIN](https://www.futbin.com/19/players?page=1&position=CB,LB,LWB,RB,RWB,CDM,CM,CAM,CF,ST,LM,LW,LF,RM,RW,RF&version=all_nif).


Za vsakega igralca bom zajel:
* njegovo ime, klub, ligo in državljanstvo
* pozicijo igranja
* vrednost na trgu
* njegovo povprečno oceno in oceno hitrosti, strela, podaj, driblanja, obrambe in fizične pripravljenosti
* oceno tehnične sposobnosti in udarca z šibkejšo nogo
* višino
* popularnost pri igralcih igre

Delovne hipoteze:
* Ali katera izmed ocen drastično poveča igralčevo ceno na trgu?
* Kako je odvisna velikost igralca od položaja na igrišču?
* Ali so povprečne ocene sorazmerne z ostalimi ocenami ali na to vpliva še kaj drugega?
* Ali imata ocena tehnične sposobnosti in udarca z šibkejšo nogo sploh kakšen vpliv na ceno oziroma oceno?
* Ali bi lahko glede na ocene igralca ocenili položaj na katerem igra?
* Kako klub, liga in državljanstvo vplivajo na igralčevo ceno?

## Zajem podatkov

V imeniku `spletne_strani` so shranjene html datoteke analiziranih spletnih strani, navedenih zgoraj. V upoštev je prišlo prvih 100 strani, da sem dosegel začetno predpostavko 3000 igralcev.
Tako sem z omenjenih datotek, s pomočjo pythonove knjižnice `re`, za vsakega igralca razbral zgoraj navedene atribute. Te podatke sem na koncu shranil v imenik `podatki`, v datoteke `igralci.json` in `*.csv`. V slednji sem zaradi preglednosti ločil od igralcev (`igralci.csv`) vse atribute, ki se jih da razbrati samo iz stolpca _id_kluba_, ki je eden izmed atributov in jih shranil v `klubi.csv`.

**OPOMBA:** iz analize so izvzeti igralci na položaju _golmana_, ker njihove ocene niso skladne z ostalimi. 
