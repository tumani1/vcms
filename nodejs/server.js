var ws = require('nodejs-websocket');
var zerorpc = require('zerorpc');


(function(){
    var server = ws.createServer(function (conn) {
        console.log("New connection");

        conn.on("text", function (json) {
            var client = new zerorpc.Client();
            client.connect("tcp://127.0.0.1:4242");
            client.invoke("routing", json, function(error, res, more) {
                console.log(res);
                conn.sendText(res);
            });
        });

        conn.on("close", function (code, reason) {
            console.log("Connection closed")
        });
    }).listen(8001, '127.0.0.1');
}).call();