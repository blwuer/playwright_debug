from playwright.async_api import async_playwright
import asyncio

async def async_get_page_source(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        
        page.on("request", lambda request: print(">>", request.method, request.url))
        page.on("response", lambda response: print("<<", response.status, response.url))

        await page.goto(url)
        page_source = await page.content()
        await browser.close()
        return page_source

if __name__ == "__main__":
    url = "https://playwright.neocities.org/"
    loop = asyncio.get_event_loop()
    ret = loop.run_until_complete(async_get_page_source(url=url))
    print(ret)