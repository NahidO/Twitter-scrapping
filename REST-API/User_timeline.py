import tweepy #https://github.com/tweepy/tweepy

#Identifiants Twitter API. Plus d'infos : https://dev.twitter.com/oauth/overview
consumer_key = ''#keep the quotes, replace this with your consumer key
consumer_secret = ''#keep the quotes, replace this with your consumer secret key
access_key = ''#keep the quotes, replace this with your access token
access_secret = ''#keep the quotes, replace this with your access token secret

#S'authentifier à Twitter et initialiser Tweepy par un object de type OAuthHandler.

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

#Tous mes tweets seront contenus dans une liste
alltweets = []

#User_timeline permet de collecter les 3240 derniers tweets de l'utilisateur passé entre parenthèses - par paquets de 200 tweets
new_tweets = api.user_timeline(screen_name = "@screen_name",count=200)

#Pour ajouter les paquets de 200, j'utiliser la fonction liste.extend
alltweets.extend(new_tweets)

#Enregistrer le plus vieil identifiant unique possible pour empêcher les doublons (optionnel)
oldest = alltweets[-1].id - 1

#Boucle pour ajouter mes new_tweets à all_tweets
while len(new_tweets) > 0:
	
	#max_id est l'ID du dernier tweet 
	new_tweets = api.user_timeline(screen_name = "@screen_name",count=200,max_id=oldest)
	
	#Ajouter news_tweets à all_tweets
	alltweets.extend(new_tweets)
	
	#mettre à jour l'ID du tweet
	oldest = alltweets[-1].id - 1
	
  #Vérifier que les tweets sont bien collectés
	print (len(alltweets), "tweets downloaded so far") 

#Conserver la date et le texte brut dans un array
outtweets = [[tweet.created_at, tweet.text] for tweet in alltweets]

#Manipuler les tweets avec Pandas
outtweets_df = pd.DataFrame(outtweets)

#Convertir la date au format datetime
import datetime as dt
outtweets_df[0] = pd.to_datetime(outtweets_df[0])

#Convertir la date au format EPOCH pour UNIX (1/1/1970) en millisecondes
outtweets_df[0] = (outtweets_df[0] - dt.datetime(1970,1,1)).dt.total_seconds()

#Renommer les colonnes 
outtweets_df = outtweets_df.rename(columns = {0 : "timestamp_millis", 1 : "text"})

#Si mon tweet n'a pas de date associée, virer la ligne en question
outtweets_df = outtweets_df[outtweets_df["timestamp_millis"].notnull()]

#Exporter au format csv pour exploitation
#Le line_terminator "\r\n" permet d'éviter que les tweets avec des sauts de ligne soient considérés comme un nouvel enregistrement
outtweets_df.to_csv(path_or_buf = "/Users/noulmi/Downloads/outtweets.csv", sep = ";", line_terminator = "\r\n", encoding = "utf-8", index = False)
