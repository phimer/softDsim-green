async (page) => {
  // Go to the url passed to the command line (see below)
  console.log(page)
  await page.goto("", { waitUntil: "networkidle" });
  await page.waitForTimeout(1000); // Wait for 3 seconds

  // Click Login
  await page.locator('.css-ot4ipg').click();
  await page.waitForTimeout(1000);

  // Enter username and password
  await page.locator('.css-216twa').fill('admin');
  await page.locator('.css-i9hn22').fill('admin');

  // Accept terms
  await page.locator('.css-xxkadm').click();
  await page.waitForTimeout(1000);

  // Click login
  await page.locator('.css-1en85ns').click();
  await page.waitForTimeout(1000);

  // now all scenarios get loaded

  await page.waitForNetworkIdle(); // Wait for every request to be answered - like a normal user would do
  await page.waitForTimeout(8000)
};
