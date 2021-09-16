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
        # await page.content() raise Error : Execution context was destroyed, most likely because of a navigation.
        # I am guessing because the html contains meta http-equiv="refresh"
        page_source = await page.content()
        await browser.close()
        return page_source
        
if __name__ == "__main__":
    """
    <html>
    <head>
            <meta http-equiv="refresh" content="0; url=https://www.debian.org/blends/">
    </head>
    <body>
            <h1>Debian Pure Blends</h1>
    </body>
    </html>
    """
    url = "https://playwright.neocities.org/"
    loop = asyncio.get_event_loop()
    ret = loop.run_until_complete(async_get_page_source(url=url))
    print(ret)
