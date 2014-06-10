var http  = require("http"),
    url = require("url"),
    fs = require("fs"),
    path = require("path"),
    yaml = require("js-yaml"),
    jade = require("jade");
    log = console.log;


function load_conf(filename) {
    return yaml.safeLoad(fs.readFileSync(path.resolve(__dirname, filename), 'utf8'));
}

function run_server(host, port) {
    var server = http.createServer(function(request, response) {
        if (request.method === "GET") {
            var parsed = url.parse(request.url);
            if (parsed.pathname === "/index.html") {
                jade.renderFile('/home/dmitriy/Projects/next_tv/templates/index.jade', options, function(err, html) {
                    response.end(html);
                });
            }
        }
    });
    server.on("error", function(error) {
        log(error);
        log(error.stack);
    });
    server.listen(host, port);
    log("render server runnig on "+host+":"+port);
}

var conf = load_conf('../configs/node_service.yaml');
run_server(conf["render_serv"]["host"], conf["render_serv"]["port"]);