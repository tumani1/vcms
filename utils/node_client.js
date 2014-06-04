var http = require("http");
var options = {
    hostname: '127.0.0.1',
    port: 7777,
//    path: "/api/v1/films/7914/persons.json.xml.yaml?type=a&top=4"
    path: "/users/info?type=a&top=4&id=77"
};


http.get(options, function(response) {
    response.on("data", function(chunk) {
        console.log(chunk.toString());
    });
    response.on("error", function(error) {
        console.log("error: "+error.message);
    })
});
console.log("exiting");