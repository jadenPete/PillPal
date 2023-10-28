import functools
import json
import os
import sys
import typing

@functools.cache
def get_config() -> typing.Any:
	try:
		with open(os.path.join(os.path.dirname(__file__), os.pardir, "config.json")) as file:
			return json.load(file)
	except (OSError, json.JSONDecodeError) as error:
		print(error, file=sys.stderr)

		return {
			"connectionInfo": "dbname=pill_pal"
		}
