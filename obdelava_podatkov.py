import re
import orodja

vzorec_odseka = re.compile(
    r'<tr class="player_tr_(1|2)"'
    r'.*?'
    r'</tr>',
    re.DOTALL
    )

vzorec_igralca = re.compile(
        r'<a href="/19/player/(?P<id>\d+)/(?P<ime>\D*)?" class="player_name_players_table">(?P<vzdevek>\D*)?</a>.*?'
        r'&club=(?P<id_kluba>\d+)" data-original-title="(?P<klub>.*?)" data-toggle="tooltip".*?'
        r'nation=(?P<id_države>\d+)" data-original-title="(?P<država>\D+)?" data-toggle="tooltip".*?'
        r'&league=(?P<id_lige>\d+)" data-original-title="(?P<liga>.+)?" data-toggle="tooltip".*?'
        r'<td><span class="form rating ut19.*?">(?P<ocena>\d+)</span></td>.*?'
        r'<td class="">(?P<pozicija>\w+)</td>.*?'
        r'<td><span class="ps4_color font-weight-bold">(?P<cena>.*)? <img alt="c" class="small-coins-icon".*?'
        r'<td>(?P<spretnost>\d)<i style="font-size: 10px;" class="icon-star-full stars-"></i></td>.*?'
        r'<td>(?P<šibka_noga>\d)<i style="font-size: 10px;" class="icon-star-full stars"></i></td>.*?'
        r'<td><span class="badge .*? p-2 font-weight-normal">(?P<hitrost>\d+)</span></td>.*?'
        r'<td><span class="badge .*? p-2 font-weight-normal">(?P<strel>\d+)</span></td>.*?'
        r'<td><span class="badge .*? p-2 font-weight-normal">(?P<podaje>\d+)</span></td>.*?'
        r'<td><span class="badge .*? p-2 font-weight-normal">(?P<dribling>\d+)</span></td>.*?'
        r'<td><span class="badge .*? p-2 font-weight-normal">(?P<obramba>\d+)</span></td>.*?'
        r'<td><span class="badge .*? p-2 font-weight-normal">(?P<fizičnost>\d+)</span></td>.*?'
        r'<td>(?P<višina>\d+)cm.*?'
        r'<td class="mobile-hide-table-col">(?P<popularnost>.*?)</td>',
        re.DOTALL
    )
imena_polj = [
    'id', 'ime', 'vzdevek', 'id_kluba', 'klub', 'id_države', 'država', 'id_lige',
    'liga', 'ocena', 'pozicija', 'cena', 'spretnost', 'šibka_noga', 'hitrost', 'strel',
    'podaje', 'dribling', 'obramba', 'fizičnost', 'višina', 'popularnost'
    ]

def obdelava_spletne_strani(st_strani):
    url = ('https://www.futbin.com/19/players'
    '?page={}'
    '&position=CB,LB,LWB,RB,RWB,CDM,CM,CAM,CF,ST,LM,LW,LF,RM,RW,RF&version=all_nif'
    ).format(st_strani)
    ime_datoteke = 'igralci-Fife19-{}.html'.format(str(st_strani))
    orodja.shrani_spletno_stran(url, ime_datoteke)
    vsebina = orodja.vsebina_datoteke(ime_datoteke, orodja.IMENIK_HTML)
    odseki_igralcev = orodja.razdeli_stran_na_igralce(ime_datoteke, vzorec_odseka)
    for igralec in odseki_igralcev:
        yield obdelaj_igralca(igralec)

def razberi_ceno(niz):
    niz = niz.strip()
    try:
        cena = int(niz)
    except ValueError:
        if niz[-1] == 'M':
            cena = 10**6 * float(niz[:-1])
        else:
            cena = 10**3 * float(niz[:-1])
    return int(cena)


def obdelaj_igralca(odsek):
    '''Vsakega igralca posebej obdela, počisti vse nepotrebne napake, ki se zgodijo, ko 
    program izbira golo besedilo s html kode in vrne iskane podatke v obliki slovarja'''
    igralec = vzorec_igralca.search(odsek).groupdict()
    st_atributi = ['id', 'id_kluba', 'id_države', 'id_lige', 'ocena',
    'spretnost', 'šibka_noga', 'hitrost', 'strel', 'podaje', 'dribling',
    'obramba', 'fizičnost', 'višina', 'popularnost']
    for vzorec in st_atributi:
        igralec[vzorec] = int(igralec[vzorec]) 
    if igralec['ime'] == igralec['vzdevek']:    # Preverim ali je igralčev vzdevek enak polnemu imenu
        igralec['vzdevek'] = None
    igralec['cena'] = razberi_ceno(igralec['cena'])
    return igralec

igralci = []
for i in range(1, 101):
    for igralec in obdelava_spletne_strani(i):
        igralci.append(igralec)
igralci.sort(key=lambda igralec: igralec['id'])

orodja.zapisi_json(igralci, 'igralci.json')
orodja.zapisi_csv(igralci, imena_polj, 'igralci.csv')
