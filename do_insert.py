from flaski.database import init_db
from flaski.database import db_session
from flaski.models import Shop, Product
import json

f = open("english_shops.json", 'r')
json_data_all = json.load(f)
for index, shop_name in enumerate(json_data_all):
    # insert shop
    shop = Shop(shop_name, index+1)
    db_session.add(shop)
    db_session.commit()
    for json_data in json_data_all[shop_name]:
        # insert product
        json_data['shops_id'] = index+1
        product = Product(**json_data)
        db_session.add(product)
        db_session.commit()
