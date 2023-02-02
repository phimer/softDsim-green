async (page) => {
    // Go to the url passed to the command line (see below)
    console.log(page)
    await page.goto("", { waitUntil: "networkidle" });
    await page.waitForTimeout(1000); // Wait for 3 seconds
  
  };
  