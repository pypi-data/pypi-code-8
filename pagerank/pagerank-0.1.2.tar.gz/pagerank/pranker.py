import re
from urlparse import urlparse

def get_page_rank(target_domain, keywords, num_considered_entries=100, tld='com.tr', lang='tr'):
    """
    @param tld: str, tld to use in google.tld
    @param lang: str, langguage of the query
    @return prank: int, nullable
    """
    from lib.xgoogle.search import GoogleSearch
    if type(keywords) == unicode:
        keywords = keywords.encode('utf-8')
    if type(target_domain) == unicode:
        target_domain = target_domain.encode('utf-8')
    target_domain = target_domain.lower()
    gs = GoogleSearch(keywords, tld=tld, lang=lang, random_agent=True)
    gs.results_per_page = 50
    idx = 0

    prev_domain = None
    while idx < num_considered_entries:
        results = gs.get_results()
        for res in results:
            parsed = urlparse(res.url)
            domain = mk_nice_domain(parsed.netloc)
            if prev_domain == domain:
                continue
            prev_domain = domain
            idx = idx + 1
            if target_domain in domain:
                print "Ranking position %d for keyword %s on domain %s" % (idx, keywords, target_domain)
                return idx
    print "no entries found for %s keyword %s" % (target_domain, keywords)
    return None

def mk_nice_domain(domain):
    """
    convert domain into a nicer one (eg. www3.google.com into google.com)
    """
    domain = re.sub("^www(\d+)?\.", "", domain)
    # add more here
    return domain

def test(domain, keyword, tld, lang):
    """
    @param tld: str, tld to use in google.tld
    @param lan: str, language of the query
    """
    get_page_rank(domain, keyword, tld=tld, lang=lang)

def main():
    define("lang", help='tr for turkish')
    define("tld", help='com.tr for turkish', default='com')
    define("domain", default='istanbella.com')
    define("keyword", default='istanbella')

    parse_command_line()
    basicConfig(options=options)

    test(options.domain, options.keyword, options.tld, options.lang)

if __name__ == "__main__":
    from utensils.options import define, options, parse_command_line
    from utensils.loggingutils import basicConfig
    main()

