#!/bin/bash

LATEST_TAR_GZ=`ls -t dist/*.tar.gz | head -n 1`
if [ -f "$LATEST_TAR_GZ" ]; then
    echo "Latest sdist $LATEST_TAR_GZ found."
else
    echo "NO sdist found!"
    return 1
fi

LATEST_PKG_TAG=`basename $LATEST_TAR_GZ | sed 's/.tar.gz//' | sed 's/_/-/'`

LATEST_PKG_VERSION=`echo $LATEST_PKG_TAG | awk -F '-' '{print $NF}'`

PKG_NAME=`echo $LATEST_PKG_TAG | sed "s/-$LATEST_PKG_VERSION//"`

echo "pkg_sdist=${LATEST_TAR_GZ}" >> $GITHUB_ENV
echo "pkg_tag=${LATEST_PKG_TAG}" >> $GITHUB_ENV
echo "pkg_version=${LATEST_PKG_VERSION}" >> $GITHUB_ENV
echo "pkg_name=${PKG_NAME}" >> $GITHUB_ENV
