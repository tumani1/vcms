#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --json --client tcp://0.0.0.0:6600 route '{"api_method": "test/echo", "api_type":"put", "query_params":{"message":"hello"}, "token": "foobar"}'
