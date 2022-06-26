#!/bin/bash

git diff --name-only --exit-code HEAD
LOG_VERSION=`[[ 0 -eq $? ]] && versioningit || versioningit -n`
echo $LOG_VERSION
python -m towncrier build --version=$LOG_VERSION --yes

git add -A .
git commit -m "$changelog v${LOG_VERSION}"
