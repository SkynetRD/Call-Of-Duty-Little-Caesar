from flask import Flask, request, render_template, send_file
from PIL import Image, ImageDraw, ImageFont
import random
import datetime
import io

app = Flask(__name__)

# Definir los productos y precios de Little Caesar's
productos = {
    "Super Cheese": 139.00,
    "Caesar Wings": 85.00,
    "Refresco 600 ML": 18.00,
    "Crazy Bread": 40.00,
    "Italian Cheese Bread": 45.00,
    "Pepperoni Pizza": 149.00,
    "Hawaiian Pizza": 159.00,
    "Combo Familiar": 199.00
}

# Ruta para la página de inicio
@app.route('/')
def index():
    return render_template("index.html")

# Ruta para generar el recibo
@app.route('/generate_receipt', methods=['POST'])
def generate_receipt():
    idioma = request.form.get("idioma", "Español")
    moneda = request.form.get("moneda", "MXN")
    
    # Configuración del recibo
    total = 0
    items = []
    metodos_pago = ["Apple Pay", "Google Pay", "Tarjeta", "Cash"]
    num_productos = random.randint(3, len(productos))
    productos_aleatorios = random.sample(list(productos.items()), num_productos)

    for producto, precio in productos_aleatorios:
        cantidad = random.randint(1, 3)
        items.append((producto, cantidad, precio * cantidad))
        total += precio * cantidad
    
    subtotal = total
    impuestos = random.uniform(5, 15)
    total_con_impuestos = subtotal + (subtotal * impuestos / 100)
    metodo_pago = random.choice(metodos_pago)
    
    # Generar imagen del recibo
    img = Image.new('RGB', (300, 650), color='white')
    draw = ImageDraw.Draw(img)
    font_regular = ImageFont.load_default()

    y_offset = 20
    draw.text((150, y_offset), "Little Caesar's", font=font_regular, fill='black', anchor="mm")
    y_offset += 30
    draw.text((150, y_offset), f"Total: ${total_con_impuestos:.2f}", font=font_regular, fill='black', anchor="mm")
    y_offset += 30
    draw.text((150, y_offset), f"Método de pago: {metodo_pago}", font=font_regular, fill='black', anchor="mm")

    # Convertir imagen a bytes
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)

    return send_file(img_byte_arr, mimetype='image/png', as_attachment=True, download_name="receipt.png")

if __name__ == "__main__":
    app.run(debug=True)
