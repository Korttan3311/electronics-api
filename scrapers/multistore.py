from playwright.async_api import async_playwright

categories = {
    "Televisions": [
        {"url": "https://www.courts.com.sg/televisions", "store": "Courts"},
        {"url": "https://www.harveynorman.com.sg/televisions", "store": "Harvey Norman"}
    ]
}

async def scrape_category(playwright, cat_name, cat_data):
    products = []
    for item in cat_data:
        try:
            browser = await playwright.chromium.launch(headless=True, args=["--no-sandbox"])
            page = await browser.new_page()
            await page.goto(item["url"], timeout=60000)
            await page.wait_for_timeout(5000)

            # Logic for Courts
            if "courts" in item["url"]:
                tiles = await page.locator(".product-grid-item").all()
                for tile in tiles:
                    try:
                        name = await tile.locator(".product-title").text_content()
                        price = await tile.locator(".price-sales").text_content()
                        link = await tile.locator("a").get_attribute("href")
                        if name and price and link:
                            products.append({
                                "category": cat_name,
                                "name": name.strip(),
                                "price": price.strip(),
                                "link": "https://www.courts.com.sg" + link.strip(),
                                "store": item["store"]
                            })
                    except:
                        continue

            # Logic for Harvey Norman
            elif "harveynorman" in item["url"]:
                tiles = await page.locator(".product-item-info").all()
                for tile in tiles:
                    try:
                        name = await tile.locator(".product-item-name a").text_content()
                        price = await tile.locator(".price").text_content()
                        link = await tile.locator("a").get_attribute("href")
                        if name and price and link:
                            products.append({
                                "category": cat_name,
                                "name": name.strip(),
                                "price": price.strip(),
                                "link": link.strip(),
                                "store": item["store"]
                            })
                    except:
                        continue

            await browser.close()
        except Exception as e:
            print(f"Error scraping {item['url']}: {e}")
            continue
    return products

async def scrape_all_categories():
    async with async_playwright() as p:
        results = []
        for category, store_list in categories.items():
            result = await scrape_category(p, category, store_list)
            results.extend(result)
        return results
