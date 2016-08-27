'''
Simple quick utility Script which is a wrapper over
Curl command to hit Elastic Search ES_SERVER
Script helps in:
- typing less like the Elastic server path shouldn't be
  typed over and over again while calling curl,
- pretty print of response
- Dont have to write the curl arg identifiers
- Does json checking for the inputted body
'''
import sys, os, json, urllib2
import requests

ES_SERVER = 'http://localhost:9200'

def printUsage():
	scriptName = os.path.basename(sys.argv[0])
	print 'Usage  : ' + scriptName + ' <HTTP_METHOD> <PATH?QUERY_STRING>'
	print 'Example: ' + scriptName + ' GET|POST|PUT|HEAD|DELETE /index_name/type_name/id?pretty'

def checkCommandArgs():
	if (len(sys.argv)<3):
		printUsage()
		sys.exit(-1)

def getBodyInputFromUser():
	print 'Enter Body(Optional) (Press Enter, to curl call Elastic server):'
	body = ''
	while True:
		line = raw_input().strip()
		if not line: break
		body = body + line
	return body

def getPrettyAppend(urlPath):
	prettyAppend = ''
	if 'pretty' not in urlPath:
		if '?' in urlPath:
			prettyAppend = '&pretty'
		else:
			prettyAppend = '?pretty'

	return prettyAppend

def getParsedBodyJson(body):
	bodyJson = None
	if (len(body) > 0):
		try:
			bodyJson = json.loads(body)
		except Exception as e:
			print >> sys.stderr, 'Incorrect body JSON, Error: %s' % e
			body = getBodyInputFromUser()
			return getParsedBodyJson(body)

	return bodyJson

def getCurlBodyPortion(prettyBodyJsonStr):
	curlBodyPortion = ''
	if len(prettyBodyJsonStr.strip()) > 0:
		curlBodyPortion = " -d'" + prettyBodyJsonStr +  "'"

	return curlBodyPortion

def getParsedJsonPrettyStr(body):
	prettyBodyJson = ''
	parsedBodyJson = getParsedBodyJson(body)
	if parsedBodyJson != None:
		prettyBodyJson = json.dumps(parsedBodyJson, indent=4, separators=(',', ': '))

	return prettyBodyJson

if __name__ == '__main__':
	checkCommandArgs()

	httpMethod = sys.argv[1]
	urlPath = sys.argv[2]

	body = getBodyInputFromUser()
	prettyBodyJsonStr = getParsedJsonPrettyStr(body)
	curlBodyPortion = getCurlBodyPortion(prettyBodyJsonStr)

	prettyAppend = getPrettyAppend(urlPath)
	urlPath = urlPath + prettyAppend

	curlCommand = 'curl -X' + httpMethod + ' ' + ES_SERVER + urlPath 
	print 'Executing:\n' + curlCommand + curlBodyPortion
	response = requests.request(httpMethod, ES_SERVER + urlPath, data=prettyBodyJsonStr)


	print '\nResponse:'
	print(response.text)
