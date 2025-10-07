// render_pdf.js
import puppeteer from "puppeteer";

const browser = await puppeteer.launch();
const page = await browser.newPage();

// Change the path if your HTML is in a different folder
await page.goto(`file://${process.cwd()}/templates/payslip.html`, { waitUntil: "networkidle0" });

await page.pdf({
  path: "demo_output/payslip.pdf",
  format: "A4",
  printBackground: true
});

await browser.close();
console.log("✅ PDF generated: demo_output/payslip.pdf");