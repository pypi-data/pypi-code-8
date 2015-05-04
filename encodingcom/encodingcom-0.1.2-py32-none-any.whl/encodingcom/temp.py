
destination = 'http://AKIAJEZZPJ5J5HXKD2NQ:XaSNfd7ncFD3qwMmAfoIALSAeLiXVld3TRFoWzfu@snwatsonencodingdropbox.s3.amazonaws.com/rzpj88evbor79o-output-web_720.mp4?canonical_id=165842c94f82c97c1c57e365360fa6e8c282062dab4d45b2ce00012b93eb5343&acl=public-read'


output_index = destination.find('.mp4')
thumbnail_url = destination[0:output_index]
thumbnail_url += '.jpg'
thumbnail_url += destination[output_index + len('.mp4'):]

print(thumbnail_url)