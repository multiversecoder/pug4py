var fs = require("fs");
var path = require("path");
var Pug = require("pug");

try{
    if (process.argv[3].includes("/tmp/tmp")){
        var template = process.argv[3];
    }
    else {
        var template = path.join(process.argv[2], process.argv[3]);
    }
    var file = Pug.compileFile(template, {basedir: process.argv[2]});
    console.log(file(JSON.parse(
        fs.readFileSync(process.argv[4], {"encoding": "utf-8"}).toString())).replace(/<!--.*?-->/sg, ""));
} catch(e){
    console.log("#<PugJS_Error_for_python>: " + e);
}

