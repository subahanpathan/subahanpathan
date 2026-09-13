const { chromium } = require("playwright");
const fs = require("fs");

const projects = [
  {
    name: "erp",
    url: "https://erp-topaz-three.vercel.app/",
  },
  {
    name: "subverse",
    url: "https://sub-verse-six.vercel.app/",
  },
  {
    name: "meter-flow",
    url: "https://meter-flow-mu.vercel.app/",
  },
  {
    name: "bug-tracker",
    url: "https://bug-tracker-omega-three.vercel.app/",
  },
  {
    name: "nexus-ai",
    url: "https://nexus-ai-inky-iota.vercel.app/",
  },
  {
    name: "signflow",
    url: "https://signflow-olive-three.vercel.app/",
  },
];

async function main() {
  console.log("Starting project preview generation...");

  const browser = await chromium.launch({
    headless: true,
  });

  const context = await browser.newContext({
    viewport: {
      width: 1440,
      height: 900,
    },
    deviceScaleFactor: 1,
  });

  const page = await context.newPage();

  fs.mkdirSync("dist/previews", {
    recursive: true,
  });

  for (const project of projects) {
    console.log(`\nCapturing: ${project.name}`);
    console.log(`URL: ${project.url}`);

    try {
      await page.goto(project.url, {
        waitUntil: "domcontentloaded",
        timeout: 90000,
      });

      // Give the application time to render.
      await page.waitForTimeout(5000);

      await page.screenshot({
        path: `dist/previews/${project.name}.png`,
        fullPage: false,
      });

      console.log(`✓ Preview generated: ${project.name}.png`);
    } catch (error) {
      console.error(`✗ Failed: ${project.name}`);
      console.error(error.message);
    }
  }

  await browser.close();

  console.log("\nPreview generation completed.");
}

main();
