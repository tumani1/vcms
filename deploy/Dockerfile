# sshd
#

FROM ubuntu:14.04
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 1C61B9CD
RUN sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv C7917B12


RUN echo 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' | sudo tee /etc/apt/sources.list.d/mongodb.list
RUN echo "deb http://ppa.launchpad.net/chris-lea/node.js/ubuntu trusty main" >> /etc/apt/sources.list
RUN echo "deb-src http://ppa.launchpad.net/chris-lea/node.js/ubuntu trusty main" >> /etc/apt/sources.list
RUN echo "deb http://ppa.launchpad.net/vbernat/haproxy-1.5/ubuntu trusty main" >> /etc/apt/sources.list
RUN echo "deb-src http://ppa.launchpad.net/vbernat/haproxy-1.5/ubuntu trusty main" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y --force-yes openssh-server nginx supervisor pyp nodejs node-gyp mongodb-org git libpq-dev libzmq-dev haproxy python-dev python-virtualenv language-pack-en-base 
# Set the locale
RUN locale-gen en_US.UTF-8  
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8 
RUN apt-get install -y postgresql




RUN mkdir /var/run/sshd
RUN echo 'root:test' | chpasswd
RUN sed -i 's/PermitRootLogin without-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN locale



RUN service postgresql start; echo "CREATE USER pgadmin WITH SUPERUSER CREATEDB CREATEROLE REPLICATION PASSWORD 'qwerty'; CREATE DATABASE next_tv WITH OWNER pgadmin; GRANT ALL PRIVILEGES ON DATABASE next_tv TO pgadmin;  " | sudo -u postgres psql





COPY id_rsa /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/id_rsa
COPY known_hosts /root/.ssh/known_hosts
RUN ps
RUN git clone --recursive git@git.aaysm.com:developers/next_tv.git /root/next_tv ; cd /root/next_tv/;  git checkout develop

RUN mkdir /data; mkdir /data/db
RUN mongod --repair; 
RUN mongod --fork -f /etc/mongod.conf --smallfiles; cd /root/next_tv; mongo next_tv utils/mongodb.js; ps aux| grep mongo | grep fork | pyp "p.split()[1]";  kill -9 $(ps aux| grep mongo | grep fork | pyp "p.split()[1]"); sudo mongod -f /etc/mongod.conf --auth --smallfiles --fork; 

RUN cd /root/next_tv/; git submodule update --init
RUN cd /root/next_tv/; git submodule foreach git pull origin master
RUN cd /root/next_tv/nodeservices/; npm install; 
RUN cd /root/; virtualenv nextvenv;
RUN cp /root/next_tv/configs/db.yaml.example /root/next_tv/configs/db.yaml
RUN cd /root/next_tv/; /root/nextvenv/bin/pip install -r deploy/requirements.txt
RUN sudo -u postgres pg_dropcluster --stop 9.3 main
RUN sudo -u postgres pg_createcluster --start 9.3 main --locale en_US.UTF-8
RUN service postgresql start; echo "CREATE USER pgadmin WITH SUPERUSER CREATEDB CREATEROLE REPLICATION PASSWORD 'qwerty'; CREATE DATABASE next_tv WITH OWNER pgadmin; GRANT ALL PRIVILEGES ON DATABASE next_tv TO pgadmin;  " | sudo -u postgres psql
RUN locale; cd /root/next_tv/; service postgresql start; /root/nextvenv/bin/python -m utils.next_tv_sync


RUN service postgresql start; cd /root/next_tv/; /root/nextvenv/bin/python utils/gen_configs.py

RUN  cd /root/next_tv/generated_configs/; mv node_service.yaml ../nodeservices/
RUN  cd /root/next_tv/generated_configs/; mv haproxy.conf /etc/haproxy/
RUN  cd /root/next_tv/generated_configs/; mv pr_haproxy.conf zerorpc_services.conf /etc/supervisor/conf.d/

COPY docker_supervisor.conf /etc/supervisor/conf.d/
COPY admin.conf /etc/supervisor/conf.d/

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
EXPOSE 80
CMD ["/usr/sbin/sshd", "-D"]

