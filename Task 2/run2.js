// Import 
const puppeteer = require('puppeteer');
const fs = require('fs');
const ObjectsToCsv = require('objects-to-csv');

// Declare File Path
const sc_path = __dirname + '\\' + "gshopping_sc" + '\\';
const csv_path = __dirname + '\\' + 'gshopping_csv' + '\\';
const dump_path = __dirname + '\\' + 'gshopping_dump' + '\\';

file_path = [sc_path, csv_path, dump_path]

// Make required Folders if it doesnt exist
file_path.forEach(element => {
  if (!fs.existsSync(element)) {
    fs.mkdirSync(element);
  }
});

// Get urls from csv File
var file_array = fs.readFileSync('url2.csv').toString().split("\r\n");
file_array.shift()

tocsv1 = [];
tocsv2 = [];


(async () => {

  // -> Open browser, inside the browser open page, then goto given URL in the page
  const browser = await puppeteer.launch({
    headless: true,
    args: [`--window-size=1280,720`],
    defaultViewport: {
      width: 1280,
      height: 720
    }
  });

  const page = await browser.newPage();
  await page.setExtraHTTPHeaders({ 'Accept-Language': 'en-GB' });
  
  for (k in file_array) {
    console.log("Print: " + k);
    await page.goto(file_array[k],{waitUntil: 'networkidle0',});
    
    await page.setGeolocation({latitude: 44.5, longitude: -89.5});
    await screenShot(page);

    await createDump(page);

    // arr = await getData(page);

    // await convertToCsv(arr);
  }
  // csv = new ObjectsToCsv(tocsv1);
  // await csv.toDisk(csv_path + 'file1.csv');
  
  // csv = new ObjectsToCsv(tocsv2);
  // await csv.toDisk(csv_path + 'file2.csv');

  // -> Close Browser
  await browser.close();
})();

async function screenShot(page) {
  // -> Get webpage height
  const bodyHandle = await page.$('body');
  const boundingBox = await bodyHandle.boundingBox();
  const height = boundingBox.height;

  //  -> Get multiple screenshots
  var i = 0;
  var sc_y = 0;
  while (sc_y < height) {
    await page.screenshot({
      path: sc_path + k + '_v' + i + '.png', clip: {
        x: 0, y: sc_y, width: page.viewport().width, height: page.viewport().height
      }
    })
    sc_y = sc_y + page.viewport().height
    i++
  }

  //  -> Get fullpage screenshot
  await page.screenshot({ path: sc_path + k + '.png', fullPage: true });

}

async function createDump(page) {
  //  -> Create Dump file
  try {

    html = await page.content();
    fs.writeFileSync(dump_path + k + '.html', html);

  } catch (err) {
    console.error(err);
    console.log("Error");

  }
}

async function getData(page) {
  arr = []
  title_xpath = []
  title = []
  links_xpath = []
  links = []
  details_xpath = []
  details = []

  section_path = "//h3/parent::a/ancestor::div[@data-hveid and @data-ved and @class='g tF2Cxc'] | //h3//parent::a/ancestor::div[@data-hveid and @data-ved]/parent::div[contains(@class,'g')][not(./ancestor::ul)]/parent::div[not(@id) or @id='rso']/div[contains(@class,'g')][not(./ancestor::ul)][not(@data-md)][not(descendant::table)][not(./g-card)][not(parent::div[contains(@class,'V3FYCf')])] | //h3//parent::a/ancestor::div[@data-hveid and @data-ved]/ancestor::div[@class='g']/parent::div[@data-hveid]//div[@data-hveid and @data-ved][not(./ancestor::ul)][not(parent::div[contains(@class,'g ')])] | //h3/parent::a/ancestor::div[contains(@class,'ZINbbc') and contains(@class,'uUPGi')]/parent::div | //a[contains(@href,'youtube')][./h3][not(ancestor::div[contains(@style,'display:none')])]/ancestor::div[not(@*)][parent::div[contains(@class,'g')]]"
  // wait for element defined by XPath appear in page
  // await page.waitForXPath(section_path);
  let section = await page.$x(section_path);

  for (let i = 0; i < section.length; i++) {
    i_plus_one = i + 1

    title_xpath[i] = "(" + section_path + ")[" + i_plus_one + "]//a/h3";
    links_xpath[i] = "(" + section_path + ")[" + i_plus_one + "]//a/@href";
    details_xpath[i] = "(" + section_path + ")[" + i_plus_one + "]/div[//a/h3]//div[(contains(@class,'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc'))]";

    // Get data
    title[i] = await page.$x(title_xpath[i]);
    links[i] = await page.$x(links_xpath[i]);
    details[i] = await page.$x(details_xpath[i]);

    // Process data
    for (let j = 0; j < title[i].length; j++) {
      title_str = await page.evaluate(tit => tit.textContent, title[i][j]);
    }

    for (let j = 0; j < links[i].length; j++) {
      links_str = await page.evaluate(lnk => lnk.textContent, links[i][j]);
    }

    for (let j = 0; j < details[i].length; j++) {
      details_str = await page.evaluate(det => det.textContent, details[i][j]);
    }


    data_arr = [title_str, links_str, details_str]

    data_arr.forEach(element => {
      if (!element) {
        element="N/A";
      }
    });
    
    // Process if empty dataSSSS
    if (!title_str) {
      title_str = "N/A";
    } if (!links_str) {
      links_str = "N/A";
    } if (!details_str) {
      details_str = "N/A";
    }

    arr.push({ "Title": title_str, "Link": links_str, "Details": details_str });
  }
  return arr

}

async function convertToCsv(arr) {

  tocsv_arr1 = [];
  tocsv_arr2 = [];
  keys = [];

  for (i = 0; i < arr.length; i++) {
    obj = arr[i];
    tocsv_arr1.push(obj);
  }
  tocsv1 = tocsv1.concat(tocsv_arr1);
  csv = new ObjectsToCsv(tocsv_arr1);
  await csv.toDisk(csv_path + k + 'a.csv');

  if (keys.length == 0) {
    for ( key in arr[0] ) {
      keys.push(key)
    }
  }

  for (i = 0; i < keys.length; i++){    
    for (j = 0; j < arr.length; j++){
      obj = { "Index": (parseInt(k) + 1) + '.' + (j + 1) + '.' + (i + 1), "Field": keys[i], "Value": arr[j][keys[i]] };
      tocsv_arr2.push(obj);
    }
  }

  tocsv2 = tocsv2.concat(tocsv_arr2);
  csv = new ObjectsToCsv(tocsv_arr2);
  await csv.toDisk(csv_path + k + 'b.csv');
}
