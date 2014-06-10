var http = require("http");
var options = {
    hostname: '127.0.0.1',
    port: 8080,
//    path: "/api/v1/films/7914/persons.json.xml.yaml?type=a&top=4"
//    path: "/users/453/info",
    path: '/test/echo',
    method: 'POST'
};


var request = http.request(options, function(response) {
    response.on("data", function(chunk) {
        console.log(chunk.toString());
    });
    response.on("error", function(error) {
        console.log("error: "+error.message);
    })
});

request.on("error", function(error) {
        console.log("request error: "+error.message);
    });

var large_obj = {};
for (var i=1;i<10000;i++) {
    large_obj["field"+i] = i;
}
request.write(JSON.stringify({field1: 1, field2: true, field3: [1,2,3]}));
//request.write(JSON.stringify(large_obj));
request.end();
console.log("exiting");