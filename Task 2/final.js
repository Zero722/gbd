// Import 
const puppeteer = require('puppeteer');
const fs = require('fs');
const ObjectsToCsv = require('objects-to-csv');

const sc_path = __dirname + '\\' + "screenshots" + '\\';
const csv_path = __dirname + '\\' + 'csv' + '\\';
const dom_path = __dirname + '\\' + 'dom' + '\\';

if (!fs.existsSync(sc_path)){
  fs.mkdirSync(sc_path);
}
if (!fs.existsSync(csv_path)){
  fs.mkdirSync(csv_path);
}
if (!fs.existsSync(dom_path)){
  fs.mkdirSync(dom_path);
}

var file_array = fs.readFileSync('file.txt').toString().split("\n");

(async () => {
  // -> Open browser, inside the browser open page, then goto given URL in the page
  const browser = await puppeteer.launch({
    headless: false,
    args: [`--window-size=1280,720`],
    defaultViewport: {
      width: 1280,
      height: 720
    }
  });

  const page = await browser.newPage();

  for (k in file_array) {
    console.log("Apple")
    console.log("Print: " + k);
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
    let title_arr = []
    let link_arr = []
    let details_arr = []

    // await page.waitForNavigation({timeout: 20000})
    // wait for element defined by XPath appear in page
    await page.waitForXPath("//*[@id='rso']/div//a/h3[not(ancestor::li) and not(ancestor::div/@class = 'Wt5Tfe')]");

    // evaluate XPath expression of the target selector (it return array)
    let titles = await page.$x("//*[@id='rso']/div//a/h3[not(ancestor::li) and not(ancestor::div/@class = 'Wt5Tfe')]");


    // prepare to get the textContent of the selector above (use page.evaluate)
    for (let i = 0; i < titles.length; i++) {
      let title = await page.evaluate(t => t.textContent, titles[i]);
      title_arr.push(title)
    }

    console.log("Title:")
    console.log(title_arr)

    let links = await page.$x("//*[@id='rso']/div//a[child::h3 and not(ancestor::li) and not(ancestor::div/@class = 'Wt5Tfe')]/@href");

    for (let i = 0; i < links.length; i++) {
      let link = await page.evaluate(l => l.textContent, links[i]);
      link_arr.push(link)
    }

    console.log("link_arr")
    console.log(link_arr)

    let details = await page.$x("//*[@id='rso']/div//div[//a/h3[not(ancestor::li) and not(ancestor::div/@class = 'Wt5Tfe')]]/div[(@class='Uroaid' or contains(@class,'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc')) and not(ancestor::li) and not(ancestor::div/@class = 'Wt5Tfe')]");

    // prepare to get the textContent of the selector above (use page.evaluate)
    for (let i = 0; i < details.length; i++) {
      let detail = await page.evaluate(d => d.textContent, details[i]);
      details_arr.push(detail)
    }
    console.log("details_arr")
    console.log(details_arr)

    arr = { "Title": title_arr, "Link": link_arr, "Detail": details_arr }

    if (title_arr.length == details_arr.length || title_arr.length == link_arr.length) {
      tocsv_arr1 = []
      tocsv_arr2 = []

      for (i = 0; i < title_arr.length; i++) {
        obj = { "Title": title_arr[i], "Details": details_arr[i], "Link": link_arr[i] }
        tocsv_arr1.push(obj)
      }
      csv = new ObjectsToCsv(tocsv_arr1);
      await csv.toDisk(csv_path + k + 'a.csv');

      x = 1
      for (key in arr) {
        for (i = 0; i < arr[key].length; i++) {
          obj = { "Index": k + '.' + (i + 1) + '.' + x, "Field": key, "Value": arr[key][i] }
          tocsv_arr2.push(obj)

        }
        x++
      }
      csv = new ObjectsToCsv(tocsv_arr2);
      await csv.toDisk(csv_path + k + 'b.csv');
    }
    else {
      console.log("Error")
    }

  }

  // -> Close Browser
  // await browser.close();
})();
