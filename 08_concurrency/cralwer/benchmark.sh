#!/bin/bash

ulimit -n 2048

(python server.py --port=8080 &> /dev/null) &
server_pid=$!
sleep 1 # wait for server to be ready

for i in asyncio gevent tornado serial
    do 
        pushd $i
        python crawler.py
        popd
done

curl "localhost:8080/add?flush=True"
kill $server_pid

mkdir images
python visualize.py
