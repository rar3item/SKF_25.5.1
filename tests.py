from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

driver = webdriver.Chrome('/Usr/local/bin/chromedriver.exe')
driver.implicitly_wait(10)

@pytest.fixture(autouse=True)
def testing():
   driver.get('http://petfriends.skillfactory.ru/login')
   driver.find_element(By.ID, 'email').send_keys('login')
   driver.find_element(By.ID, 'pass').send_keys('pass')
   driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
   WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//button[text()='Выйти']")))

def test_get_number_my_pets():
    driver.find_element(By.CSS_SELECTOR, 'a[href$="/my_pets"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='task3 fill']")))
    pets_count = driver.find_element(By.XPATH, 'html[1]/body[1]/div[1]/div[1]/div[1]').text[20]
    cards = driver.find_elements(By.CSS_SELECTOR, 'th>img')
    assert int(len(cards)) == int(pets_count)

def test_get_img_my_pets():
    driver.find_element(By.CSS_SELECTOR, 'a[href$="/my_pets"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='task3 fill']")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'th>img')))
    cards = driver.find_elements(By.CSS_SELECTOR, 'th>img')
    pets_count = driver.find_element(By.XPATH, 'html[1]/body[1]/div[1]/div[1]/div[1]').text[20]
    count_img = 0
    for i in range(len(cards)):
        if cards[i].get_attribute('src') != "":
            count_img += 1
    assert count_img >= int(pets_count)//2

#проверям что у всех питомцев есть имя, возраст и порода.
def test_get_inf_my_pets():
    driver.find_element(By.CSS_SELECTOR, 'a[href$="/my_pets"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='task3 fill']")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr>td')))
    cols = driver.find_elements(By.CSS_SELECTOR, 'tr>td')
    for i in range(len(cols)):
        assert cols[i].text != ''

#проверям что у всех питомцев разные имена.
def test_name_my_pets_is_diff():
    driver.find_element(By.CSS_SELECTOR, 'a[href$="/my_pets"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='task3 fill']")))
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'tr>td')))
    cols = driver.find_elements(By.CSS_SELECTOR, 'tr>td')
    names = []
    counter = 0
    for i in range(0, len(cols), 4):
        names.append(cols[i].text)
        counter += 1
    names = set(names)
    assert len(names) == counter


