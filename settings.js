var path = require('path'),
    fs = require("fs"),
    yaml = require("js-yaml");

exports.DEBUG = true;
var PROJECT_PATH = __dirname;
exports.TEMPLATES_PATH = path.join(PROJECT_PATH, 'templates');
exports.NODE = yaml.safeLoad(fs.readFileSync(path.join(PROJECT_PATH, 'nodeservices', 'node_service.yaml'), 'utf8'));
exports.HEARTBEAT = 100000; //собственное значение, нужен при локальной разработке