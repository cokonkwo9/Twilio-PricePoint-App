from flask import Flask, request
from twilio import twiml
from amazon.api import AmazonAPI
from twilio.rest import TwilioRestClient
import os
import urllib, urllib2
from collections import Iterable 
#import bottlenose


ACCOUNT_SID = "AC0d744ba37551fe0d5d45c09d905927b8"
AUTH_TOKEN = "28b92f97882766727c627c3d69975b28"

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

app = Flask(__name__)

@app.route("/")
def test():
	return "Boo"

@app.route('/sms', methods=['GET','POST'])
def sms():
	from_num = request.values.get('From', None)
	msg_body = request.values.get('Body', None)
	client.messages.create(
		to = request.values.get('From', None),
		from_= '+17707663503',
		body = itemLookup(msg_body))
	return " "

def itemLookup(msg_body):
	if len(msg_body) < 13 or len(msg_body) > 13:
		return "ISBN is invalid. Please enter the 13 digit ISBN of the book you wish to find."
	if len(msg_body) == 13:
		print "Starting Lookup"
		amazon = AmazonAPI('AKIAIUTY6Q2BBIRX6NSQ', 'fdx0iIhD462Uv1Rgj2SaHj/NQIMewZfQxktWA5cO', 'chika5-20')
		book = amazon.lookup(ItemId = msg_body, SearchIndex="Books", IdType="ISBN")
		print book
		if type(book) is list:
			thebook = book[0]
			price = thebook.price_and_currency[0]
			curr = thebook.price_and_currency[1]
			title = thebook.title
			return 'The book, "{}", can be found on Amazon for {} {}'.format(title , price, curr)
		else: 
			#thebook = book[0]
			price1 = book.price_and_currency[0]
			curr1 = book.price_and_currency[1]
			title1 = book.title
			return 'The book, "{}", can be found on Amazon for {} {}'.format(title1 , price1, curr1)
	return "Sorry. The book you requested was not found."

app.run()
