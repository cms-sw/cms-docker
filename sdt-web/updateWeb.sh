#!/bin/sh -e
cd /data/cms-sw.github.io
git pull --rebase
jekyll build
