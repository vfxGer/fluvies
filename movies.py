import string
import urllib.parse
import logging 

import secrets

import requests

import google_spreadsheet

def get_movie_list():
    return google_spreadsheet.get_movie_list()

def is_on_netflix(movie_name):
    movie_name = movie_name.strip()
    if ord(movie_name[-1]) ==10060:
        return False
    elif ord(movie_name[-1]) ==9989:
        return True
    return None

def main():
    lines = get_movie_list()
    print("Number,Film Name,On Netflix,IMDB,IDMB Score,Year,Duration in minutes")
    i = 1
    for movie in lines:
        print(i, end=',')
        i+=1
        if "," in movie:
            print('"%s"' % movie, end=',')
        else:
            print(movie, end=',')
        on_netflix = is_on_netflix(movie)
        if on_netflix is None:
            print(" ", end=',')
        elif on_netflix:
            print("yes", end=',')
        else:
            print("no", end=',')

        clean_name = ""
        for c in movie:
            if c in string.printable:
                clean_name += c
        clean_name = clean_name.strip()
        logging.debug(clean_name)
        clean_name = urllib.parse.quote_plus(clean_name)
        # # movies.append(clean_name)
        r = requests.get("http://www.omdbapi.com/?apikey=%s&t=%s&type=movie"%(
                        secrets.api_key, 
                        clean_name)).json()
        try:
            id_ = r['imdbID']
        except KeyError:
                 raise Exception("Title %s not found" % clean_name)
        print("https://www.imdb.com/title/" + r['imdbID'], end=",")
        for d in r['Ratings']:
            if d['Source']=='Internet Movie Database':
                print(d['Value'].strip("/10"), end=",")
                break
        else:
            raise Exception("IMDB rating not found in: %s "% r)

        print(r['Year'], end=",")
        print(r['Runtime'].strip(" min"), end=",")
        print("")
if __name__=="__main__":
    main()


