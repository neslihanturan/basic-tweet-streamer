#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twython import Twython, TwythonStreamer
from jinja2 import Environment, FileSystemLoader
import os, json, time, BaseHTTPServer,urllib2
from threading import Thread



HOST_NAME = 'localhost'
PORT_NUMBER = 9000
json_list = []
CONSUMER_KEY = YOUR_INFORMATION
CONSUMER_SECRET = YOUR_INFORMATION
ACCESS_TOKEN = YOUR_INFORMATION
ACCESS_TOKEN_SECRET = YOUR_INFORMATION
FILE_DIR = YOUR_INFORMATION
FILE_NAME = YOUR_INFORMATION


class TweetStreamer(TwythonStreamer):

	def on_success(self, data):		#is called when tweets are caught
		if 'text' in data:			#data is is json form, includes all information about tweet
			global json_list		#global json array will get filled with tweets
			data_new = {}			#build new json object with only necessary fields
			data_new['text'] = data['text']
			data_new['created_at'] = data['created_at']
			data_new['favorite_count'] = data['favorite_count']
			data_new['retweet_count'] = data['retweet_count']
			data_new['user_name'] = data['user']['screen_name']
			data_new['urls'] = []
			for url_types in data['entities']['urls']:
				data_new['text'] = data_new['text'].replace(url_types['url'].encode("utf8"), '')		#remove displayed url from tweet text, to put origin url instead
				try:
					extended_url = {}
					opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())		#to reach cookie required sites too
					shortenedUrl = opener.open(url_types['url'])
					extended_url['url'] = shortenedUrl.geturl()			#get real source of url
					data_new['urls'].append(extended_url)
					print(extended_url['url'])
				except (urllib2.HTTPError,urllib2.URLError) as e:
					pass
			json_list.append(data_new)

	def on_error(self, status_code, data):
		print status_code
		self.disconnect()

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
	def do_GET(s):		#is called after GET request

		j2_env = Environment(loader=FileSystemLoader(FILE_DIR),			#trim_blocks will achieve space management in json
				             trim_blocks=True
				           	)
		html_code = j2_env.get_template(FILE_NAME).render(			#render method will return final html as unicode string
										json_list=json_list
										)


		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()
		s.wfile.write(html_code.encode("utf16"))		#write file to display html, encode to convert unicode string to string




def stream_twitter(self):
	while True:
		try:
			print time.asctime(), "Stream Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
			streamer = TweetStreamer(CONSUMER_KEY, CONSUMER_SECRET,
			              			ACCESS_TOKEN, ACCESS_TOKEN_SECRET)		#give token parameters to construct streamer
			streamer.statuses.filter(track='asp')		#set tweet filter
			print time.asctime(), "Stream Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
		except:
			continue




def run_server(self):
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	httpd.serve_forever()		#start server



if __name__ == '__main__':


	thread1 = Thread( target=stream_twitter, args=("Thread-1", ) )
	thread2 = Thread( target=run_server, args=("Thread-2", ) )

	thread1.start()
	thread2.start()
