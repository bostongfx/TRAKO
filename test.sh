#!/bin/bash
./trakofy.py -i example.vtp -o example.tko
./untrakofy.py -i example.tko -o restored.vtp
./compare.py -a example.vtp -b restored.vtp