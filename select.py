import subprocess
import re
import os
import sys
from collections import namedtuple
import reparse
import shlex

class BaseSearch():

	"""	Base Search:
		The simplest form of grabbing data from OS and filtering it
	"""

	def __init__(self):
		pass

	def search(self, base_search, Filter=None, args=None, **kwargs):
		"""
		Search for results from base_search, then apply filtering and processing
		"""

		arguments = []

		if args:
			arguments = arguments + args

		cmd = ['mdfind']+shlex.split(base_search)
		pipe = subprocess.Popen(
			cmd,
			stdout=subprocess.PIPE
		)

		output,err= pipe.communicate()
		
		# Filter output data
		output = re.split(r'\n', output)
		
		if Filter:
			output = [x for x in output if Filter(x)]

		return "\n".join(output)

def ActionType(Action):
	"""	Specify the type of the action to be performed
	"""
	if Action == 'select' or Action == 'find':
		return "select"
	return Action

def DocumentClass(Type):
	"""	Breakdown query file type into metadata search params
	"""
	document_types = {
		"file":		"kMDItemContentTypeTree == public.content",
		"script":	"kMDItemContentTypeTree == public.script",
		"code":		"kMDItemContentTypeTree == public.source-code",
		"text":		"kMDItemContentTypeTree == public.text",
		"document":	"kMDItemContentTypeTree == public.data",
		"picture":	"kMDItemContentTypeTree == public.image",
		"movie":	"kMDItemContentTypeTree == public.video",
		"audio":	"kMDItemContentTypeTree == public.audio",
		"pdf":		"kMDItemContentTypeTree == com.adobe.pdf",
		"folder":	"kMDItemContentTypeTree == public.folder",
		"all":		"kMDItemContentTypeTree == public.item",
	}

	return document_types[Type]

def FolderParse(Location=None):
	"""Get location from query. 
	"""
	return Location

def SelectQuery(Action=None, Target=None):
	"""Start building the query"""
	return {"Action":Action, "Target":Target}

def SelectQueryLocation(Query=None,Location=None):
	"""Take base query and add location field."""
	Query['Location'] = Location
	return Query

def SelectQueryFilter(Query=None,Filter=None):
	"""Select filter type and append filter"""
	Query['Filter'] = Filter
	return Query

def Filter(Type,Content):
	"""Create Filter"""
	return {'Type':Type,'Content':Content}

def SelectBaseQuery(Query=None):
	"""Consolidate both initial query types into the same pattern"""
	return Query

if __name__=="__main__":

	# Get command line args
	args = sys.argv[1:]

	# form into query structure
	query = "\n".join(args)+"\n"

	# Initialize parsing functions for cleaning data
	parsing_functions = {
		# Expressions
		
		# Actions
		'Select':				ActionType,
		
		# Document Types
		'Doctype':				DocumentClass,
		'Folder'	:			FolderParse,
		
		# Filters
		'Regex':				Filter,
		
		# Patterns	
		
		# Query Rules
		'Query':				SelectQuery,
		'QueryLocation':		SelectQueryLocation,

		# Merge base queries into general object
		'BaseQuery':			SelectBaseQuery,
		
		# Filter on query object
		'QueryFilter':			SelectQueryFilter,
		'QueryFilterLocation':  SelectQueryFilter,
		# 'QueryLocationFilter':	SelectQueryFilter
	}

	# Get current path. Note: This won't work when not run
	# from the project folder. Once the project is further
	# along we will change this. 
	path = os.getcwd()+os.sep

	# Prepare Parser
	query_parser = reparse.parser(
		parser_type=reparse.alt_parser,
		expressions_yaml_path=path + "expressions.yaml",
		patterns_yaml_path=path + "patterns.yaml",
		functions=parsing_functions
	)

	# Run query
	q = query_parser(query)

	# check if sucessful
	if q != []:
		q = q[0][0]
	else:
		print "Invalid Query"
		exit()

	# Select query
	if q['Action'] == 'select':

		search = BaseSearch()
		
		if not 'Location' in q:
			q['Location'] = '.'

		base = "\"%(Target)s\" -onlyin %(Location)s"%q

		if 'Filter' in q:

			if 're' == q['Filter']['Type']:
				filter = lambda x: re.match(q['Filter']['Content'],x)
			
			print search.search(base,Filter = filter)

		else:
			search = BaseSearch()
			print search.search(base,Filter = None)
