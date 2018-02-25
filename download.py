#!/usr/bin/env

import requests

if __name__ == '__main__':
	categories = ['hungary','IBM']
	for category in categories:
		url = 'http://api.nytimes.com/svc/search/v2/articlesearch.json'
		params = {}
		params['api-key'] = '8072c076f79340899b4887769f76fb5c'
		params['q'] = category
		response = requests.get(url = url, params=params ).json()
		#print response['response']
		file = open(category, "a")
		for doc in response['response']['docs']:
			file.write((doc['snippet'] + '\n').encode('utf-8'))
		file.close()