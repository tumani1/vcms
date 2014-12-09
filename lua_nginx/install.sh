#!/bin/bash

set -x
cd /tmp

# Install requirements
sudo apt-get install gcc make cmake luarocks lua-cjson-dev libreadline-dev libncurses5-dev libpcre3-dev libssl-dev perl memcached libgd-dev libgeoip-dev libxslt-dev

# Extract Openresty
wget http://openresty.org/download/ngx_openresty-1.7.2.1.tar.gz
tar xzvf ngx_openresty-1.7.2.1.tar.gz
cd ngx_openresty-1.7.2.1/

# Install Openresty
make clean
./configure --with-cc-opt='-g -O2 -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security -D_FORTIFY_SOURCE=2' --with-ld-opt='-Wl,-Bsymbolic-functions -Wl,-z,relro' --prefix=/usr/share/nginx --conf-path=/etc/nginx/nginx.conf --http-log-path=/var/log/nginx/access.log --error-log-path=/var/log/nginx/error.log --lock-path=/var/lock/nginx.lock --pid-path=/run/nginx.pid --http-client-body-temp-path=/var/lib/nginx/body --http-fastcgi-temp-path=/var/lib/nginx/fastcgi --http-proxy-temp-path=/var/lib/nginx/proxy --http-scgi-temp-path=/var/lib/nginx/scgi --http-uwsgi-temp-path=/var/lib/nginx/uwsgi --with-debug --with-pcre-jit --with-ipv6 --with-http_ssl_module --with-http_stub_status_module --with-http_realip_module --with-http_addition_module --with-http_dav_module --with-http_geoip_module --with-http_gzip_static_module --with-http_image_filter_module --with-http_spdy_module --with-http_sub_module --with-http_xslt_module --with-mail --with-mail_ssl_module --with-luajit
make -j2
sudo make install

# Move Nginx file
sudo mv /usr/share/nginx/nginx/sbin/nginx /usr/sbin/

# Restart Nginx
sudo service nginx restart

# Restart memcached
sudo service memcached restart

nginx -V

exit 0
