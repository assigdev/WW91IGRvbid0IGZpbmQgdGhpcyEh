#!/bin/sh

# FIX Celery redis on Python3.7
# https://github.com/celery/celery/issues/4500
TARGET=/usr/local/lib/python3.7/site-packages/celery/backends
TARGET2=/usr/local/lib/python3.7/site-packages/celery/app
cd $TARGET
if [ -e async.py ]
then
    mv async.py asynchronous.py
    sed -i 's/async/asynchronous/g' redis.py
    sed -i 's/async/asynchronous/g' rpc.py
fi
cd $TARGET2
sed -i 's/re._pattern_type/re.Pattern/g' routes.py

# Fix Celery cython bug
# https://github.com/celery/celery/issues/4342
# TARGET=/usr/local/lib/python3.7/site-packages/celery/utils
# cd $TARGET
# sed -i 's/fun\.__module__/fun.__globals__["__name__"]/g' functional.py