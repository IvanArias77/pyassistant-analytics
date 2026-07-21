const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();
  const htmlFile = process.argv[2];
  const pdfFile = process.argv[3];
  const fileUrl = 'file:///' + path.resolve(htmlFile).replace(/\\/g, '/');
  console.log('Opening:', fileUrl);
  await page.goto(fileUrl, { waitUntil: 'networkidle' });
  await page.pdf({
    path: pdfFile,
    format: 'Letter',
    margin: { top: '0.4in', bottom: '0.4in', left: '0.4in', right: '0.4in' },
    printBackground: true
  });
  await browser.close();
  console.log('PDF created:', pdfFile);
})();