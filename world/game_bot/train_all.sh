#!/usr/bin/env bash

rm -rf models

docker run \
  -v $(pwd):/app/project \
  -v $(pwd)/models/rasa_core:/app/models \
  rasa/rasa_core:latest \
  train \
    --domain project/domain.yml \
    --stories project/data/stories.md \
    --out models

docker run \
  -v $(pwd):/app/project \
  -v $(pwd)/models/rasa_nlu:/app/models \
  rasa/rasa_nlu:latest-spacy \
  run \
    python -m rasa_nlu.train \
    -c config.yml \
    -d project/data/nlu.md \
    -o models \
    --project current
