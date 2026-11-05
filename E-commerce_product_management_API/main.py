from fastapi import FastAPI,Path,HTTPException
import json

app=FastAPI()

#read product data from json file
def load_product():
    with open("product.json","r") as file:
        return json.load(file)

#Get all product
@app.get("/products")
def show_product():
    product=load_product()
    return product

#get product by id
@app.get("/products/id/{product_id}")
def get_product(product_id:str=Path(...)):
    product=show_product()
    if product_id in product:
        return product[product_id]
    raise HTTPException(status_code=404,detail="product not found")
    
#get product by category  
@app.get("/products/category/{category}")
def get_product_by_category(category:str):
    product=show_product()
    result={}
    for product_id,product in product.items():
        if product["category"].lower()==category.lower():
            result[product_id]=product
    return result

#get product by brand
@app.get("/products/brand/{brand}")
def get_product_brand(brand:str=Path(...)):
    product=show_product()
    #stored the brand we want to requied in result
    result={}

    for product_id,product in product.items():
        if product["brand"].lower()==brand.lower():
            result[product_id]=product
    return result


#get product under maximum price
"""http://127.0.0.1:8000/products?price=55000.00"""
#@app.get("/products/price")

@app.get("/products/price/{max_price}")
def get_products_by_price(max_price:float):
    product=show_product()
    result={}

    for product_id,product in product.items():
        if product["price"]<=max_price:
            result[product_id]=product


    return result

# 6. Get products in stock
@app.get("/products/stock")
def get_products_in_stock():
    products = show_product()
    result = {}

    for product_id, product in products.items():
        if product["stock"] > 0:
            result[product_id] = product

    return result


