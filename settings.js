var path = require('path'),
    fs = require("fs"),
    yaml = require("js-yaml");


var PROJECT_PATH = __dirname;
exports.TEMPLATES_PATH = path.join(PROJECT_PATH, 'templates');
exports.NODE = yaml.safeLoad(fs.readFileSync(path.join(PROJECT_PATH, 'nodeservices', 'node_service.yaml'), 'utf8'));