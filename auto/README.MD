# Playwright

## Installation
pip install --upgrade pip

pip install playwright

playwright install
    C:\Users\zibang.com\AppData\Local\ms-playwright\ffmpeg-100
    C:\Users\zibang.com\AppData\Local\ms-playwright\firefox-1313
    C:\Users\zibang.com\AppData\Local\ms-playwright\webkit-1596

## Usage
## Inspector
## Trace Viewer


## Other
enable-automation
useAutomationExtension
https://bot.sannysoft.com/

Playwritght 跳过检测
- args=['--disable-blink-features=AutomationControlled'] 

data = { 'text': 'some data', 'value': 1 }
# Pass |data| as a parameter.
result = await page.evaluate("""data => {
  window.myApp.use(data)
}""", data)


browser.add_init_script(
                script='!1===navigator.webdriver||void 0===navigator.webdriver||delete Object.getPrototypeOf(navigator).webdriver')
https://dcinfos-cache.abtasty.com/v1/geoip
https://dcinfos-cache.abtasty.com/v1/ua-parser