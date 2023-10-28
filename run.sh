#!/usr/bin/env bash

# Terminate webpack and sass when `flask run` exits
# https://stackoverflow.com/a/2173421
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

node_modules/.bin/webpack build --mode development --watch &

FLASK_APP=pill_pal.app FLASK_DEBUG=true flask run
