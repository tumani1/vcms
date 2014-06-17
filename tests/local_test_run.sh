#!/bin/bash
python -m zerorpcserver.server & some_pid=$! ;
mv configs/db.yaml configs/db.yaml.production;
mv configs/db.yaml.test configs/db.yaml;
nosetests;
mv configs/db.yaml configs/db.yaml.test;
mv configs/db.yaml.production configs/db.yaml;
kill $some_pid
