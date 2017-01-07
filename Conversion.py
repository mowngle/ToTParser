#Parser to Parse \r\BehindTheTables and \r\BehindTheScreen tables.
#1/7/2017, Release 1
#Author: Mowngle

import sys, argparse

inputfile = ''
outputfile = ''

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="Expected Input File")
parser.add_argument("-o", help="Expected Output File")
args = parser.parse_args()
inputfile = "table.txt"
outputfile = "out_table.txt"
if args.i:
	inputfile = args.i
if args.o:
	outputfile = args.o
	
print("The input file is {}".format(inputfile))
print("The output file is {}".format(outputfile))

#Open Input File
with open(inputfile) as inputObject, open(outputfile, "w+") as outputObject:
	
	#inputTextList = inputObject.readLines()
	contents = inputObject.read()
	inputTextList = contents.split("\n")
	
	#Parse first the line, this is the title.
	listSize = len(inputTextList)
	i = 0
	while (i < listSize):	
		#Next line has the dice type to look for.  e.g. d100 (case insensitive)
		line_tuple = inputTextList[i].split("\t")
		tab_len = len(line_tuple)
		if (tab_len == 0):
			break
		
		description = ""
		if (tab_len == 1):
			description = line_tuple[0]
			i += 1
			line_tuple = inputTextList[i].split("\t")
			
		#for each table, write an opening brace {
		outputObject.write("{\n")
		
		#write d:d<number> <title>
		outputObject.write("d:")
		outputObject.write(line_tuple[0].replace(" Roll", ""))
		outputObject.write(" ")
		if (len(description) == 0):
			outputObject.write(line_tuple[1])
		else:
			outputObject.write(description)
			
		outputObject.write("\n")
		
		#iterate over a given array
		while(True):
			i += 1
			if (i >= listSize or len(inputTextList[i]) == 0 or inputTextList[i].startswith('d')):
				break
			
			#split by the tab
			elementTuple = inputTextList[i].split("\t")
			
			if (len(elementTuple) < 2):
				break
			
			#parse the number on the left, verify its a number, check if there's a dash
			numberRange = elementTuple[0]
			tableElement = elementTuple[1]
			
			range = 1
			if (numberRange.find('-')!=-1):
				rangeList = numberRange.split('-')
				range = int(rangeList[1]) - int(rangeList[0]) + 1
			
			#copy the text on the right
			x = 0
			while(x < int(range)):
				outputObject.write("i:%s\n" % tableElement)
				x += 1

		#write the closing brace }			
		outputObject.write("}\n")