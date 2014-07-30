#!/bin/bash
for e in $(nosetests -v --collect-only $1 2>&1 | pyp "p.split('(')[1].split(')')[0]|list(set(pp))|p|'.'.join(p.split('.')[:-1]) +':'+p.split('.')[-1]");
   do
    echo "Running nosetests " $e
    python -m utils.next_tv_clear -y;
    python -m utils.next_tv_sync;
    # Starting server process
    python -m zerorpcservices.rest_service & zerorpc_pid=$! ;

    nosetests -v --with-xunit --xunit-file=$(echo $e| pyp "'_'.join(p.split(':')[0].split('.')+p.split(':')[1:]) +'.xml'") $e;

    # Killing original zerorpc server process
    kill $zerorpc_pid;
   done;
