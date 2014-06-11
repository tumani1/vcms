#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --json --client tcp://0.0.0.0:4242 route '{"api_group": "msgr", "api_method":"create", "api_format":"json", "token":"echo_token", "http_method":"put", "query_params":{"user_ids": 21 }}'
