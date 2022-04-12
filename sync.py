# from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount
import configparser

config = configparser.ConfigParser()
config.read("secrets/plex.ini")
inifile = config['Default']
token = inifile["token"]
libs = inifile["libs"]
fromServers = inifile["fromServers"]
toServers = inifile["toServers"]

plex = MyPlexAccount(token)


def get_watched(server, library):
    watched_episodes = []

    shows = server.library.section(library)
    for show in shows.search(unwatched=False):
        # print(show)
        for episode in show.watched():
            watched_episodes.append(episode)

    return watched_episodes


def mark_watched(server, watched, library):
    for episode in watched:
        try:
            show = server.library.section(library).get(episode.grandparentTitle)
            ep = show.episode(season=int(episode.parentIndex), 
                              episode=int(episode.index))

            print('{} - {} - marked as watched.'.format(ep.grandparentTitle, 
                                                        ep.title))

            ep.markWatched()
        except KeyboardInterrupt:
            break
        except Exception:
            print('{} - {} - NOT FOUND!.'.format(episode.grandparentTitle, 
                                                 episode.title))


for fs in fromServers:
    fromServer = plex.resource(fs).connect()
    
    for ts in toServers:
        print('Syncing from {} to {}'.format(fs, ts))
        toServer = plex.resource(ts).connect()
        
        for lib in libs:
            watched = get_watched(fromServer, lib)
            mark_watched(toServer, watched, lib)
