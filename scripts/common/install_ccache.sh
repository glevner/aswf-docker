#!/usr/bin/env bash
# Copyright (c) Contributors to the aswf-docker Project. All rights reserved.
# SPDX-License-Identifier: Apache-2.0

set -ex

mkdir ccache
cd ccache

if [ ! -f "$DOWNLOADS_DIR/ccache-${ASWF_CCACHE_VERSION}.tar.gz" ]; then
    curl --location "https://github.com/ccache/ccache/releases/download/v${ASWF_CCACHE_VERSION}/ccache-${ASWF_CCACHE_VERSION}.tar.gz" -o "$DOWNLOADS_DIR/ccache-${ASWF_CCACHE_VERSION}.tar.gz"
fi

tar xf "$DOWNLOADS_DIR/ccache-${ASWF_CCACHE_VERSION}.tar.gz"

cd "ccache-${ASWF_CCACHE_VERSION}"
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release -DZSTD_FROM_INTERNET=ON -DCMAKE_INSTALL_PREFIX=/usr/local ..
make -j$(nproc)
make install

mkdir -p /usr/local/bin/_ccache
ln -s /usr/local/bin/ccache /usr/local/bin/_ccache/gcc
ln -s /usr/local/bin/ccache /usr/local/bin/_ccache/g++
ln -s /usr/local/bin/ccache /usr/local/bin/_ccache/cc
ln -s /usr/local/bin/ccache /usr/local/bin/_ccache/c++
ln -s /usr/local/bin/ccache /usr/local/bin/_ccache/clang++
ln -s /usr/local/bin/ccache /usr/local/bin/_ccache/clang

# Create activate_ccache.sh script
cat <<EOF > /usr/local/bin/activate_ccache.sh
#!/usr/bin/env bash
export PATH=/usr/local/bin/_ccache:$PATH
if [ -z "$CCACHE_DIR"]
then
    export CCACHE_DIR=/tmp/ccache
fi
EOF
chmod a+x /usr/local/bin/activate_ccache.sh


cd ../../..
rm -rf ccache
