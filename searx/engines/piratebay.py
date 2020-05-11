#  Piratebay (Videos, Music, Files)
#
# @website     https://thepiratebay.se
# @provide-api no (nothing found)
#
# @using-api   no
# @results     HTML (using search portal)
# @stable      yes (HTML can change)
# @parse       url, title, content, seed, leech, magnetlink

from lxml import html
from operator import itemgetter
from searx.engines.xpath import extract_text
from searx.url_utils import quote, urljoin
import json
import datetime

# engine dependent config
categories = ['videos', 'music', 'files']
paging = True

# search-url
siteurl = 'https://thepiratebay.org/'
url = 'https://apibay.org/'
search_url = url + 'q.php?q='

#piratebay specific type-definitions
tpb_categories = { "101" :	'Music',
               "102" : 'Audio books',
               "103" : 'Sound clips',
               "104" : 'FLAC',
               "199" : 'Other',
               "201" : 'Movies',
               "202" : 'Movies DVDR',
               "203" : 'Music videos',
               "204" : 'Movie clips',
               "205" : 'TV shows',
               "206" : 'Handheld',
               "207" : 'HD - Movies',
               "208" : 'HD - TV shows',
               "209" : '3D',
               "299" : 'Other',
               "301" : 'Windows',
               "302" : 'Mac',
               "303" : 'UNIX',
               "304" : 'Handheld',
               "305" : 'IOS (iPad/iPhone)',
               "306" : 'Android',
               "399" : 'Other OS',
               "401" : 'PC',
               "402" : 'Mac',
               "403" : 'PSx',
               "404" : 'XBOX360',
               "405" : 'Wii',
               "406" : 'Handheld',
               "407" : 'IOS (iPad/iPhone)',
               "408" : 'Android',
               "499" : 'Other',
               "501" : 'Movies',
               "502" : 'Movies DVDR',
               "503" : 'Pictures',
               "504" : 'Games',
               "505" : 'HD - Movies',
               "506" : 'Movie clips',
               "599" : 'Other',
               "601" : 'E-books',
               "602" : 'Comics',
               "603" : 'Pictures',
               "604" : 'Covers',
               "605" : 'Physibles',
               "699" : 'Other' }

# do search-request
def request(query, params):

    url = search_url + query
    params['url'] = url
    logf=open("/tmp/searx.log","w")
    logf.write(url + "\n")
    logf.close()

    return params


# get response from search-request
def response(resp):

    torrents = json.loads(resp.text)

    results = []

    # parse results
    for torrent in torrents:

        link = torrent['name']
        href = 'https://thepiratebay.org/description.php?id=' + torrent['id']
        title = torrent['name']
        timestamp = float(torrent['added'])
        seed = torrent['seeders']
        leech = torrent['leechers']
        size = float(torrent['size'])
        category = torrent['category']
        content = 'Contains ' + torrent['num_files'] + ' file(s), uploaded ' + str(datetime.datetime.fromtimestamp(timestamp)) + ' by: ' + torrent['username'] + ' (' + torrent['status'] + ') in category : "' + tpb_categories.get(category) + '"'

        # convert seed to int if possible
        if seed.isdigit():
            seed = int(seed)
        else:
            seed = 0

        # convert leech to int if possible
        if leech.isdigit():
            leech = int(leech)
        else:
            leech = 0

        magnetlink = 'magnet:?xt=urn:btih:' + torrent['info_hash'] + '&dn=' + torrent['name'] + '&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2920%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=udp%3A%2F%2Ftracker.internetwarriors.net%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.leechers-paradise.org%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.pirateparty.gr%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.cyberia.is%3A6969%2Fannounce'

        torrentfile_link = None

        # append result
        results.append({'url': href,
                        'title': title,
                        'content': content,
                        'seed': seed,
                        'leech': leech,
                        'magnetlink': magnetlink,
                        'torrentfile': torrentfile_link,
                        'filesize': size,
                        'template': 'torrent.html'})

    # return empty array if nothing is found
    if not results:
        return []

    # return results sorted by seeder
    return sorted(results, key=itemgetter('seed'), reverse=True)
