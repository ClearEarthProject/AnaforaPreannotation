# Create preannotation files, given an Anafora directory and a word list.

import os
import sys
import argparse
from bs4 import BeautifulSoup, Comment, Tag, NavigableString

# Read in word list CSV and create dictionaries.
def read_CSV(csv_path):
	wordlist = dict()
	wordsToType = dict()
	with open(csv_path, 'r') as csvFile:
		csv = csvFile.readlines()
		for line in csv:
			entry = line.split(',')
			entry[0] = entry[0].lower()
			wordsToType[entry[0]] = entry[1].strip()
			startLetter = entry[0][0]
			if startLetter not in wordlist:
				wordlist[startLetter] = [entry[0]]
			else:
				wordlist[startLetter].append(entry[0])
	for letter in wordlist:
		wordlist[letter] = sorted(wordlist[letter], key=len, reverse=True)
	return wordlist, wordsToType

# Read in schema to obtain "parentType"s
def get_parent_types(schema_path):
	parents = dict()
	schemaText = ''
	with open(schema_path, 'r') as schemaFile:
		schemaText = schemaFile.read()
	soup = BeautifulSoup(schemaText, "html.parser")
	for parent in soup.findAll('entities'):
		parentType = parent['type']
		for child in parent.findAll('entity'):
			parents[child['type']] = parentType
	return parents

# Create preannotation files for all text files in the Anafora directory.
def create_preannotation(directory, schema_name, wordlist, wordsToType, parents):
	for root, directories, filenames in os.walk(directory):
		for filename in filenames:
			if '.' in filename:
				continue
			filename = os.path.join(root, filename)
			outputFile = open(filename + '.' + schema_name + '.preannotation.completed.xml', 'w')
			docName = filename.split('/')[-1]
			text = ''
			print(filename)
			with open(filename, 'r') as infile:
				text = infile.read()
			output = '<?xml version="1.0" encoding="UTF-8"?>\n\n<data>\n<info>\n\t<savetime>09:48:07 \
11-10-2016</savetime>\n\t<progress>completed</progress>\n</info>\n\n<schema path="./" \
protocol="file">temporal.schema.xml</schema>\n\n<annotations>\n'
			idIndex = 1
			i = 0
			while i < len(text):
				if text[i-1].isalpha():
					i += 1
					continue
				try:
					candidates = wordlist[text[i].lower()]
				except KeyError:
					i += 1
					continue
				foundMatch = False
				for candidate in candidates:
					if candidate == text[i:i + len(candidate)].lower():
						if i + len(candidate) < len(text) and text[i + len(candidate)].isalpha():
							continue
						output += '\t<entity>\n\t\t<id>' + str(idIndex) + '@e@' + docName + \
						'@gold</id>\n\t\t<span>' + str(i) + ',' + str(i + len(candidate)) + '</span>\n\t\t<type>'\
								  + wordsToType[candidate] + '</type>\n\t\t<parentsType>' + \
								  parents[wordsToType[candidate]] + \
								  '</parentsType>\n\t\t<properties></properties>\n\t</entity>\n\n'
						foundMatch = True
						idIndex += 1
						i += len(candidate)
						break
				if not foundMatch:
					i += 1
			output += '</annotations>\n\n</data>'
			outputFile.write(output)
			outputFile.close()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('--csv', dest='csv', help="CSV of phrases to preannotate")
	parser.add_argument('--schema', dest='schema', help="Path to Anafora schema XML")
	parser.add_argument('--name', dest='name', help="Schema name used in the filenames")
	parser.add_argument('--directory', dest='directory', help="Anafora directory to create preannotation files for")
	args = parser.parse_args()
	print(args)
	parents = get_parent_types(args.schema)
	wordlist, wordsToType = read_CSV(args.csv)
	create_preannotation(args.directory, args.name, wordlist, wordsToType, parents)

if __name__ == "__main__":
	main()