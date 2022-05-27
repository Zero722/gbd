const ObjectsToCsv = require('objects-to-csv');
 
// Sample data - two columns, three rows:
const data = [
  {code: 'CA', name: 'California'},
  {code: 'TX', name: 'Texas'},
  {code: 'NY', name: 'New York'},
];
 
// If you use "await", code must be inside an asynchronous function:
(async () => {
  const csv = new ObjectsToCsv(data);
 
  // Save to file:
  await csv.toDisk('./test.csv');
 
  // Return the CSV file as string:
  console.log(await csv.toString());
})();