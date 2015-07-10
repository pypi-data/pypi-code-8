# koningrijk/wet.py
#
#

""" puntje, puntje, puntje. """

## IMPORTS

from kern.clock import Repeater
from kern import kernel

import random

## CMNDS

def grond(*args, **kwargs): kernel.announce(grond_txt)

kernel.register("grond", grond)

def beleid(*args, **kwargs): kernel.announce(beleid_txt)

kernel.register("beleid", beleid)

def criteria(*args, **kwargs): kernel.announce(criteria_txt)

kernel.register("criteria", criteria)

def geest(*args, **kwargs): kernel.announce(geest_txt)

kernel.register("geest", geest)

def machtiging(*args, **kwargs): kernel.announce(machtiging_txt)

kernel.register("machtiging", machtiging)

## INIT

def init():
    todo = Repeater(criteria, 600)
    kernel.put(todo.start)

## TXT

grond_txt = """
Artikel 3:1

Verplichte zorg is zorg die ondanks verzet als bedoeld in artikel 1:4 kan worden verleend
op grond van:

 a. een zorgmachtiging;
 b. een crisismaatregel;
 c. een beslissing tot tijdelijke verplichte zorg voorafgaand aan een crisismaatregel als bedoeld in artikel 7:4;
 d. een beslissing tot tijdelijke verplichte zorg in een noodsituatie als bedoeld in de artikelen 8:11 en 8:12.
"""

beleid_txt = """
Artikel 3:2

Zorg kan bestaan uit:

 a. een interventie, bestaande uit een vorm van verzorging, bejegening, behandeling, begeleiding of bescherming;
 b. toediening van medicatie, vocht en voeding, regelmatige medische controle of andere medische handelingen;
 c. pedagogische of therapeutische maatregelen;
 d. opname in een accommodatie;
 e. beperking van de bewegingsvrijheid;
 f. afzondering of separatie in een daartoe geschikte verblijfsruimte;
 g. beperking van het recht op het ontvangen van bezoek of het gebruik van communicatiemiddelen;
 h. toezicht op betrokkene;
 i. onderzoek aan kleding of lichaam;
 j. controle op de aanwezigheid van gedrag beïnvloedende middelen;
 k. beperkingen in de vrijheid het eigen leven in te richten, die tot gevolg hebben dat betrokkene iets moet doen of nalaten.
"""

criteria_txt = """
Artikel 3:3

Indien het gedrag van een persoon als gevolg van zijn psychische stoornis leidt tot een
aanzienlijk risico op ernstige schade voor hemzelf of voor een ander kan als uiterste middel
verplichte zorg worden verleend, indien:

 a. er geen mogelijkheden voor zorg op basis van vrijwilligheid zijn;
 b. er voor betrokkene geen minder bezwarende alternatieven met het beoogde effect zijn;
 c. het verlenen van verplichte zorg, gelet op het beoogde doel van verplichte zorg evenredig is; en
 d. redelijkerwijs te verwachten is dat het verlenen van verplichte zorg effectief is.
"""

geest_txt = """
Artikel 3:4

1. Verplichte zorg kan worden verleend om:

 a. een crisissituatie af te wenden;
 b. een aanzienlijk risico op ernstige schade af te wenden;
 c. een zorgplan op te stellen;
 d. de geestelijke gezondheid van betrokkene te stabiliseren;
 e. de geestelijke gezondheid van betrokkene dusdanig te herstellen dat hij zijn autonomie
    zo veel mogelijk herwint.

2. Indien het gedrag van een persoon als gevolg van zijn psychische stoornis leidt tot een
aanzienlijk risico op ernstige schade voor zijn fysieke gezondheid, kan ook verplichte zorg
worden verleend om zijn fysieke gezondheid te stabiliseren of te herstellen.
"""

machtiging_txt = """
Artikel 6:3

1. De rechter verleent een zorgmachtiging, indien naar zijn oordeel:

 a. aan de criteria voor verplichte zorg is voldaan, en
 b. met de in het zorgplan opgenomen verplichte zorg of indien een zorgplan ontbreekt,
    met de in de medische verklaring opgenomen verplichte zorg het aanzienlijke risico op
    ernstige schade kan worden weggenomen.

2. De zorgmachtiging vermeldt in elk geval:

 a. de zorg die noodzakelijk is om het aanzienlijke risico op ernstige schade weg te nemen;
 b. de wijze waarop rekening wordt gehouden met de voorkeuren van betrokkene, zoals
    vastgelegd op de zorgkaart of in de zelfbindingsverklaring;
 c. de minimale en maximale duur van de afzonderlijke vormen van verplichte zorg;
 d. de wijze waarop de zorgaanbieder en de geneesheer-directeur de kwaliteit van de
    verplichte zorg bewaken en toezicht houden op de uitvoering van verplichte zorg in
    ambulante omstandigheden;
 e. de frequentie waarmee en de omstandigheden waaronder het zorgplan en de
    subsidiariteit, proportionaliteit, effectiviteit en veiligheid van de verplichte zorg met
    betrokkene en de vertegenwoordiger zal worden geëvalueerd en het zorgplan geactualiseerd;
 f. de zorgaanbieder die wordt belast met de uitvoering van de zorgmachtiging en zo nodig de accommodatie;
 g. de inventarisatie van de essentiële voorwaarden voor maatschappelijke deelname;
 h. de mogelijkheid tot het verlenen van advies en bijstand door een patiëntenvertrouwenspersoon.


3. Indien de rechter van oordeel is dat aan de criteria voor verplichte zorg is voldaan, maar
   de in het zorgplan of de medische verklaring opgenomen zorg het aanzienlijk risico op
   ernstige schade niet kan worden weggenomen, kan hij in de zorgmachtiging in afwijking van 
   het zorgplan andere verplichte zorg of doelen van verplichte zorg in de zorgmachtiging
   opnemen, alsmede in de zorgmachtiging bepalen dat een ander zorgplan moet worden
   opgesteld.

4. De zorgmachtiging is bij voorraad uitvoerbaar.

5. De griffie van de rechtbank zendt een afschrift van de beslissing van de rechter aan:

 a. betrokkene;
 b. de vertegenwoordiger;
 c. de advocaat;
 d. de contactpersoon;
 e. de ouders die het gezag uitoefenen, de voogd, de curator of de mentor;
 f. de echtgenoot, partner, levensgezel of degene die betrokkene verzorgt;
 g. de aanvrager, bedoeld in artikel 5:1;
 h. de zorgaanbieder, de geneesheer-directeur, de zorgverantwoordelijke en de huisarts;
 i. de officier van justitie.
"""
