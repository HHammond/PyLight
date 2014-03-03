#PyLight

PyLight is a python binding for Mac OS X Spotlight.

#Goals

The goal of this project is to provide a functional and extendable framework for smart searching of files in OS X.


The general objective of PyLight is to provide a SQL style interface into searching for files with metatdata. Currently the options for this require using the terminal and knowing exactly which features you want to search for and then writing awkward queries. PyLight aims to extend the functionality of Apple's Spotlight by removing the need to know all of the metadata you're looking for. 

#Current State

Currently the project is not very far along. PyLight only supports queries of the form:

* `select <filetype>`
* `select <filetype> from <location>`
* `select <filetype> from <location> filter <filter_type> <filter_params>`

The only current filter right now is `re` which runs a Regex filter on the returned data from the query.