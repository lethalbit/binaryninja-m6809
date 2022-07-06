#!/usr/bin/env python
# SPDX-License-Identifier: BSD-3-Clause

from re import sub
import sys
import json
from pathlib import Path

LICENSE_FILE = Path('./LICENSE').resolve()
README_FILE  = Path('./README.md').resolve()
PLUGIN_FILE  = Path('./plugin.json').resolve()
PIP_REQ_FILE = Path('./requirements.txt').resolve()

PLUGIN_METADATA = {
	'pluginmetadataversion': 2,
	'name': 'MC6809/MC6809E Architecture',
	'type': [
		'architecture',
	],
	'api': [
		'python3',
	],
	'description': 'Architecture support for MC6809/MC6809E',
	'longdescription': '',
	'license': {
		'name': 'BSD-3-Clause',
		'text': None,
	},
	'platforms': [
		'Linux',
		'Darwin',
		'Windows',
	],
	'installinstructions': {
		'Linux': 'Install the `construct` python package',
		'Darwin': 'Install the `construct` python package',
		'Windows': 'Install the `construct` python package',
	},
	'dependencies': {
		'pip': [ ]
	},
	'version': None,
	'author': 'Aki "lethalbit" Van Ness',
	'minimumbinaryninjaversion': 3164
}

def get_version_tag():
	import subprocess

	GIT_GET_HASH  = ['git', 'rev-parse', '--short', 'HEAD']
	GIT_GET_DIRTY = ['git', 'diff', '--quiet']
	GIT_GET_TAG   = ['git', 'describe', '--tag']

	version = ''

	hash = subprocess.check_output(GIT_GET_HASH).decode('utf-8').strip()
	is_dirty = (subprocess.call(GIT_GET_DIRTY) == 0)
	has_tag = (subprocess.call(GIT_GET_TAG) == 0)
	tag = None
	if has_tag:
		tag = subprocess.check_output(GIT_GET_TAG).decode('utf-8').strip()

	if has_tag:
		version += tag
	else:
		version += hash

	if is_dirty and has_tag:
			version += f'-g{hash}'
	elif is_dirty and not has_tag:
		 version += '-dirty'

	return version

def main():
	if not LICENSE_FILE.exists() or not README_FILE.exists():
		print('Unable to find license or readme file')
		return 1

	plugin_data = None
	if PLUGIN_FILE.exists():
		with PLUGIN_FILE.open('r') as plg:
			plugin_data = json.load(plg)
	else:
		plugin_data = PLUGIN_METADATA
		with LICENSE_FILE.open('r') as lic:
			plugin_data['license']['text'] = lic.read()
		with README_FILE.open('r') as rdm:
			plugin_data['longdescription'] = rdm.read()


	plugin_data['version'] = get_version_tag()

	if PIP_REQ_FILE.exists():
		with PIP_REQ_FILE.open('r') as req:
			plugin_data['dependencies']['pip'] = list(map(lambda l: l.strip(), req.readlines()))


	with PLUGIN_FILE.open('w+') as plg:
		json.dump(plugin_data, plg, indent = 4)


	return 0



if __name__ == '__main__':
	sys.exit(main())
