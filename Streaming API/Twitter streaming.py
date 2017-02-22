import tweepy

#stocker les accès API dans des variables
consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''

#Importer OAuthHandler. OAuthHandler est un module de Tweepy qui permet de gérer les accès
from tweepy import OAuthHandler

# Créer une instance de OAuthHandler qui prend consumer_key, consumer_secret en paramètre
auth = OAuthHandler(consumer_key, consumer_secret)

#Définir les access token via les variables créées précédemment
auth.set_access_token(access_token, access_secret)

#Créer une instance de API qui crée la connexion avec l'API
api = tweepy.API(auth)

#Importer l'API Streaming de Twitter
from tweepy import Stream
#StreamListener va écrire mon stream
from tweepy.streaming import StreamListener
#Importer json pour manipuler les data
import json

#Une classe qui permet de filtrer les données en entrée et d'écrire les erreurs potentielles
class MyListener(StreamListener):
    def on_data(self, data):
        try:
            #convertir les str en dict
            data = json.loads(data)
            #Afficher les tweets si ils correspondent à l'auteur voulu 
            if data['user']["screen_name"] == "nom_de_l'auteur":
                    print(data)
        #Si il y a une erreur : l'afficher
        except BaseException as e:
            print(str(e))
        return True

    def on_error(self, status):
        print(status)
        return True
        
#Créer une instance de Stream avec pour paramètres mes credentials et ma classe
twitter_stream = Stream(auth, MyListener())
#Filtrer les tweets qui ne viennent que de l'id déterminé 
twitter_stream.filter(follow=["id_float"])
