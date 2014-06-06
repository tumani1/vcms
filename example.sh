#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --json --client tcp://0.0.0.0:4242 route '{"api_group": "persons", "api_method":"info", "api_format":"json", "token":"foobar", "http_method":"get", "query_params":{"person":"1"}}'

