var webdriver = require('selenium-webdriver');
var driver = new webdriver.Builder().forBrowser('chrome').build();

driver.get("http://127.0.0.1:8000");
driver.findElement(webdriver.By.name('username')).sendKeys('Nirvik');
driver.findElement(webdriver.By.name('password')).sendKeys('cs561admin');
driver.findElement(webdriver.By.name('Submit')).click();
driver.findElement(webdriver.By.linkText('Timer')).click();
driver.findElement(webdriver.By.id('playpause')).click();
driver.findElement(webdriver.By.id('stopbutton')).click();
driver.findElement(webdriver.By.linkText('Timer')).click();
driver.findElement(webdriver.By.name('course')).click();

driver.quit();
