import os
import sys
import requests
import re

IMENIK_HTML = 'spletne_strani'
IMENIK_PODATKOV = 'podatki'

def nova_datoteka(ime_datoteke, imenik=''):
    '''Preveri ali imenik že obstaja ter ga, če je to potrebno ustvari in vrne direktno pot do datoteke z danim imenom'''
    trenutno_mesto = os.getcwd()
    if imenik:
        os.makedirs(imenik, exist_ok=True)
    direktna_pot = os.path.join(trenutno_mesto, imenik, ime_datoteke)
    return direktna_pot

def shrani_spletno_stran(url, ime_datoteke, imenik):    # imenik je dodan zaradi preglednosti datotek v mapi
    '''Vsebino spletne strani z danega url-ja shrani v datoteko -v imeniku- z danim imenom'''
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


for i in range(1, 101):
    url = ('https://www.futbin.com/19/players'
    '?page={}'
    '&position=CB,LB,LWB,RB,RWB,CDM,CM,CAM,CF,ST,LM,LW,LF,RM,RW,RF&version=all_nif'
    ).format(i)
    ime_datoteke = 'igralci-Fife19-{}.html'.format(i)
    shrani_spletno_stran(url, ime_datoteke, IMENIK_HTML)

def razdeli_stran_na_igralce(ime_datoteke):
    '''S html datoteke razbere odsek podatkov za vsakega igralca posebaj ter vrne seznam odsekov za posamezne igralce'''
    vzorec = re.compile(
        r'<tr class="player_tr_(1|2)"'
        r'.*?'
        r'</tr>',
        re.DOTALL
    )
    odseki = []
    vsebina = vsebina_datoteke(ime_datoteke, IMENIK_HTML)
    for ujemanje in vzorec.finditer(vsebina):
        odseki.append(ujemanje.group(0))
    return odseki

def obdelaj_igralca(odsek):
    '''Vsakega igralca posebej obdela in vrne iskane podatke v obliki slovarja'''
    podatki_igralca = []
    vzorec = re.compile(
        r'<tr class="player_tr_(1|2)" data-url="/19/player/(?P<id>\d+)/.*?'
        r'<a href="/19/player/\d+/(?P<ime>\D*)?" class="player_name_players_table">(?P<vzdevek>\D*)?</a>',
        re.DOTALL
    )
    def pocisti_podatke(vsebina):
        podatki_igralca = vsebina.groupdict()
        podatki_igralca['id'] = int(podatki_igralca['id'])
        return podatki_igralca
    for ujemanje in vzorec.finditer(odsek):
        print(ujemanje)
        podatki_igralca.append(pocisti_podatke(ujemanje))
    return podatki_igralca

podatki = razdeli_stran_na_igralce('igralci-Fife19-1.html')

print(podatki[0])
print(podatki[-1])
print(len(podatki))
print(obdelaj_igralca(podatki[0]))
