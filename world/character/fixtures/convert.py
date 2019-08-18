#!/usr/bin/env python

import json
import yaml

with open('abilities.json', 'r') as fin:
    with open('abilities.yaml', 'w') as fout:
        yaml.dump(json.load(fin), fout, default_flow_style=False)
