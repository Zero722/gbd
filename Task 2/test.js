const parse = require('csv-parse')
const fs = require('fs') 

const data = []
fs.createReadStream("url.csv")
  .pipe(parse({ delimiter: ',' }))
  .on('data', (r) => {
    data.push(r.toString());        
  })
  .on('end', () => {
    console.log(data);
    console.log(typeof(data));

  });


console.log(data)