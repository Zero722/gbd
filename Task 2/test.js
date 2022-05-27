// // Import Puppeteer
// const puppeteer = require('puppeteer');
// const ObjectsToCsv = require('objects-to-csv');


// (async () => {
//     // -> Open browser, inside the browser open page, then goto given URL in the page
//     const browser = await puppeteer.launch({ headless: false });
//     const page = await browser.newPage();
//     await page.goto('https://www.google.com/search?q=einstein&client=firefox-b-d&channel=nrow5&ei=bF6HYoe3L4O7mAW35YLYDQ&gs_ssp=eJzjYtfP1TfISq4wYPTiSM3MKy4BEgA5AQY0&oq=e&gs_lcp=Cgdnd3Mtd2l6EAEYADIECC4QQzIECC4QQzIECC4QQzIECAAQQzIECC4QQzIECAAQQzIHCC4Q1AIQQzIECAAQQzIECC4QQzIICAAQsQMQgwE6BwgAEEcQsAM6BwgAELADEEM6CggAEOQCELADGAE6DAguEMgDELADEEMYAkoECEEYAEoFCEASATFKBAhGGAFQ2ANY2ANgzxJoAnABeACAAbMBiAGzAZIBAzAuMZgBAKABAcgBEcABAdoBBggBEAEYCdoBBggCEAEYCA&sclient=gws-wiz');

//     await page.screenshot({ path: 'buddy-screenshot.png', fullPage: true })

//     // const links = await page.$$eval('.tF2Cxc .yuRUbf > a', (links) =>
//     //     links.map((link) => link.href)
//     // );
//     // console.log("Links:")
//     // console.log(links)

//     //start
//     // let title_rem = []
//     // let link_rem = []

//     // let title_all = []
//     let data_all = []


//     // wait for element defined by XPath appear in page
//     // await page.waitForXPath("//*[@id='rso']//a/h3");

//     // evaluate XPath expression of the target selector (it return array of ElementHandle)
//     // // let titlerem = await page.$x("//*[@id='rso']/div//li//a/h3");
//     // let titlerem = await page.$x("//*[@id='rso']/div//a/h3[not(ancestor::li) and not(ancestor::div/@class = 'Wt5Tfe')]");

    
//     // // prepare to get the textContent of the selector above (use page.evaluate)
//     // for (let i = 0; i < titlerem.length; i++) {
//     //     let title_rem_str = await page.evaluate(trem => trem.textContent, titlerem[i]);
//     //     title_rem.push(title_rem_str)
//     // }
//     // console.log("title_rem")

//     // console.log(title_rem)


//     // let linkrem = await page.$x("//*[@id='rso']/div//a[child::h3 and not(ancestor::li) and not(ancestor::div/@class = 'Wt5Tfe')]/@href");

    
//     // // prepare to get the textContent of the selector above (use page.evaluate)
//     // for (let i = 0; i < linkrem.length; i++) {
//     //     let link_rem_str = await page.evaluate(lrem => lrem.textContent, linkrem[i]);
//     //     link_rem.push(link_rem_str)
//     // }
//     // console.log("link_rem")

//     // console.log(link_rem)
//     // console.log(link_rem.length)



//     // let titleall = await page.$x("//*[@id='rso']/div//a/h3");
    
//     // console.log("apple")

//     // // prepare to get the textContent of the selector above (use page.evaluate)
//     // for (let i = 0; i < titleall.length; i++) {
//     //     let title_all_str = await page.evaluate(tall => tall.textContent, titleall[i]);
//     //     title_all.push(title_all_str)
//     // }
//     // console.log("title_all")

//     // console.log(title_all)


//     // let dataall = await page.$x("//*[@id='rso']//div//div[@class='VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc']");
//     section_path = "//h3/parent::a/ancestor::div[@data-hveid and @data-ved and @class='g tF2Cxc'] | //h3//parent::a/ancestor::div[@data-hveid and @data-ved]/parent::div[contains(@class,'g')][not(./ancestor::ul)]/parent::div[not(@id) or @id='rso']/div[contains(@class,'g')][not(./ancestor::ul)][not(@data-md)][not(descendant::table)][not(./g-card)][not(parent::div[contains(@class,'V3FYCf')])] | //h3//parent::a/ancestor::div[@data-hveid and @data-ved]/ancestor::div[@class='g']/parent::div[@data-hveid]//div[@data-hveid and @data-ved][not(./ancestor::ul)][not(parent::div[contains(@class,'g ')])] | //h3/parent::a/ancestor::div[contains(@class,'ZINbbc') and contains(@class,'uUPGi')]/parent::div | //a[contains(@href,'youtube')][./h3][not(ancestor::div[contains(@style,'display:none')])]/ancestor::div[not(@*)][parent::div[contains(@class,'g')]]"
//     await page.waitForXPath(section_path);
//     let section = await page.$x(section_path);
    
//     // prepare to get the textContent of the selector above (use page.evaluate)
//     // for (let i = 0; i < section.length; i++) {
//     //     console.log(section[i])
//     //     let data_all_str = await page.evaluate(dall => dall.textContent, section[i]);
//     //     data_all.push(data_all_str)
//     // }

//     title_xpath = []
//     title = []
//     links_xpath = []
//     links = []
//     details_xpath = []
//     details = []

//     for (let i = 0; i < section.length; i++) {
//         i_plus_one = i+1

//         title_xpath[i] = "(" + section_path + ")[" + i_plus_one  + "]//a/h3"; 
//         links_xpath[i] = "(" + section_path + ")[" + i_plus_one  + "]//a/@href";
//         details_xpath[i] = "(" + section_path + ")[" + i_plus_one  + "]/div[//a/h3]//div[(contains(@class,'VwiC3b yXK7lf MUxGbd yDYNvb lyLwlc'))]";

//         title[i] = await page.$x(title_xpath[i]);
//         links[i] = await page.$x(links_xpath[i]);
//         details[i] = await page.$x(details_xpath[i]);

//         for (let j = 0; j < title[i].length; j++) {
//             title_str = await page.evaluate(tit => tit.textContent, title[i][j]);
//             links_str = await page.evaluate(lnk => lnk.textContent, links[i][j]);
//             details_str = await page.evaluate(det => det.textContent, details[i][j]);
//         }
//         data_all.push({"Title" : title_str, "Link" : links_str, "Details": details_str})
//     }

//     // for (let i = 0; i < t.length; i++) {
//     //     let data_all_str = await page.evaluate(dall => dall.textContent, t[i]);
//     //     data_all.push(data_all_str)
//     // }
    
//     console.log("data_all")
//     console.log(data_all)

//     // let link1 = await page.$x(section[00] + "")

//     // tocsv_arr = []    

//     // for(i=0;i<5;i++){
//     //     a={"title": title_rem[i], "details": data_all[i], "link": link_rem[i] }
//     //     tocsv_arr.push(a)
//     // }

//     const csv = new ObjectsToCsv(data_all);
 
//     // Save to file:
//     await csv.toDisk('./test.csv');
    
//     // Return the CSV file as string:
//     // console.log(await csv.toString());
//     //end


//     // const datas = await page.$$eval('.tF2Cxc .VwiC3b.yXK7lf.MUxGbd.yDYNvb.lyLwlc', (datas) =>
//     //     datas.map((data) => data.textContent)
//     // );



//     //*[@id="rso"]/div[1]/div/div/div/div[1]/div/div[1]/a/h3


//     // console.log("Data:")
//     // console.log(datas)



//     // -> Close Browser
//     // await browser.close();
// })();





// const arr = ['a', 'b'];

// if (arr[3] !== undefined) {
//   console.log("apple")
// }
// else{
//     console.log("banana")
// }


a = " "
if(!a){
    console.log("Undefined")
}else{
    console.log("Done")
}