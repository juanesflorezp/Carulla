from flask import Flask, request, render_template, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["file"]
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        df = pd.read_excel(filepath)

        # Configurar Selenium con opciones para Render
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = "/usr/bin/google-chrome"

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        nombres = []
        precios = []

        for codigo in df['codigo']:
            url = f"https://www.carulla.com/s?q={codigo}"
            driver.get(url)
            driver.implicitly_wait(5)

            try:
                nombre = driver.find_element("css selector", ".product__item__name").text
                precio = driver.find_element("css selector", ".price__integer").text
            except:
                nombre = "No encontrado"
                precio = "No encontrado"

            nombres.append(nombre)
            precios.append(precio)

        driver.quit()

        df['nombre'] = nombres
        df['precio'] = precios
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], "resultado.xlsx")
        df.to_excel(output_path, index=False)

        return send_file(output_path, as_attachment=True)

    return '''
        <html>
            <body>
                <h2>Sube tu archivo Excel con códigos</h2>
                <form method="POST" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit">
                </form>
            </body>
        </html>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
