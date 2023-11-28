#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    All_bakeries=Bakery.query.all()
    serialized_bakeries = [bakery.to_dict(rules=Bakery.serialize_rules) for bakery in All_bakeries]
    response=jsonify(serialized_bakeries)
    return response

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery=Bakery.query.filter(Bakery.id==id).first()
    serialized_bakery = bakery.to_dict(rules=Bakery.serialize_rules)
    response=jsonify(serialized_bakery)
    return response

@app.route('/baked_goods/by_price')
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    response = [{'id': good.id,'name': good.name, 'price': good.price , 'created_at':good.created_at, } for good in baked_goods]
    return jsonify(response)

@app.route('/baked_goods/most_expensive')
def get_most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    result = {'id': most_expensive_good.id,'name': most_expensive_good.name, 'price': most_expensive_good.price, 'created_at':most_expensive_good.created_at} 
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
