#!/bin/sh

# should generate wieghts.js from raw files

mkdir dist
cp -R ./images *.js *.css *.html dist
tar -czvf dist.tar.gz dist
