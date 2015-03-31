# -*- coding: utf-8 -*-

from __future__ import print_function

import os, sys, shutil
import logging
from urllib import unquote

from metapub import PubMedFetcher, CrossRef 
from metapub.exceptions import MetaPubError
from metapub.utils import asciify

#from tabulate import tabulate

####
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("eutils").setLevel(logging.INFO)
####

fetch = PubMedFetcher()

def print_table(res_table, headers):
    print('\t'.join(headers))
    for x in range(0, len(res_table['score'])):
        print('\t'.join(['{}'.format(res_table[h][x]) for h in headers]))

if __name__=='__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        print('Supply filename of pmid list as the argument to this script.')
        sys.exit()
    
    pmids = open(filename, 'r').readlines()

    results_table = { 'pmid': [], 'pma_title': [], 'cr_title': [], 'doi': [], 'score': [], 'pma_aulast': [], 'cr_aulast': [], 'pma_journal': [], 'cr_journal': [] } 

    CR = CrossRef()

    for pmid in pmids:
        pmid = pmid.strip()
        if pmid:
            results_table['pmid'].append(pmid)
            try:
                pma = fetch.article_by_pmid(pmid)
            except:
                pma = None
                #print("%s: Could not fetch" % pmid)
        if pma:
            results = CR.query_from_PubMedArticle(pma)
            top_result = CR.get_top_result(results, CR.last_params, use_best_guess=True)
                
            results_table['pma_title'].append(asciify(pma.title))
            results_table['pma_journal'].append(asciify(pma.journal))
            results_table['cr_title'].append(asciify(top_result['title']))
            results_table['doi'].append(top_result['doi'])
            results_table['score'].append(top_result['score'])

            if top_result['slugs'] != {}:
                try:
                    results_table['cr_aulast'].append(asciify(top_result['slugs']['aulast']))
                except:
                    results_table['cr_aulast'].append('NA')
                    
                results_table['cr_journal'].append(asciify(top_result['slugs']['jtitle']))
            else:
                results_table['cr_aulast'].append('')            
                results_table['cr_journal'].append('')

            #print(unquote(top_result['coins'])) #.decode('utf8'))

            results_table['pma_aulast'].append(asciify(pma.author1_last_fm))
        else:
            results = None
            top_result = None
            results_table['pma_aulast'].append('NA')
            results_table['pma_journal'].append('NA')
            results_table['pma_title'].append('NA')
            results_table['doi'].append('NA')
            results_table['score'].append('NA')
            results_table['cr_journal'].append('NA')
            results_table['cr_aulast'].append('NA')
            results_table['cr_title'].append('NA')

        #print(pmid, top_result['doi'], top_result['score'], sep='\t')

    headers = ['score', 'pmid', 'doi', 'pma_aulast', 'cr_aulast', 'pma_journal', 'cr_journal', 'pma_title', 'cr_title']

    print_table(results_table, headers)


# crossref return looks like:
"""{
        doi: "http://dx.doi.org/10.2307/40250596",
        score: 2.0651011,
        normalizedScore: 74,
        title: "Research and Relevant Knowledge: American Research Universities since World War II",
        fullCitation: "Winton U. Solberg, Roger L. Geiger, 1994, 'Research and Relevant Knowledge: American Research Universities since World War II', <i>Academe</i>, vol. 80, no. 1, p. 56",
        coins: "ctx_ver=Z39.88-2004&amp;rft_id=info%3Adoi%2Fhttp%3A%2F%2Fdx.doi.org%2F10.2307%2F40250596&amp;rfr_id=info%3Asid%2Fcrossref.org%3Asearch&amp;rft.atitle=Research+and+Relevant+Knowledge%3A+American+Research+Universities+since+World+War+II&amp;rft.jtitle=Academe&amp;rft.date=1994&amp;rft.volume=80&amp;rft.issue=1&amp;rft.spage=56&amp;rft.aufirst=Winton+U.&amp;rft.aulast=Solberg&amp;rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Ajournal&amp;rft.genre=article&amp;rft.au=Winton+U.+Solberg&amp;rft.au=+Roger+L.+Geiger",
        year: "1994"
        },"""

