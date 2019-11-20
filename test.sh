#!/bin/bash
./trakofy -i DATA/example.vtp -o DATA/example.tko
./untrakofy -i DATA/example.tko -o DATA/restored.vtp
./tkompare -a DATA/example.vtp -b DATA/restored.vtp
