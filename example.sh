#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --json --client tcp://0.0.0.0:4242 route '{"api_group": "test", "api_method":"echo", "api_format":"json", "token":"foobar", "http_method":"put", "query_params":{"message":"test"}}'
