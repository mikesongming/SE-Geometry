#!/bin/bash

LINUX_WHEEL=`ls wheelhouse/*.whl | grep manylinux | head -n 1`
if [ -f "$LINUX_WHEEL" ]; then
    echo "Linux wheel $LINUX_WHEEL found."
else
    echo "NO linux wheel found!"
    return 1
fi

LINUX_PKG_TAG=`basename $LINUX_WHEEL | awk -F '-cp' '{print $1}' | sed 's/_/-/'`

LINUX_PKG_VERSION=`echo $LINUX_PKG_TAG | awk -F '-' '{print $NF}'`

LINUX_PKG_NAME=`echo $LINUX_PKG_TAG | sed "s/-$LINUX_PKG_VERSION//"`

echo "pkg_tag=${LINUX_PKG_TAG}" >> $GITHUB_ENV
echo "pkg_version=${LINUX_PKG_VERSION}" >> $GITHUB_ENV
echo "pkg_name=${LINUX_PKG_NAME}" >> $GITHUB_ENV
