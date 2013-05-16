#!/bin/sh

cd ../doc
./mkdoc.sh

cd ../prep-release
./distbuild.sh 
