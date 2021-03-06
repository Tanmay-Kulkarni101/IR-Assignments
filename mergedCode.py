import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import json 
from itertools import islice
import pprint
import os
import pickle
import math

def calc(tfval,dfval,number)
	return (1+math.log(tfval))*(math.log(number/dfval))

def tf_idf(reviews):
	'''This function takes a review as input and gives the tf_idf of each word for each document as the output'''
	df={} #dictionary to hold word:document frequency
	tf_overall={} #holds the tf for each word within a document 
	for document,content in reviews.items():
		if document not in tf_overall:
			tf_overall[document]={}
			tf_doc={} #temp tf for each document
			for word in content['text']:
				if word not in tf_doc: #checking for the first instance of a word
					if word not in df:
						df[word]=1
					else:
						df[word]=df[word]+1
					tf_doc[word]=1
				else:
					tf_doc[word]=tf_doc[word]+1

				tf_overall[document][word]=tf_doc[word] #Adding the list of word:freq dictionaries
	
	tf_idf={}
	number=len(document)
	for document,content in reviews.items():
		if document not in tf_idf:
			tf_idf[document]={} #mapping each tf_idf to the corresponding document
			tf_idf_doc={} #give the tf_idf for each word in a document
			for word in content['text']:
				val=calc(tf_overall[document][word],df[word],number)
				tf_idf_doc[word]=val
				tf_idf[document][word]=tf_idf_doc[word]

	return tf_idf

def main():
	with(open(os.getcwd()+'/yelp-dataset/yelp_academic_dataset_review.json')) as f:
		objects =(json.loads(line) for line in f)
		print(objects)
		reviews={}
		wordnet_lemmatizer=WordNetLemmatizer()
		i=0
		for x in objects:
			pp=pprint.PrettyPrinter(indent=4)
			tokens=nltk.word_tokenize(x['text'])
			tokens=[word.lower() for word in tokens if word.isalpha()]
			numWords=len(tokens)
			stop_words=stopwords.words('english')
			#print(stop_words)
			#print(tokens)
			tokens=[word for word in tokens if not(word in stop_words)]
			tokens=[wordnet_lemmatizer.lemmatize(word) for word in tokens]
			#print(stop_words)
			#print(tokens)
			reviews[x['review_id']]={'business':x['business_id'],'numWords':numWords,'stars':x['stars'],'text':tokens}
			i+=1
			tf_idf(reviews)
			#pp.pprint(reviews)
		with open('id_tokens_mappings.pickle', 'wb') as handle:
			pickle.dump(reviews, handle, protocol=pickle.HIGHEST_PROTOCOL)
		

if __name__ == '__main__':
	main()
