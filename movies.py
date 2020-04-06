import string
import urllib.parse
import requests

import secrets

def get_movie_list():
    with open("movie_list.txt") as fp:
        raw_string = fp.read()
    res = raw_string.split("\n")
    res = [i for i in res if i]
    return res

def main():
    lines = get_movie_list()
    for movie in lines:
        clean_name = ""
        for c in movie:
            if c in string.printable:
                clean_name += c
        clean_name = clean_name.strip()
        # print(clean_name)
        clean_name = urllib.parse.quote_plus(clean_name)
        # movies.append(clean_name)
        r= requests.get("http://www.omdbapi.com/?apikey=%s&t=%s&type=movie"%(
            secrets.api_key, 
            clean_name)).json()
        if True:
            try:
                id_ = r['imdbID']
            except KeyError:
                raise Exception("Title %s not found" % clean_name)
            print("https://www.imdb.com/title/" + r['imdbID'])
        else:
            # print(r['Year'])
            found = False
            for d in r['Ratings']:
                if d['Source']=='Internet Movie Database':
                    print(d['Value'].strip("/10"))
                    found = True
            if not found:
                raise Exception(r)

if __name__=="__main__":
    main()


