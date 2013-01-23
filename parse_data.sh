#!/bin/bash
ls data | sed 's/\.7z$//g' | xargs -P 4 -n1 -I{} bash -c "7z x -so data/{}.7z | pv -c | python parse.py | pv -c > parsed_data/{}.json" 
