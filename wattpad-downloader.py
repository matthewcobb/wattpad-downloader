#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__      = "@carlosgarciamou"

#Usage: execute this file followed by "--help"

#Parameters
DownloadDirectory = '/' #Save to current directory
#End parameters

from urllib.request import urlopen
import re
import time
import sys

start = time.time()

def everything_between(text,begin,end):
    idx1=text.find(begin)
    idx2=text.find(end,idx1)
    return text[idx1+len(begin):idx2].strip()

def getPartContent(part,extra,option):

	partURL = 'http://www.wattpad.com/' + partIDs[part] + extra

	partContent = urlopen(partURL).read().decode('utf-8')

	splita = partContent.split('<div class="panel panel-reading" dir=\'ltr\'>',1)
	splitb = splita[1].split('</p></pre>')

	splitTitle = everything_between(splita[0],'<title>','</title>')
	fullpage = splitTitle.split(' - ')

	if (option=='a'):
		content = re.sub('<[^<]+?>', '\n', splitb[0])
		title = int(re.search(r'\d+', fullpage[2]).group())
		ChapterTitle = everything_between(splitTitle,'- ',' -')
		return content, title, ChapterTitle
	elif (option=='b'):
		newcontent = re.sub('<[^<]+?>', '\n', splitb[0])
		title = int(re.search(r'\d+', fullpage[2]).group())
		return newcontent, title
	elif (option=='c'):
		maxtitle = int(re.search(r'\d+', fullpage[2]).group())
		return maxtitle
	else:
		print('Error 1')

#Get URL

if len(sys.argv) > 1:
	link = str(sys.argv[1])
else:
	link = '--help'

if link!='--help':

	storyURL = link + '/parts'

	#Load /parts website

	html = urlopen(storyURL).read().decode('utf-8')
	StoryTitle = everything_between(html,'<title>',' -').replace(' ','-')


	print('Downloading "'+StoryTitle+'"...')

	#Get array of parts

	splitarriba = html.split('<ul class="table-of-contents">',1)

	splitabajo = splitarriba[1].split('</ul>')

	splitbis = splitabajo[0].split('"')


	partIDs = []
	ids = 0

	while ((len(splitbis)-1)/6>ids):
		partIDs.append(splitbis[ids*6+1])
		ids = ids+1


	#print (partIDs)

	#Get content of each part


	chapters = []
	ChapterTitles = []

	tries = 0
	nchap = len(partIDs)

	while tries<len(partIDs):
		variables=getPartContent(tries,'','a')
		content = variables[0]
		title = variables[1]
		ChapterTitle = variables[2]
		print('Page added')
		
		maxtitle = getPartContent(tries,'/page/999999','c')
		PagNum = 2
		while (title!=maxtitle):
			num = str(PagNum)
			variables = getPartContent(tries,'/page/'+num,'b')
			newcontent = variables[0]
			title = variables[1]
			content = content+newcontent
			PagNum = PagNum+1
			print('Page added')

		#Add chapter to "chapters" list

		chapters.append(content)

		#Add chapter title to "ChaperTitles"

		tries = tries+1

		ChapterTitles.append(ChapterTitle)
		print(ChapterTitle+'                    '+str(tries)+'/'+str(nchap))
		



	FullStory = ''
	added = 0

	while (added<len(chapters)):
		FullStory = FullStory + ChapterTitles[added] + '\n\n' + chapters[added] + '\n\n'
		added = added + 1


	text_file = open(DownloadDirectory+StoryTitle+'.txt', 'w')
	text_file.write(FullStory)
	text_file.close()

	print ("Done!")
	print('Story downloaded to: '+DownloadDirectory+StoryTitle+'.txt')

	end = time.time()
	elapsed = end - start

	print ('Execution time: ')
	print (elapsed)

else:
	print("""Usage: pithon3 wattpad-downloader.py [Story URL]\nThe output will be a txt file with the name of the Wattpad story. It will be saved by default in the current folder.""")
