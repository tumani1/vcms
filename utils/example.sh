#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --json --client tcp://0.0.0.0:6600 route '{"api_group": "test", "api_method":"echo", "http_method":"put", "query_params":{"message":"hello"}, "token": "foobar"}'
