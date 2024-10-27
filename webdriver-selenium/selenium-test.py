from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configure o caminho para o ChromeDriver
chrome_driver_path = '/path/to/chromedriver'  # Altere para o caminho do seu ChromeDriver

# Inicializa o navegador
driver = webdriver.Chrome(executable_path=chrome_driver_path)

try:
    # Abre o Google
    driver.get("https://www.google.com")

    # Espera a página carregar completamente
    time.sleep(2)  # Aguarda 2 segundos

    # Encontra a barra de pesquisa
    search_box = driver.find_element(By.NAME, "q")

    # Digita o termo de pesquisa e envia
    search_box.send_keys("OpenAI GPT-4")
    search_box.send_keys(Keys.RETURN)

    # Espera a página de resultados carregar
    time.sleep(2)  # Aguarda 2 segundos

    # Realiza mais ações conforme necessário
    # Exemplo: clicar no primeiro link
    first_result = driver.find_element(By.CSS_SELECTOR, "h3")
    first_result.click()

    # Espera um pouco antes de fechar
    time.sleep(5)  # Aguarda 5 segundos para ver a página

finally:
    # Fecha o navegador
    driver.quit()
pi