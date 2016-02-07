from sys import argv
import re
import json

class Processor:
	def __init__(self, qualifactionsFile, inputFile, outputFileName):
		self.InputFileName = inputFile
		self.QualificationsFile = qualifactionsFile
		self.OutputFileName = outputFileName

	def Run(self):
		inputData = self.__LoadInputData()
		qualificationsData = self.__LoadQualificationsData()
		outputLines = self.__BuildOutput(inputData, qualificationsData)
		outputString = self.__BuildPreliminaryString(inputData, outputLines)
		outputString = self.__ReplaceFieldsInString(inputData, outputString)
		self.__WriteOutputFile(outputString)

	def __LoadInputData(self):
		filedata = open(self.InputFileName, "r").read()
		return json.loads(filedata)

	def __LoadQualificationsData(self):
		filedata = open(self.QualificationsFile, "r").read()
		return json.loads(filedata)

	def __BuildOutput(self, inputData, qualificationsData):
		if "items" not in inputData:
			raise Exception("Please make sure the input file has an items element")

		outputLines = []
		for foundQualification in inputData["items"]:
			found = False
			for definedQualification in qualificationsData:
				if (foundQualification.lower() == definedQualification["name"].lower()):
					found = True
					outputLines.append(definedQualification["text"])

			if found is False:
				raise Exception("WARNING: Could not `find` %s qualifcation in qualification.json" % foundQualification)

		return outputLines

	def __BuildPreliminaryString(self, inputData, lines):
		if "opening" not in inputData:
			raise Exception("Please make sure the input file has an opening element")

		if "itemsOpening" not in inputData:
			raise Exception("Please make sure the input file has an itemsOpening element")	

		if "closing" not in inputData:
			raise Exception("Please make sure the input file has an closing element")	

		items = [inputData["opening"],
				"\n\n",
				inputData["itemsOpening"], 
				" ",
				" ".join(lines),
				"\n\n",
				 inputData["closing"], 
				"\n\n"]
		return "".join(items)

	def __ReplaceFieldsInString(self, inputData, string):
		for replaceField, replaceValue in inputData["fields"].items():
			string = self.__ReplaceFields(replaceField, replaceValue, string)
		return string

	def __ReplaceFields(self, fieldName, value, text):
		print (fieldName)
		return re.sub("{" + fieldName + "}", value, text)	

	def __WriteOutputFile(self, string):
		outputFile = open(self.OutputFileName, "w")
		outputFile.write(string)	

processor = Processor("qualification.json", "input.json", "output.txt")
processor.Run()