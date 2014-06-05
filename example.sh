#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --client tcp://0.0.0.0:4242 routing '{"api_group": "topics", "api_method":"info", "api_format":"json", "token":"foobar", "http_method":"get", "query_params":{"name":"test"}}'
