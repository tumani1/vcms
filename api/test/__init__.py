# coding: utf-8
import rest_test
import render_test

routing = (
    (r'^echo$', {'put': rest_test.put, 'get': rest_test.get}),
    (r'^echo/(?P<id>\d+)$', {'get': render_test.get}),
    (r'^echoauth$', {'get': rest_test.echo_auth}),
)










