// Import 
const puppeteer = require('puppeteer');
const fs = require('fs');
const ObjectsToCsv = require('objects-to-csv');

const sc_path = __dirname + '\\' + "screenshots" + '\\';
const csv_path = __dirname + '\\' + 'csv' + '\\';
const dom_path = __dirname + '\\' + 'dom' + '\\';

if (!fs.existsSync(sc_path)) {
  fs.mkdirSync(sc_path);
}
if (!fs.existsSync(csv_path)) {
  fs.mkdirSync(csv_path);
}
if (!fs.existsSync(dom_path)) {
  fs.mkdirSync(dom_path);
}

var file_array = fs.readFileSync('file.txt').toString().split("\n");
tocsv1 = [];
tocsv2 = [];
(async () => {
  // -> Open browser, inside the browser open page, then goto given URL in the page
  const browser = await puppeteer.launch({
    headless: false,
    args: [`--window-size=1280,720`,'--lang=en-GB,en'],
    defaultViewport: {
      width: 1280,
      height: 720
    } 
  });

  const page = await browser.newPage();
  await page.setExtraHTTPHeaders({'Accept-Language': 'en-GB'});

  for (k in file_array) {
    // console.log("Apple")
    // console.log("Print: " + k);
    await page.goto(file_array[k])

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

    //  -> Create DOM file
    try {
      const cdp = await page.target().createCDPSession();
      const { data } = await cdp.send('Page.captureSnapshot', { format: 'mhtml' });
      fs.writeFileSync(dom_path + k + '.mhtml', data);

    } catch (err) {
      console.error(err);
    }

    //start
    arr = []
    title_xpath = []
    title = []
    links_xpath = []
    links = []
    details_xpath = []
    details = []

    // await page.waitForNavigation({timeout: 20000})
    // wait for element defined by XPath appear in page
    section_path = "//h3/parent::a/ancestor::div[@data-hveid and @data-ved and @class='g tF2Cxc'] | //h3//parent::a/ancestor::div[@data-hveid and @data-ved]/parent::div[contains(@class,'g')][not(./ancestor::ul)]/parent::div[not(@id) or @id='rso']/div[contains(@class,'g')][not(./ancestor::ul)][not(@data-md)][not(descendant::table)][not(./g-card)][not(parent::div[contains(@class,'V3FYCf')])] | //h3//parent::a/ancestor::div[@data-hveid and @data-ved]/ancestor::div[@class='g']/parent::div[@data-hveid]//div[@data-hveid and @data-ved][not(./ancestor::ul)][not(parent::div[contains(@class,'g ')])] | //h3/parent::a/ancestor::div[contains(@class,'ZINbbc') and contains(@class,'uUPGi')]/parent::div | //a[contains(@href,'youtube')][./h3][not(ancestor::div[contains(@style,'display:none')])]/ancestor::div[not(@*)][parent::div[contains(@class,'g')]]"
    await page.waitForXPath(section_path);
    let section = await page.$x(section_path);

    for (let i = 0; i < section.length; i++) {
      i_plus_one = i + 1

      title_xpath[i] = "(" + section_path + ")[" + i_plus_one + "]//a/h3";
      links_xpath[i] = "(" + section_path + ")[" + i_plus_one + "]//a/@href";
      details_xpath[i] = "(" + section_path + ")[" + i_plus_one + "]/div[//a/h3]//div[(contains(@class,'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc'))]";

      title[i] = await page.$x(title_xpath[i]);
      links[i] = await page.$x(links_xpath[i]);
      details[i] = await page.$x(details_xpath[i]);

      for (let j = 0; j < title[i].length; j++) {
        title_str = await page.evaluate(tit => tit.textContent, title[i][j]);
        links_str = await page.evaluate(lnk => lnk.textContent, links[i][j]);
        details_str = await page.evaluate(det => det.textContent, details[i][j]);
      }

      if(!title_str){
        title_str = "N/A";
      }if(!links_str){
        links_str = "N/A";
      }if(!details_str){
        details_str = "N/A";
      }
 
      arr.push({ "Title": title_str, "Link": links_str, "Details": details_str });
    }
    console.log(arr);


    tocsv_arr1 = [];
    tocsv_arr2 = [];

    for (i = 0; i < arr.length; i++) {
      obj = { "Title": arr[i]["Title"], "Details": arr[i]["Details"], "Link": arr[i]["Link"] };
      tocsv_arr1.push(obj);
    }
    tocsv1 = tocsv1.concat(tocsv_arr1);
    csv = new ObjectsToCsv(tocsv_arr1);
    await csv.toDisk(csv_path + k + 'a.csv');

    for (i = 0; i < arr.length; i++) {
      j = 1
      for (key in arr[i]) {
        obj = { "Index": k + '.' + (i + 1) + '.' + j, "Field": key, "Value": arr[i][key] };
        tocsv_arr2.push(obj);
        j++;
      }
    }
    tocsv2 = tocsv2.concat(tocsv_arr2);
    csv = new ObjectsToCsv(tocsv_arr2);
    await csv.toDisk(csv_path + k + 'b.csv');
  }
  csv = new ObjectsToCsv(tocsv1);
  await csv.toDisk(csv_path + 'file1.csv');

  csv = new ObjectsToCsv(tocsv2);
  await csv.toDisk(csv_path + 'file2.csv');

  // -> Close Browser
  // await browser.close();
})();
