#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --client tcp://0.0.0.0:4242 routing '{"api_group": "users", "api_method":"friendship", "api_format":"json","http_method":"get","query_params":{"partner_id":1},"token": "foobar"}'
