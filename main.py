from flask import Flask, request, url_for, redirect, render_template, flash
import gspread
from random import randrange


gc = gspread.service_account()
sh = gc.open("Clothing Store Inventory")
wk = sh.worksheet("prod_inventory")

# Functions
def get_prod_ids():
    prod_ids = wk.col_values(1)
    
    return prod_ids

def get_product_cat():
    prod_cat = ['Dresses', 'Jackets', 'Skirts', 'Jeans', 'Pants', 'Shorts', 'Tops', 'Accessories', 'Sweaters', 'Shoes', 'Underwear']

    return prod_cat

def gen_prod_id():
    prod_ids = get_prod_ids()
    prod_id = int(prod_ids.pop()) + 1

    return prod_id

def find_next_row():
    prod_ids = get_prod_ids()
    next_row_num = str(len(prod_ids) + 1)

    return next_row_num

def gen_sku():
    sku = ''
    size = new_prod['prod_size']
    for x in range(0,8):
        sku_1 = str((randrange(0,10)))
        sku += sku_1
    
    full_sku = f'{sku}_{size}'

    return full_sku

def find_row_num():
    prod_id = update_prod['prod_id']
    cell = wk.find(prod_id)
    row_num = cell.row

    return row_num

def append_row():
    prod_id = gen_prod_id()
    sku = gen_sku()
    row_num = find_next_row()

    wk.update(f'A{row_num}', prod_id)
    wk.update(f'B{row_num}', new_prod['prod_name'])
    wk.update(f'C{row_num}', new_prod['prod_cat'])
    wk.update(f'D{row_num}', new_prod['prod_brand'])
    wk.update(f'E{row_num}', new_prod['prod_price'])
    wk.update(f'F{row_num}', new_prod['prod_qty'])
    wk.update(f'G{row_num}', sku)

def update_row():
    row_num = find_row_num()
    
    wk.update(f'C{row_num}', update_prod['prod_cat'])
    wk.update(f'D{row_num}', update_prod['prod_brand'])
    wk.update(f'E{row_num}', update_prod['prod_price'])
    wk.update(f'F{row_num}', update_prod['prod_qty'])

new_prod = {
    'prod_id': '',
    'prod_name': '',
    'prod_cat': '',
    'prod_brand': '',
    'prod_price': '',
    'prod_qty': '',
    'prod_size': ''
}

update_prod = {
    'prod_cat': '',
    'prod_brand': '',
    'prod_price': '',
    'prod_qty': ''
}

app = Flask(__name__)
app.config.from_pyfile('config.py')
@app.route("/")
@app.route("/home")

def home():
    return render_template('home.html')

@app.route("/newproduct", methods=["POST", "GET"])
def new_product():
    prod_cats = get_product_cat()
    
    if request.method == "POST":
        new_prod['prod_name'] = request.form["inputProductName"]
        new_prod['prod_cat'] = request.form["inputProdCat"]
        new_prod['prod_brand'] = request.form["inputProdBrand"]
        new_prod['prod_price'] = request.form["inputProdPrice"]
        new_prod['prod_qty'] = request.form["inputProdQty"]
        new_prod['prod_size'] = request.form["inputProdSize"]

        append_row()

        prod_cats = get_product_cat()

        prod_ids = get_prod_ids()
        prod_id = prod_ids.pop()
        skus = wk.col_values(7)
        sku = skus.pop()

        flash(f'Successfully added new product: Product ID: {prod_id} | Product Name: {new_prod["prod_name"]} | Product Category: {new_prod["prod_cat"]} | Brand: {new_prod["prod_brand"]} | Price: {new_prod["prod_price"]} | Quantity: {new_prod["prod_qty"]} | Size: {new_prod["prod_size"]} | SKU: {sku}')
        
        return render_template('newproduct.html', prod_cats=prod_cats)

    else:

        return render_template('newproduct.html', prod_cats=prod_cats)

@app.route("/updateproduct", methods=["POST", "GET"])
def update_product():
    prod_ids = get_prod_ids()
    prod_cats = get_product_cat()

    if request.method == "POST":
        update_prod['prod_id'] = request.form["inputProdID"]

        try:
            update_prod['prod_cat'] = request.form["inputProdCat"]
            if update_prod['prod_cat'] == '':
                update_prod['prod_cat'] = None
        except KeyError as ke:
            update_prod['prod_cat'] = None

        update_prod['prod_brand'] = request.form["inputProdBrand"]
        if update_prod['prod_brand'] == '':
            update_prod['prod_brand'] = None
            
        update_prod['prod_price'] = request.form["inputProdPrice"]
        if update_prod['prod_price'] == '':
            update_prod['prod_price'] = None

        update_prod['prod_qty'] = request.form["inputProdQty"]
        if update_prod['prod_qty'] == '':
            update_prod['prod_qty'] = None

        update_row()

        prod_ids = get_prod_ids()
        prod_cats = get_product_cat()

        return render_template('updateproduct.html', prod_ids=prod_ids, prod_cats=prod_cats)

    else:

        return render_template('updateproduct.html', prod_ids=prod_ids, prod_cats=prod_cats)

if __name__ == "__main__":
    app.run(debug=True)
