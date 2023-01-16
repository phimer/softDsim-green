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

  // Select first Scenario
  await page.locator('xpath=/html/body/div[1]/div/div[2]/div[2]/div/div/table/tbody/tr[1]/td[2]/button').click();
  await page.waitForTimeout(1000);

  // Click Start Simulation
  await page.locator('.css-8pcd7y').click();
  await page.waitForTimeout(5000);

  // Click Close story
  await page.locator('.css-8pcd7y').click();
  await page.waitForTimeout(1000);

  // Click Waterfall
  await page.locator('xpath=/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/button[1]').click();
  await page.waitForTimeout(500);
  
  // Click Next
  await page.locator('.css-bxzc6t').click();
  await page.waitForTimeout(5000);
  
  // Click on question answers and click next
  await page.locator('xpath=/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[1]/div/div/div/label[1]/span[1]').click();
  await page.locator('xpath=/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div/div/div/label[1]/span[1]').click();
  await page.locator('.css-bxzc6t').click();
  await page.waitForTimeout(5000);
  
  // Click on question answers and click next
  await page.locator('xpath=/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/label[1]/span[1]').click();
  await page.locator('xpath=/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/label[2]/span[1]').click();
  await page.locator('.css-bxzc6t').click();
  await page.waitForTimeout(5000);


  // Close story
  await page.locator('.css-8pcd7y').click();
  await page.waitForTimeout(1000);


  const play_one_week = async (
    open_employees_section=false,
    number_of_devs_to_add = 0,
    drag_slider_to = 40
    ) => {

    // Select employees (only needed the first time)
    if (open_employees_section) { await page.locator('.css-103jld').click() };
    // Add senior developers
    for (i = 0; i < number_of_devs_to_add; i++) {
      await page.locator('xpath=/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[1]/div/div/button[2]').click();
    }
    // Add junior developers
    for (i = 0; i < number_of_devs_to_add; i++) {
      await page.locator('xpath=/html/body/div[1]/div/div[2]/div/div/div/div[3]/div/div[1]/div[2]/div[2]/div/div/button[2]').click();
    }

    await page.waitForTimeout(500);

    // Drag Training slider
    let slider_handle = await page.locator('.css-1sth7vg').first()
    slider_handle.dragTo(slider_handle, {
      force: true,
      targetPosition: {
        x: drag_slider_to,
        y: 0
      }
    });

    await page.waitForTimeout(500);

    //Drag Meetings slider
    slider_handle = await page.locator('.css-1sth7vg').last()
    slider_handle.dragTo(slider_handle, {
      force: true,
      targetPosition: {
        x: drag_slider_to,
        y: 0
      }
    });

    await page.waitForTimeout(500);

    // Click Next Week
    await page.locator('.css-bxzc6t').click()
  }

  await play_one_week(
    open_employees_section=true,
    number_of_devs_to_add = 40
  )
  await page.waitForTimeout(5000);

  await play_one_week(
    open_employees_section=false,
    number_of_devs_to_add = 40
  )
  await page.waitForTimeout(5000);

  await play_one_week(
    open_employees_section=false,
    number_of_devs_to_add = 40
  )
  await page.waitForTimeout(5000);

  

  // Click Deliver Project
  await page.locator('.css-rp7iz6').click()
  await page.waitForTimeout(5000);
  
  // Click first answer on final question
  await page.locator('.css-1rggdzb').first().click()
  // Click Next
  await page.locator('.css-bxzc6t').first().click()

  await page.waitForTimeout(6000);
  
  // Click Finish
  await page.locator('.css-fus2ix').first().click()
  
  

  //await page.scrollToElement("footer"); // Scroll to the bottom of the page (change the element name depending on your markup)
  await page.waitForNetworkIdle(); // Wait for every request to be answered - like a normal user would do
};
