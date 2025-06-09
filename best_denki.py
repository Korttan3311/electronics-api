from playwright.async_api import async_playwright

async def scrape_best_denki():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.courts.com.sg/televisions", timeout=60000)
        await page.wait_for_timeout(5000)

        items = await page.locator(".product-tile").all()
        products = []

        for item in items:
            try:
                name = await item.locator(".product-title").text_content()
                price = await item.locator(".product-price").text_content()
                link = await item.locator("a").get_attribute("href")
                if name and price and link:
                    products.append({
                        "name": name.strip(),
                        "price": price.strip(),
                        "link": f"https://www.courts.com.sg{link.strip()}",
                        "store": "Courts"
                    })
            except:
                continue

        await browser.close()
