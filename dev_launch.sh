#!/bin/bash

./dev_build.sh
cd domestos
celeryd --discard -EB -l INFO
cd -

