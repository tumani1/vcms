#!/bin/bash
# Example of client request for our backend zerorpc service
zerorpc --json --client tcp://127.0.0.1:7777 route '{"api_group": "test", "api_method":"echo", "token":"echo_token", "http_method":"get", "query_params":{"text": "FROM CONSOLE"}}'
