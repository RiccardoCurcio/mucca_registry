#!/bin/bash
rm -rf vendor &&
mkdir vendor &&
cd vendor &&
git clone https://github.com/fefender/mucca_connector_py.git &&
cd mucca_connector_py && git checkout -b develop && git pull origin develop
cd ..
