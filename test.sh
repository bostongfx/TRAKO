#!/bin/bash
./trakofy.py -i DATA/example.vtp -o DATA/example.tko
./untrakofy.py -i DATA/example.tko -o DATA/restored.vtp
./compare.py -a DATA/example.vtp -b DATA/restored.vtp
