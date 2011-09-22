#!/bin/bash

./dev_build.sh
cd domestos
celeryd --discard -EB -l INFO -Q default,configurator,core,heartbeat,echo,lirc
cd -

