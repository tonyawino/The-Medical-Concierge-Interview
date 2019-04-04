import SimpleHTTPServer
import SocketServer
import csv
import os

from Character import Character
from Season import Season
from SeasonCharacter import SeasonCharacter

__author__ = 'Tony Awino'

if __name__ == '__main__':
    # Store all the characters in a list
    characters = []
    with open('characters.csv', 'rb') as user_file:
        spam_reader = csv.DictReader(user_file)
        for row in spam_reader:
            name = row.get('name')
            district = row.get('district')
            mother = row.get('mothers name')
            father = row.get('fathers name')
            registration = row.get('date registered')
            actor = Character(name, mother, father, district, registration)
            characters.append(actor)

    # Store a dictionary containing Season objects with key season number
    seasons = {}
    with open('episode_per_season.csv') as appearance_file:
        spam_reader = csv.DictReader(appearance_file)
        for row in spam_reader:
            season = Season(int(row.get('season')))
            seasons[int(row.get('season'))] = season

    # Store character information per season
    with open('episode_per_season.csv') as appearance_file:
        spam_reader = csv.DictReader(appearance_file)
        for row in spam_reader:
            user = row.get('user')
            episodes = row.get('no of episodes')
            died = row.get('died in this season')
            character = SeasonCharacter(user, episodes, died)
            seasons[int(row.get('season'))].characters()[user] = character

    html = "<!DOCTYPE html><html><head lang=\"en\"><meta charset=\"UTF-8\"><title>GOT Character Profile</title><style>" \
           "table, th, td {border: 1px solid black;}</style></head><body><h1>GOT Character " \
           "Profiles</h1><table><tr><th>Name</th><th>District</th><" \
           "th>Mother's Name</th><th>Father's Name</th><th>Date Added</th><th>Episodes Per Season</th><th>Died in Se" \
           "ason</th></tr>%s</table></body></html>"

    page_data = []
    for character in characters:
        character_episodes = []
        deathSeason = 0
        for season in seasons.values():
            seasonCharacter = season.characters().get(character.name(), None)
            if seasonCharacter is not None:
                if int(seasonCharacter.died()) == 1:
                    deathSeason = season.season()
                character_episodes.append("%s Episodes in Season %s" % (seasonCharacter.episodes(), season.season()))

        data = "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>Season %s</td></tr>" % \
               (character.name(), character.district(), character.mother(), character.father(),
                character.registrationDate(),
                '<br/><hr/>'.join(character_episodes), "None" if deathSeason == 0 else deathSeason)
        page_data.append(data)

    page = open('index.html', 'w')
    page.write(html % (''.join(page_data)))
    page.close()

    # Server
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", 8082), Handler)

    print "serving at port 8082"
    print "Press Ctrl+c twice to exit"
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        os.remove('index.html')
        raise KeyboardInterrupt()
