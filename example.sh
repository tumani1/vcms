#!/bin/bash
# Example of client request for our backend zerorpc service
<<<<<<< Updated upstream
zerorpc --json --client tcp://0.0.0.0:4242 route '{"api_group": "test", "api_method":"echo", "http_method":"put", "query_params":{"message":"hello"}, "token": "foobar"}'
=======
zerorpc --json --client tcp://0.0.0.0:4242 route '{"api_group": "topics", "api_method":"subscribe", "api_format":"json", "token":"foobar", "http_method":"post", "query_params":{"name":"test"}}'
>>>>>>> Stashed changes
