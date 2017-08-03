#!/usr/bin/bash

python main.py --csv && \
    diff -d <(cat output/*.csv) expected.txt && \
    rm output/*.csv
