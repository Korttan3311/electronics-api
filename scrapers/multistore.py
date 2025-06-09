from playwright.async_api import async_playwright

categories = {
    "Televisions": [
        {"url": "https://www.courts.com.sg/televisions", "store": "Courts"},
        {"url": "https://www.harveynorman.com.sg/televisions", "store": "Harvey Norman"},
        {"url": "https://www.parisilk.com/televisions", "store": "Parisilk"}
    ],
    "Phones": [
        {"url": "https://www.courts.com.sg/mobile-phones", "store": "Courts"},
        {"url": "https://www.harveynorman.com.sg/mobile-phones.html", "store": "Harvey Norman"}
    ],
    "Routers": [
        {"url": "https://www.courts.com.sg/networking/network-routers", "store": "Courts"},
        {"url": "https://www.harveynorman.com.sg/computing/computer-accessories/networking.html", "store": "Harvey Norman"}
    ],
    "Audio": [
        {"url": "https://www.audiohouse.com.sg/audio", "store": "Audio House"},
        {"url": "https://www.courts.com.sg/audio", "store": "Courts"}
    ],
    "Kitchen Appliances": [
        {"url": "https://www.gaincity.com/kitchen-appliances", "store": "Gain City"},
        {"url": "https://www.bestdenki.com.sg/kitchen-appliances", "store": "Best Denki"}
    ],
    "Home Appliances": [
        {"url": "https://www.gaincity.com/home-appliances", "store": "Gain City"},
        {"url": "https://www.bestdenki.com.sg/home-appliances", "store": "Best Denki"}
    ]
}

async def scrape_category(playwright, cat_name, cat_data):
    products = []
    for item in cat_data:
        try:
            browser = await playwright.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(item["url"], timeout=60000)
            await page.wait_for_timeout(5000)

            tiles = await page.locator(".product-tile").all()
            for tile in tiles:
                try:
                    name = await tile.locator(".product-title").text_content()
                    price = await tile.locator(".product-price").text_content()
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
        except:
            continue
    return products

async def scrape_all_categories():
    async with async_playwright() as p:
        results = []
        for category, store_list in categories.items():
            result = await scrape_category(p, category, store_list)
            results.extend(result)
        return results
