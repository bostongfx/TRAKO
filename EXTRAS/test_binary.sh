#!/bin/bash
../trakofy -i ../DATA/example.vtp -o ../DATA/example.tko
cp ../DATA/example.tko ../DATA/example.gltf
ls -l ../DATA/example.gltf
node_modules/gltf-pipeline/bin/gltf-pipeline.js -i ../DATA/example.gltf -o ../DATA/example.glb
ls -l ../DATA/example.glb
node_modules/gltf-pipeline/bin/gltf-pipeline.js -i ../DATA/example.glb -o ../DATA/restored_from_bin.gltf
cp ../DATA/restored_from_bin.gltf ../DATA/restored_from_bin.tko 
../untrakofy -i ../DATA/restored_from_bin.tko -o DATA/restored_from_bin.vtp
../tkompare -a DATA/example.vtp -b DATA/restored_from_bin.vtp
