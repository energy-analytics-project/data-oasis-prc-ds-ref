#!/bin/bash

# -----------------------------------------------------------------------------
# 60_dist.sh : create distribution to archive
# -----------------------------------------------------------------------------

if [ -d ./dist ]; then
    chmod -R +w ./dist
    rm -rf ./dist
fi
mkdir -p ./dist/zip
mkdir -p ./dist/db
cp -r ./zip/*.zip ./dist/zip/.
cp -r ./zip/state.txt ./dist/zip/.
chmod +w ./dist/zip/*
cp ./db/*.db ./dist/db/.
chmod +w ./dist/db/*
pigz ./dist/db/*.db
