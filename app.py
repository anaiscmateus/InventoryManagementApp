from flask import Flask, request, render_template, flash
import gspread
from random import randrange

# ACCESS GOOGLE SHEET
gc = gspread.service_account()
sh = gc.open("Clothing Store Inventory")
wk = sh.worksheet("prod_inventory")

# CLASSES
class Product():

    def __init__(self, column=1):
        self.column = column

    # METHODS
    def get_col_values(self):
        return wk.col_values(self.column)

    def find_next_row(self):
        rows = self.get_col_values()
        return str(len(rows) + 1)

    def gen_prod_id(self):
        prod_ids = self.get_col_values()
        return int(prod_ids[-1]) + 1

    def gen_sku(self, size):
        numbers = ''
        for num in range(0,8):
            num = str((randrange(0,10)))
            numbers += num
        return f'{numbers}_{size}'

    def find_row_num(self, prod_id):
        cell = wk.find(prod_id)
        return cell.row

    def add_product(self, prod_id, name, category, brand, price, qty, size):
        full_sku = self.gen_sku(size)
        row_num = self.find_next_row()
        wk.update(f'A{row_num}', prod_id)
        wk.update(f'B{row_num}', name)
        wk.update(f'C{row_num}', category)
        wk.update(f'D{row_num}', brand)
        wk.update(f'E{row_num}', price)
        wk.update(f'F{row_num}', qty)
        wk.update(f'G{row_num}', full_sku)


    def update_product(self, prod_id, category, brand, price, qty):
        row_num = self.find_row_num(prod_id)
        wk.update(f'C{row_num}', category)
        wk.update(f'D{row_num}', brand)
        wk.update(f'E{row_num}', price)
        wk.update(f'F{row_num}', qty)

prod = Product()

# DICTIONARIES  
new_prod = {
    'prod_id': prod.gen_prod_id(),
    'prod_name': '',
    'prod_cat': '',
    'prod_brand': '',
    'prod_price': '',
    'prod_qty': '',
    'prod_size': ''
}

update_prod = {
    'prod_id': '',
    'prod_cat': '',
    'prod_brand': '',
    'prod_price': '',
    'prod_qty': ''
}

# ARRAYS 
prod_cats = ['Dresses', 'Jackets', 'Skirts', 'Jeans', 'Pants', 'Shorts', 'Tops', 'Accessories', 'Sweaters', 'Shoes', 'Underwear']

# FLASK APPLICATION
app = Flask(__name__)
app.config.from_pyfile('config.py')    

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/newproduct", methods=["POST", "GET"])
def new_product():

    if request.method == "POST":
        new_prod['prod_name'] = request.form["inputProductName"]
        new_prod['prod_cat'] = request.form["inputProdCat"]
        new_prod['prod_brand'] = request.form["inputProdBrand"]
        new_prod['prod_price'] = request.form["inputProdPrice"]
        new_prod['prod_qty'] = request.form["inputProdQty"]
        new_prod['prod_size'] = request.form["inputProdSize"]
        
        # ADD NEW PRODUCT
        prod.add_product(new_prod['prod_id'], new_prod['prod_name'], new_prod['prod_cat'], 
                        new_prod['prod_brand'], new_prod['prod_price'], new_prod['prod_qty'], new_prod['prod_size'])

        return render_template('newproduct.html', prod_cats=prod_cats)
    else:
        return render_template('newproduct.html', prod_cats=prod_cats)

@app.route("/updateproduct", methods=["POST", "GET"])
def update_product():
    prod_ids = prod.get_col_values()

    if request.method == "POST":
        update_prod['prod_id'] = request.form["inputProdID"]
        try:
            update_prod['prod_cat'] = request.form["inputProdCat"]
        except KeyError:
            update_prod['prod_cat'] = ''
        update_prod['prod_brand'] = request.form["inputProdBrand"]
        update_prod['prod_price'] = request.form["inputProdPrice"]
        update_prod['prod_qty'] = request.form["inputProdQty"]

        for key in update_prod:
            if update_prod[key] == '':
                update_prod[key] = None

        # UPDATE EXISTING PRODUCT
        prod.update_product(update_prod['prod_id'], update_prod['prod_cat'], update_prod['prod_brand'], 
                            update_prod['prod_price'], update_prod['prod_qty'])

        return render_template('updateproduct.html', prod_ids=prod_ids, prod_cats=prod_cats)
    else:
        return render_template('updateproduct.html', prod_ids=prod_ids, prod_cats=prod_cats)

if __name__ == "__main__":
    app.run(debug=True)