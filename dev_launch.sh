#!/bin/bash

./dev_build.sh
cd domestos
celeryd --purge -EB -l INFO -Q default,lirc,echo,heartbeat
cd -

