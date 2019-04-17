import app
import unittest, os, random, json, string
from faker import Faker
from flaski.models import Shop, Product
from flaski.database import db_session
from cerberus import Validator

app.app.config['TESTING'] = True

class TestApp(unittest.TestCase):

    def setUp(self):
        self.fake = Faker()
        self.app = app.app.test_client()

    def tearDown(self):
        pass
    
    def randomname(self, n):
        return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

    def build_shop_json(self):
        shop_json = {
            'name': self.fake.company()
        }
        return shop_json

    def create_new_shop(self):
        shop_json = self.build_shop_json()
        shop = Shop(**shop_json)
        db_session.add(shop)
        db_session.commit()
        return shop
    def build_product_json(self, shops_id=None):
        product_json = {
            'title': self.fake.name(),
            'link': self.fake.profile(fields=['website'])['website'][0],
            'description': self.fake.profile(fields=['residence'])['residence'],
            'image_link': self.fake.profile(fields=['website'])['website'][0]
        }
        if shops_id:
            product_json['shops_id'] = shops_id
        return product_json  

    def create_new_product(self, shops_id=None):
        product_json = self.build_product_json(shops_id)
        product = Product(**product_json)
        db_session.add(product)
        db_session.commit()
        return product    

    def create_new_product_with_json(self, product_json):
        product = Product(**product_json)
        db_session.add(product)
        db_session.commit()
        return product      

    def test_shop_validate(self):
       v = Validator()
       self.assertFalse(v.validate({'name1': 'aaa'}, app.shop_schema))
       self.assertFalse(v.validate({'name': ''}, app.shop_schema))
       self.assertTrue(v.validate({'name': self.randomname(200)}, app.shop_schema))
       self.assertFalse(v.validate({'name': self.randomname(201)}, app.shop_schema))
       self.assertTrue(v.validate({'name': self.randomname(200)}, app.shop_schema))
    
    def test_product_validate(self):
        v = Validator()
        self.assertFalse(v.validate({'title1': 'aaa'}, app.product_schema))
        self.assertFalse(v.validate({'title': ''}, app.product_schema))
        self.assertTrue(v.validate({'title': self.randomname(100)}, app.product_schema))
        self.assertTrue(v.validate({'title': self.randomname(100), 'link': self.randomname(255),
            'description': self.randomname(5000), 'image_link': self.randomname(255)}, app.product_schema))

    def test_shops(self):
        shops = []
        for i in range(3):
            shops.append(self.create_new_shop())
        response = self.app.get('/shops', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data())
        response_shops_names = [d.get('name') for d in response_data]
        for shop in shops:
            self.assertIn(shop.name, response_shops_names)

    def test_post_shop(self):
        shop_json = self.build_shop_json()
        response = self.app.post('/shops', follow_redirects=True, data=json.dumps(shop_json),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data())
        self.assertEqual(shop_json['name'], response_data['name'])

    def test_get_shop_products(self):
        shop = self.create_new_shop()
        products = []
        for i in range(3):
            products.append(self.create_new_product(shop.id))
        response = self.app.get('/shops/{}/products'.format(shop.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data())
        response_products_titles = [d.get('title') for d in response_data]
        for product in products:
            self.assertIn(product.title, response_products_titles)

    def test_get_shop_linked_imaged_products(self):
        shop = self.create_new_shop()
        shop_id = shop.id
        product_json = self.build_product_json(shop_id)
        self.create_new_product_with_json(product_json)
        product2 = self.build_product_json(shop_id)
        product2['link'] = None
        self.create_new_product_with_json(product2)
        product3 = self.build_product_json(shop_id)
        product3['image_link'] = None
        self.create_new_product_with_json(product3)
        product4 = self.build_product_json(shop_id)
        product4['link'] = None
        product4['image_link'] = None
        self.create_new_product_with_json(product4)
        product5 = self.build_product_json(shop_id)
        product5['link'] = ""
        product5['image_link'] = ""
        self.create_new_product_with_json(product5)
        response = self.app.get('/shops/{}/linked_imaged_products'.format(shop_id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.get_data())
        self.assertEqual(len(response_data), 1)
        response_data = response_data[0]
        self.assertEqual(product_json['title'], response_data['title'])
        self.assertEqual(shop_id, response_data['shops_id'])
        self.assertEqual(product_json['link'], response_data['link'])
        self.assertEqual(product_json['description'], response_data['description'])
        self.assertEqual(product_json['image_link'], response_data['image_link'])

    def test_post_shop_products(self):
        shop = self.create_new_shop()
        shop_id = shop.id
        product_json = self.build_product_json()
        response = self.app.post('/shops/{}/products'.format(shop_id), follow_redirects=True, data=json.dumps(product_json),
        content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data())
        self.assertEqual(product_json['title'], response_data['title'])
        self.assertEqual(shop_id, response_data['shops_id'])
        self.assertEqual(product_json['link'], response_data['link'])
        self.assertEqual(product_json['description'], response_data['description'])
        self.assertEqual(product_json['image_link'], response_data['image_link'])

if __name__ == '__main__':
    unittest.main()
