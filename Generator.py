from sys import argv
import re
import json

def ReplaceFields(fieldName, value, text):
	print fieldName
	return re.sub("{" + fieldName + "}", value.encode('utf-8'), text)

def LoadInputData():
	filedata = open("input.json", "r").read()
	return json.loads(filedata)

def LoadQualificationsData():
	filedata = open("qualification.json", "r").read()
	return json.loads(filedata)


def BuildOutput(inputData, qualificationsData):

	outputLines = []
	for foundQualification in inputData["items"]:
		found = False
		for definedQualification in qualificationsData:
			if (foundQualification.lower() == definedQualification["name"].lower()):
				found = True
				outputLines.append(definedQualification["text"])

		if found is False:
			print "WARNING: Could not `find` %s qualifcation in qualification.json" % foundQualification

	return outputLines

def BuildPreliminaryString(inputData, lines):
	items = [inputData["opening"].encode('utf-8'),
			"\n\n",
			inputData["itemsOpening"].encode('utf-8'), 
			" ",
			" ".join(lines).encode('utf-8'),
			"\n\n",
			 inputData["closing"].encode('utf-8'), 
			"\n\n"]
	return "".join(items)

def ReplaceFieldsInString(inputData, string):
	for replaceField, replaceValue in inputData["fields"].iteritems():
		string = ReplaceFields(replaceField, replaceValue, string)

	return string

def WriteOutputFile(string):
	outputFile = open("output.txt", "w")
	outputFile.write(string)

def Run():
	inputData = LoadInputData()
	qualificationsData = LoadQualificationsData()
	outputLines = BuildOutput(inputData, qualificationsData)
	outputString = BuildPreliminaryString(inputData, outputLines)
	outputString = ReplaceFieldsInString(inputData, outputString)
	WriteOutputFile(outputString)

Run()