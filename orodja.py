import os
import sys
import requests
import json
import csv

IMENIK_HTML = 'spletne_strani'
IMENIK_PODATKOV = 'podatki'

def nova_datoteka(ime_datoteke, imenik=''):
    '''Preveri ali imenik že obstaja ter ga, če je to potrebno ustvari in vrne direktno pot do datoteke z danim imenom'''
    trenutno_mesto = os.getcwd()
    if imenik:
        os.makedirs(imenik, exist_ok=True)
    direktna_pot = os.path.join(trenutno_mesto, imenik, ime_datoteke)
    return direktna_pot

def shrani_spletno_stran(url, ime_datoteke, imenik=IMENIK_HTML):    # imenik je dodan zaradi preglednosti datotek v mapi
    '''Vsebino spletne strani z danega url-ja shrani v datoteko --v imeniku-- z danim imenom'''
    try:
        print('Shranjujem {} ...'.format(url), end='')
        sys.stdout.flush()
        pot_datoteke = nova_datoteka(ime_datoteke, imenik)
        if os.path.isfile(pot_datoteke):
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        with open(pot_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')

def vsebina_datoteke(ime_datoteke, imenik=''):
    pot = os.path.join(os.getcwd(), imenik, ime_datoteke)
    with open(pot, encoding='utf-8') as datoteka:
        return datoteka.read()

def razdeli_stran_na_igralce(ime_datoteke, vzorec):
    '''S html datoteke razbere odsek podatkov za vsakega igralca posebej ter vrne seznam odsekov za posamezne igralce'''
    odseki = []
    vsebina = vsebina_datoteke(ime_datoteke, IMENIK_HTML)
    for ujemanje in vzorec.finditer(vsebina):
        odseki.append(ujemanje.group(0))
    return odseki

def zapisi_json(odsek, ime_datoteke):
    '''Iz danega odseka ustvari JSON datoteko.'''
    direktna_pot = nova_datoteka(ime_datoteke, IMENIK_PODATKOV)
    with open(direktna_pot, 'w', encoding='utf-8') as json_datoteka:
        json.dump(odsek, json_datoteka, indent=4, ensure_ascii=False)

def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    direktna_pot = nova_datoteka(ime_datoteke, IMENIK_PODATKOV)
    with open(direktna_pot, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)