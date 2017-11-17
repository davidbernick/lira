#!/usr/bin/env bash

docker build -t gcr.io/broad-dsde-mint-dev/lira:test ..

# Tell Jenkins to run both unittests in root folder and listener_utils package folder
docker run -e listener_config=config.json gcr.io/broad-dsde-mint-dev/lira:test bash -c "cd test && python -m unittest discover -v"
