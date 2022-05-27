

const puppeteer = require('puppeteer');
const fs = require('fs');

(async function main() {
  try {
    const browser = await puppeteer.launch();
    const [page] = await browser.pages();

    await page.goto('https://www.google.com/search?q=einstein&source=hp&ei=7xuCYt2LEsadseMP_5-cmAE&iflsig=AJiK0e8AAAAAYoIp__iDDzMARSR8YP3QHfeCF2MxdRpC&gs_ssp=eJzjYtfP1TfISq4wYPTiSM3MKy4BEgA5AQY0&oq=eins&gs_lcp=Cgdnd3Mtd2l6EAMYADIHCC4QsQMQQzIECC4QQzIECAAQQzIECAAQQzIFCAAQgAQyCwguEIAEEMcBEK8BMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoUCAAQ6gIQtAIQigMQtwMQ1AMQ5QI6CAgAELEDEIMBOgsILhCABBCxAxCDAToLCAAQgAQQsQMQgwE6BwgAELEDEEM6DgguEIAEELEDEMcBEK8BOggILhCABBCxAzoICAAQgAQQsQM6BQguEIAEUKsHWJ4MYPgaaAFwAHgAgAGwAYgBkgWSAQMwLjSYAQCgAQGwAQo&sclient=gws-wiz');

    const cdp = await page.target().createCDPSession();
    const { data } = await cdp.send('Page.captureSnapshot', { format: 'mhtml' });
    fs.writeFileSync('page.mhtml', data);

    await browser.close();
  } catch (err) {
    console.error(err);
  }
})();