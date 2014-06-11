#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --json --client tcp://0.0.0.0:4242 route '{"api_group": "topics", "api_method":"info", "api_format":"json", "token":"echo_token", "http_method":"get", "query_params":{"name":"test11"}}'
