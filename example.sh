#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --json --client tcp://0.0.0.0:4242 route '{"api_group": "msgr", "api_method":"info", "token":"echo_token", "http_method":"get", "query_params":{"id":1}}'
