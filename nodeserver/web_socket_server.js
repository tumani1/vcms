var PORT = 8001;

var WebSocketServer = require('ws').Server;
var zerorpc = require('zerorpc');
var http = require('http');


(function(){
    var httpServer = http.createServer(function (request, response) {
        response.writeHead(200, {'Content-Type': 'text/plain'});
        response.end();
    }).listen(PORT, function(){
        console.log((new Date()) + ' Server is listening on port ' + PORT);
    });

    var server = new WebSocketServer({server: httpServer});
    server.on('connection', function(socket){
        console.log((new Date()) + " New connection");
        socket.on("message", function(message){
            console.log((new Date()) + ' New message');
            var client = new zerorpc.Client();
            client.connect("tcp://127.0.0.1:4242");
            client.invoke("routing", message, function(error, res, more) {
                if (error){
                    console.error((new Date()) + " " + error);
                    return;
                }
                socket.send(res);
            });
        });
        socket.on("close", function (code, message) {
            console.log((new Date()) + " Connection closed with code: " + code);
            console.log("Message: " + message);
        });
    });
    server.on('error', function(error){
       console.error((new Date()) + " " + error)
    });

}).call();