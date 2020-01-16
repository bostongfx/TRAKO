#!/bin/bash
./trakofy -i /home/haehn/Downloads/100408.vtp -o /tmp/100408.tko
./untrakofy -i /tmp/100408.tko -o /tmp/100408_restored.vtp
./tkompare -a /home/haehn/Downloads/100408.vtp -b /tmp/100408_restored.vtp
