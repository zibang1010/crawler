//检测模拟浏览器
webdriver = window.navigator.webdriver;
if (webdriver) {
    console.log('模拟浏览器');
} else {
    console.log('正常浏览器')
}