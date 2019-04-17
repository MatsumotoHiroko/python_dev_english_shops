from flask import Flask, request, redirect, url_for, abort, jsonify
from flaski.models import Shop, Product
from cerberus import Validator
from flaski.database import db_session

shop_schema = {
    'name': {
        'type': 'string',
        'required': True,
        'empty': False,
        'maxlength': 200
    }
}

product_schema = {
    'title': {
        'type': 'string',
        'required': True,
        'empty': False,
        'maxlength': 100
    },
    'link': {
        'type': 'string',
        'maxlength': 255
    },
    'description': {
        'type': 'string',
        'maxlength': 5000
    },
    'image_link': {
        'type': 'string',
        'maxlength': 255
    }
}

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('application.cfg', silent=True)

@app.teardown_request
def shutdown_session(exception=None):
    db_session.remove()

@app.route('/')
def index():
    return redirect('/shops')

@app.route('/shops', methods=['GET'])
def all_shops():
    shops = Shop.query.all()
    result = []
    if shops:
        result = [l.to_dict() for l in shops]
    return jsonify(result), 200

@app.route('/shops', methods=['POST'])
def create_shop():
    json = request.get_json()
    if json:
        v = Validator()
        if not v.validate(json, shop_schema):
            return jsonify(v.errors), 400
    else:
        return jsonify({'message': 'no json data'}), 400
    content = Shop(**json)
    db_session.add(content)
    db_session.commit()
    return jsonify(content.to_dict()), 201

@app.route('/shops/<int:id>/products', methods=['GET'])
def get_shop_products(id):
    result = logic_get_shop_products(id)
    return jsonify(result), 200

@app.route('/shops/<int:id>/linked_imaged_products', methods=['GET'])
def get_shop_linked_imaged_products(id):    
    result = logic_get_shop_products(id, True)
    return jsonify(result), 200

def logic_get_shop_products(id, linked_imaged=False):
    shop = Shop.query.get(id)
    result = []
    if shop:
        products = []
        if linked_imaged:
            products = Product.query.filter(
                Product.shops_id == id, 
                Product.link.isnot(None), Product.link.isnot(''), 
                Product.image_link.isnot(None), Product.image_link.isnot('')
            )
        else:
            products = shop.products
        if products:
            result = [l.to_dict() for l in products]
    return result
    
@app.route('/shops/<int:id>/products', methods=['POST'])
def create_shop_products(id):
    json = request.get_json()
    if json:
        v = Validator()
        if not v.validate(json, product_schema):
            return jsonify(v.errors), 400
    else:
        return jsonify({'message': 'no json data'}), 400
    shop = Shop.query.get(id)
    if not shop:
        return jsonify({'message': 'invalid shops id'}), 400
    json['shops_id'] = shop.id
    content = Product(**json)
    db_session.add(content)
    db_session.commit()
    return jsonify(content.to_dict()), 201
     
@app.errorhandler(500)
@app.errorhandler(404)
@app.errorhandler(405)
def error_handler(error):
    return jsonify({'message': 'access error'}), error.code

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)