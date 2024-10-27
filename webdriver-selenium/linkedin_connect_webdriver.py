from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time

class LinkedInXPaths:
    # LoginPage
    LOGIN_TEXT = '//*[@id="username"]'
    PWD_TEXT = '//*[@id="password"]'

    # ConnectPage
    # MAIN_BLUE_BUTTON = '/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[3]/div/button/span'
    MAIN_BLUE_BUTTON = '//*[contains(@class, "artdeco-button--primary")]'
    
    
    NIVEL_CONEXAO = '//*[contains(@class, "mt2")]'
    # NIVEL_CONEXAO = '/html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]'
    #                  /html/body/div[4]/div[3]/div/div/div[2]/div/div/main/section[1]/div[2]/div[2]/div[1]/div[1]

    ADD_NOTE = '/html/body/div[3]/div/div/div[3]/button[1]/span'
    CONNECT_TEXT_MESSAGE = '//*[@id="custom-message"]'
    ADD_NOTE_SEND_BUTTON = '/html/body/div[3]/div/div/div[3]/button[2]/span'

    WAIT = 3  # Em segundos

    @staticmethod
    def type_text_element(driver, xpath, text):
        element = driver.find_element(By.XPATH, xpath)
        time.sleep(LinkedInXPaths.WAIT)
        element.send_keys(text)
        time.sleep(LinkedInXPaths.WAIT)
        return element
    
    @staticmethod
    def click_button(driver, xpath):
        button = driver.find_element(By.XPATH, xpath)
        button.click()
        time.sleep(LinkedInXPaths.WAIT)
        return button

class LinkedIn:
    def __init__(self, driver):
        # Armazena o valor do driver passado no construtor
        self.driver = driver

    # Método de exemplo que utiliza o driver
    def login(self):
        self.driver.get('https://www.linkedin.com/login')
        LinkedInXPaths.type_text_element(self.driver, LinkedInXPaths.LOGIN_TEXT, 'fabiopereira.me@gmail.com')
        pwd = LinkedInXPaths.type_text_element(self.driver, LinkedInXPaths.PWD_TEXT, 'LINKEDIN_PASSWORD')
        pwd.send_keys(Keys.RETURN)
        time.sleep(3)

    def find_type_and_wait(self, xpath, text):
        element = driver.find_element(By.XPATH, xpath)
        element.send_keys(text)
        time.sleep(5)
        return element
    
    def find_click_and_wait(self, xpath):
        button = driver.find_element(By.XPATH, xpath)
        return self.click_and_wait(self, button)

    def click_button_and_wait(self, button):
        button.click()
        time.sleep(LinkedInXPaths.WAIT)
        return button
    
    def check_exists_by_xpath(self,xpath):
        try:
            self.driver.find_element(By.XPATH,xpath)
        except NoSuchElementException:
            return False
        return True
    
    def check_exists(self, element,driver,sel):
        try:
            self.driver.find_element(element,sel)
        except NoSuchElementException:
            return False
        return True

    def connect(self, profile):        
        driver = self.driver
        driver.get(profile)
        xpath="//main[@id='main']/div[1]/section[1]/div[2]/div[3]/div[1]/button[1]/span[1]"
        if self.check_exists_by_xpath(xpath):
                driver.find_element(By.XPATH,xpath).click()
                if self.check_exists(By.ID,driver,"custom-message"):
                    driver.find_element(By.ID,"custom-message").send_keys('Oi, estamos juntos no HJ Conference, vamos conectar por aqui?')
                    driver.find_element(By.CSS_SELECTOR,"[aria-label='Send now']").click()
        else:
            driver.find_element(By.CSS_SELECTOR,"[aria-label='More actions']").click()
            if self.check_exists(By.CSS_SELECTOR,driver,"[data-control-name='follow']"):
                driver.find_element(By.CSS_SELECTOR,"[data-control-name='follow']").click()
        time.sleep(LinkedInXPaths.WAIT)
        print("Done")

    def connect1(self, profile):
        driver = self.driver
        driver.get(profile)
        time.sleep(LinkedInXPaths.WAIT)
        nivel_conexao = driver.find_element(By.XPATH, LinkedInXPaths.NIVEL_CONEXAO)
        print(nivel_conexao.text)
        if "1st degree" in nivel_conexao.text:
            print("Já é conexão de 1st nível")
        else:
            print("Não é conexão, vamos conectar")
            main_blue_button = driver.find_element(By.XPATH, LinkedInXPaths.MAIN_BLUE_BUTTON)
            print(main_blue_button.text)
            # print("Encontrou botão com texto:", main_blue_button.text)
            # main_blue_tag = main_blue_button.find_element(By.TAG_NAME, "span")
            # button_text = main_blue_tag.get_attribute('innerHTML')
            # if "Connect" in button_text:
            self.click_button_and_wait(main_blue_button)
            self.find_click_and_wait(LinkedInXPaths.ADD_NOTE)
            self.find_type_and_wait(LinkedInXPaths.CONNECT_TEXT_MESSAGE, 'Oi, estamos juntos no HJ Conference, vamos conectar por aqui?')
            self.find_click_and_wait(LinkedInXPaths.ADD_NOTE_SEND_BUTTON)
            # else:
                # print("Botão não tem texto Connect, não vou conectar")
        

# from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome()
linkedin = LinkedIn(driver)
linkedin.login()
linkedin.connect('https://www.linkedin.com/in/brunoperissotti/')
driver.quit()


