#!/bin/bash
for e in $(nosetests -v --collect-only $1 2>&1 | pyp "p.split('(')[1].split(')')[0]|list(set(pp))|p|'.'.join(p.split('.')[:-1]) +':'+p.split('.')[-1]");
   do
    echo "Running nosetests " $e
    python manage.py local_db_reset;
    python manage.py syncdb;
    # Starting server process
    python -m zerorpcserver.service & zerorpc_pid=$! ;

    nosetests -v $e;

    # Killing original zerorpc server process
    kill $zerorpc_pid;
   done;
