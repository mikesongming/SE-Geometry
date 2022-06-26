#!/bin/bash

git add -A .
git diff --name-only --exit-code HEAD
if [ 0 -ne $? ];
then
    git commit -m 'temp commit with news'
fi

_VERSION_TAG=`git describe --dirty --long --always --tags --match 'v*'`
_DISTANCE=`echo $_VERSION_TAG | awk -F '-' '{print $2}'`

echo $_VERSION_TAG, $_DISTANCE

LOG_VERSION=`python -m versioningit -n`

if ! [[ "${_VERSION_TAG}" =~ .*"dirty".* ]] && [ $_DISTANCE -eq 0 ];
then
    echo 'clean'
    LOG_VERSION=`python -m versioningit`
fi

echo $LOG_VERSION

python -m towncrier build --version=$LOG_VERSION --yes
git reset --soft HEAD~
git add -A .
git commit -m "changelog v${LOG_VERSION}"
