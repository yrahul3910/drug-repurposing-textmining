const fs = require('fs');

if (process.argv.length != 3) {
    console.error('Usage: node low_confidence_prune.js <directory-path>\n');
    process.exit(1);
}

let path = process.argv[2];
let excerpts = [];
fs.readdir(path, (err, files) => {
    files.forEach(file => {
        let content = fs.readFileSync(`${path}/${file}`);
        let json = JSON.parse(content);
        let highConfidence = json.response.results.filter(x => x.alternatives[0].confidence >= 0.96);
        let objs = highConfidence.map(x => x.alternatives[0])
        excerpts = excerpts.concat(objs);
    });
    console.log(JSON.stringify(excerpts, null, 2)); // pretty-print
});

