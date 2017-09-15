#!/usr/bin/env bash

source config.sh
./subscription-create.py "$dss_url?replica=gcp" $green_url $listener_secret $key_file $query_json
