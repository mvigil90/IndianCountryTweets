import csv
import sys
import json
import geopy
import geopy.distance
import math
import datetime
import logging
import time
import re

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.iteritems()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, unicode):
        return input.encode('utf-8')
    else:
        return input

def parseTweet(tweet, filename):
	try:
		# Is this a nativevote tweet?
		text = ""
		if "text" in tweet.keys():
			text=tweet["text"].lower()
		user=tweet["user"]["screen_name"].lower()
		#if "nativevote" not in text and "nativevote" not in user and "nativelives" not in text and "nativelives" not in user and "nativesfor" not in text and "nativesfor" not in user and "notyourmascot" not in text and "notyourmascot" not in user and "#appropriation" not in text and "appropriation" not in user and "nativevoice" not in text and "nativevoice" not in user and "honorthetreaties" not in text and "honorthetreaties" not in user:
		#if ("dine" in text or "dine" in user or "blacklivesmatter" in text or "blacklivesmatter" in user) and ("native" not in text or "native" not in user or "indian" not in text or "indian" not in "user" or "indigenous" not in text or "indigenous" not in user):
			#return
		#Is this a nativevote tweet?
		#hashtags = tweet["entities"]["hashtags"]
		#for h in hashtags:
		#	if "nativevote" not in h['text'].lower():
		#		# Is this generated by @nativevote
		#		if "nativevote" not in tweet['user']['screen_name'].lower():
		#			# Is this in response to @nativevote
		#			for user in tweet["entities"]["user_mentions"]:
		#				if "nativevote" not in user["screen_name"]:
		#					print(tweet)
		#					return 
		# Get basic tweet info (all tweets have this)
		tid = tweet["id"]
		if "text" in tweet.keys():
			text = re.sub('[^A-Za-z0-9:\/.#@\&]+', ' ', tweet["text"])
		uid = tweet["user"]["id"]
		uname = tweet["user"]["screen_name"]
		ufollowcount = tweet["user"]["followers_count"]
		ufriendcount = tweet["user"]["friends_count"]
		ustatuscount = tweet["user"]["statuses_count"]
		ufavecount = tweet["user"]["favourites_count"]
		lat = ""
		lng = ""
		if tweet["coordinates"] != None:
			posn=tweet["coordinates"]["coordinates"]
		
		timestamp = float(tweet["timestamp_ms"])

		urls=[]
		if "urls" in tweet["entities"].keys():
			urlst = tweet["entities"]["urls"]
			for u in urlst:
				urls.append(u["expanded_url"])
		media=[]
		if "media" in tweet["entities"].keys():
			medialst=tweet["entities"]["media"]
			for m in medialst:
				media.append(m["media_url_https"])
		hashtags=[]
		if "hashtags" in tweet["entities"].keys():
			hashlst = tweet["entities"]["hashtags"]
			for h in hashlst:
				hashtags.append(h["text"].lower())
		mentions=[]
		if "user_mentions" in tweet["entities"].keys():
			mentionlst = tweet["entities"]["user_mentions"]
			for m in mentionlst:
				mentions.append(str(m["id"]))
	
		replytouser = tweet["in_reply_to_user_id"]
		replytostatus = tweet["in_reply_to_status_id"]
		# Now if it is a retweet
		oid=""
		otimestamp=timestamp
		ouid=""
		oufollowcount=""
		oufriendcount = ""
		oufavecount=""
		oustatuscount=""
		olat = ""
		olng = ""
		oreplytouser = ""
		oreplytostatus = ""
		if "retweeted_status" in tweet.keys():
			oid=tweet["retweeted_status"]["id"]
			created_at=tweet["retweeted_status"]["created_at"]
			ts = time.mktime(time.strptime(created_at,"%a %b %d %H:%M:%S +0000 %Y"))
			otimestamp=ts*1000
			ouid=tweet["retweeted_status"]["user"]["id"]
			oufollowcount=tweet["retweeted_status"]["user"]["followers_count"]
			oufriendcount=tweet["retweeted_status"]["user"]["friends_count"]
			oufavecount=tweet["retweeted_status"]["user"]["favourites_count"]
			oustatuscount=tweet["retweeted_status"]["user"]["statuses_count"]
			oreplytouser=tweet["retweeted_status"]["in_reply_to_user_id"]
			oreplytostatus=tweet["retweeted_status"]["in_reply_to_status_id"]
			if tweet["retweeted_status"]["coordinates"] != None:
                        	olat,olng=tweet["retweeted_status"]["coordinates"]
		with open(filename, 'a') as tf:
			tf.write("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (timestamp, tid, uid, uname, replytostatus, replytouser, oid, ouid, ufollowcount, ufriendcount, ufavecount, ustatuscount, lat, lng, ','.join(mentions), ','.join(hashtags), ','.join(urls), timestamp-otimestamp, otimestamp, oufollowcount, oufriendcount, oufavecount, oustatuscount, olat, olng, text))
	except KeyboardInterrupt:
		sys.exit(1)
	except Exception as e:
		print(e)
		

if __name__ == '__main__':

	# Get file names
	tweets_data_path = sys.argv[1]
	logfile = sys.argv[2]
	tweets_file = open(tweets_data_path, "r")
	for line in tweets_file:
    		try:
        		tweet = byteify(json.loads(line))
			parseTweet(tweet, logfile)
    		except:
        		continue

