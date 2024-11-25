const { chromium } = require('playwright');

(async () => {
    const userDataDir = './user-data'; // Directory for storing user data

    // Launch a persistent browser context
    const browser = await chromium.launchPersistentContext(userDataDir, {
        headless: false, // Run with GUI (set to true for headless mode)
    });

    // Open a new page or use the first page in the persistent context
    let page;
    if (browser.pages().length > 0) {
        page = browser.pages()[0]; // Use the first existing page
    } else {
        page = await browser.newPage(); // Create a new page if none exist
    }
})