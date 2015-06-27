import httplib2
h = httplib2.Http()
headers = {'content-type': 'application/x-www-form-urlencoded'}
params = 'ids=chr16:g.28883241A>G,chr1:g.35367G>A&fields=dbnsfp.genename,cadd.gene'
res, con = h.request('http://myvariant.info/v1/variant', 'POST', params, headers=headers)
print res, con