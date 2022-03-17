from plexapi.server import PlexServer
from plexapi.myplex import MyPlexAccount

token = '' # Put your plex token here

libs = ['TV Shows'] # a List of the libraries to sync, they must be named the same on all servers
fromServers = ['', ''] # a List of the names of the "from" servers
toServers = [''] # a List of the names of the "to" servers

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
            ep = show.episode(season=int(episode.parentIndex), episode=int(episode.index))

            print('{} - {} - marked as watched.'.format(ep.grandparentTitle, ep.title))

            ep.markWatched()
        except KeyboardInterrupt:
            break
        except:
            print('{} - {} - NOT FOUND!.'.format(ep.grandparentTitle, ep.title))

for fs in fromServers:
    fromServer = plex.resource(fs).connect()
    
    for ts in toServers:
        print('Syncing from {} to {}'.format(fs, ts))
        toServer = plex.resource(ts).connect()
        
        for lib in libs:
            watched = get_watched(fromServer, lib)
            mark_watched(toServer, watched, lib)