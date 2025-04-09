from flask import Flask, request, render_template, send_file
import pandas as pd
import time
import os
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # ✅ esto es lo nuevo
import shutil

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        df_original = pd.read_excel(filepath, usecols=[0, 1, 2, 3, 4, 5, 6],
                                    names=["Descripción", "Cód. Barras", "Referencia", "CONSULTA", "NETO", "LINEA", "PROVEEDOR"],
                                    skiprows=1)
        df = df_original.copy()
        df["Descripción_Carulla"] = None
        df["Precio_Carulla"] = None

        # ✅ Configuración de Selenium (Chrome headless sin rutas fijas)
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920x1080')
        options.binary_location = "/opt/google/chrome/google-chrome"


        # ✅ Usar webdriver-manager correctamente
        service = ChromeService(executable_path="/usr/bin/chromedriver")
        driver = webdriver.Chrome(service=service, options=options)

        driver.get('https://www.carulla.com')

        for index, row in df.iterrows():
            codigo_barras = str(row["Cód. Barras"]).strip()
            print(f"🔍 Buscando código de barras: {codigo_barras}")

            try:
                search_field = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/header/section/div/div[1]/div[2]/form/input'))
                )
                search_field.clear()
                time.sleep(2)

                for _ in range(21):
                    search_field.send_keys(Keys.BACKSPACE)
                    time.sleep(0.5)

                search_field.send_keys(codigo_barras)
                search_field.send_keys(Keys.ENTER)
                time.sleep(1)

                WebDriverWait(driver, 22).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[2]/ul/li/article/div[1]/div[2]/a/div/p'))
                )
                time.sleep(1)

                name = driver.find_element(By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[2]/ul/li/article/div[1]/div[2]/a/div/h3')
                price = driver.find_element(By.XPATH, '//*[@id="__next"]/main/section[3]/div/div[2]/div[2]/div[2]/ul/li/article/div[1]/div[2]/div/div/div[2]/p')

                df.at[index, "Descripción_Carulla"] = name.text
                df.at[index, "Precio_Carulla"] = price.text
                print(f"✅ Producto encontrado ({codigo_barras}): {name.text} | Precio: {price.text}")

            except TimeoutException:
                df.at[index, "Descripción_Carulla"] = "No encontrado"
                df.at[index, "Precio_Carulla"] = "No encontrado"
                print(f"❌ No se encontró el código de barras: {codigo_barras}")

            except Exception as e:
                df.at[index, "Descripción_Carulla"] = "Error"
                df.at[index, "Precio_Carulla"] = "Error"
                print(f"⚠️ Error al buscar '{codigo_barras}': {str(e)}")

            time.sleep(2)

        driver.quit()

        output = BytesIO()
        df.to_excel(output, index=False)
        output.seek(0)

        return send_file(output,
                         download_name="resultado_carulla.xlsx",
                         as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
