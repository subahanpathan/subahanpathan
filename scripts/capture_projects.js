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
  const browser = await chromium.launch();

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
    console.log(`Capturing ${project.name}...`);

    try {
      await page.goto(project.url, {
        waitUntil: "networkidle",
        timeout: 60000,
      });

      await page.waitForTimeout(3000);

      await page.screenshot({
        path: `dist/previews/${project.name}.png`,
        fullPage: false,
      });

      console.log(`✓ ${project.name}`);
    } catch (error) {
      console.error(`✗ ${project.name}`);
      console.error(error.message);
    }
  }

  await browser.close();
}

main();
