# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Flask,request,jsonify
import product
import uom
import order
import json
from sql_connection import get_sql_connection
from flask_cors import CORS

# Flask constructor takes the name of 
# current module (__name__) as argument.
connection=get_sql_connection() 

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
app = Flask(__name__)
CORS(app)

@app.route('/getProducts', methods=['GET'])
def get_products():
    response=product.get_all_products(connection)
    response=jsonify(response)
    response.headers.add('Access-Control-Allow-Origin','*')
    return response

@app.route('/getUOM',methods=['GET'])
def get_uom():
    response = uom.get_uoms(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route('/insertProduct', methods=['POST'])
def insert_product():
    request_payload = json.loads(request.form['data'])
    product_id = product.insert_new_product(connection, request_payload)
    response = jsonify({
        'product_id': product_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/getAllOrders', methods=['GET'])
def get_all_orders():
    response = order.get_all_orders(connection)
    response = jsonify(response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/insertOrder', methods=['POST'])
def insert_order():
    request_payload = json.loads(request.form['data'])
    order_id = order.insert_order(connection, request_payload)
    response = jsonify({
        'order_id': order_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/deleteProduct', methods=['POST'])
def delete_product():
    return_id = product.delete_product(connection, request.form['product_id'])
    response = jsonify({
        'product_id': return_id
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
# main driver function
if __name__ == '__main__':  
    app.run(port=5000)
    # run() method of Flask class runs the application 
    # on the local development server.