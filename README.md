# python_dev_english_shops
english_shops coding test

## environment
- Python 3.6
- Flask
- SQLite

# installation
## download Docker
[Get Started with Docker](https://www.docker.com/get-started)
## builds docker compose
```
$ docker-compose up -d 
```

## access url
http://0.0.0.0:5000/

# execution
## all shop list
```
$ http GET http://0.0.0.0:5000/shops
HTTP/1.0 200 OK
Content-Length: 1124
Content-Type: application/json
Date: Wed, 17 Apr 2019 11:45:41 GMT
Server: Werkzeug/0.15.2 Python/3.6.2

[
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 1,
        "name": "Eye of Tree data feed"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 2,
        "name": "uniqbrow data feed"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 3,
        "name": "Tattoo it data feed"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 4,
        "name": "Solid Leather data feed"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 5,
        "name": "NDNLadies Bead Supply data feed"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 6,
        "name": "LogoCosmos data feed"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 7,
        "name": "Fragrance Top data feed"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 8,
        "name": "thebigturk2 data feed"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 9,
        "name": "LaSanaX data feed"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "id": 10,
        "name": "tekbotic data feed"
    }
]
```
## all product list (given shop)
```
$ http GET http://0.0.0.0:5000/shops/1/products
HTTP/1.0 200 OK
Content-Length: 1422
Content-Type: application/json
Date: Wed, 17 Apr 2019 11:46:42 GMT
Server: Werkzeug/0.15.2 Python/3.6.2

[
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "description": "A classic ringer style t-shirt featuring the Eye of Tree seal.\n   100% pre-shrunk combed ring-spun cotton (Heather colors contain polyester)    Semi-fitted    Contrast color binding at neck and sleeves    Double-needle stitched bottom hem\n \n\n\n\n\n \nS\nM\nL\nXL\n2XL\n\n\nBody Length (inches) \n27 1/2\n28  \n29  \n30  \n32\n\n\nBody Width (inches) \n18\n20\n22\n24\n26",
        "id": 1,
        "image_link": "https://cdn.shopify.com/s/files/1/1981/6771/products/mockup-066cc215.png?v=1504737037",
        "link": "https://eye-of-tree.myshopify.com/products/seal-ringer-t-shirt",
        "shops_id": 1,
        "title": "Seal Ringer T-Shirt"
    },
    {
        "created_at": "Wed, 17 Apr 2019 19:23:51 GMT",
        "description": "A super soft t-shirt featuring the Eye of Tree seal.   100% ring-spun cotton (heather colors contain polyester)   Baby-knit jersey    Shoulder-to-shoulder taping    Cover stitched and hemmed sleeves    Side-seamed    Unisex\n \n\n\n\n\n \nS\nM\nL\nXL\n2XL\n3XL\n4XL\n\n\nLength (inches) \n28\n29\n30\n31\n32\n33\n34\n\n\nWidth (inches) \n18\n20\n22\n24\n26\n28\n30",
        "id": 2,
        "image_link": "https://cdn.shopify.com/s/files/1/1981/6771/products/mockup-cee83cfa.png?v=1504133697",
        "link": "https://eye-of-tree.myshopify.com/products/eye-of-tree-seal-t-shirt",
        "shops_id": 1,
        "title": "Seal T-Shirt"
    }
]
```

## create new shop
```
$ http POST http://0.0.0.0:5000/shops name='shop name 1'
HTTP/1.0 201 CREATED
Content-Length: 91
Content-Type: application/json
Date: Wed, 17 Apr 2019 11:49:59 GMT
Server: Werkzeug/0.15.2 Python/3.6.2

{
    "created_at": "Wed, 17 Apr 2019 20:42:59 GMT",
    "id": 11,
    "name": "shop name 1"
}
```
## create new product (given shop)
```
$ http POST http://0.0.0.0:5000/shops/11/products title='product name 1' link='http://link.com/' description='description1' image_link='http://image-link.com/'
HTTP/1.0 201 CREATED
Content-Length: 222
Content-Type: application/json
Date: Wed, 17 Apr 2019 11:55:34 GMT
Server: Werkzeug/0.15.2 Python/3.6.2

{
    "created_at": "Wed, 17 Apr 2019 20:42:59 GMT",
    "description": "description1",
    "id": 48,
    "image_link": "http://image-link.com/",
    "link": "http://link.com/",
    "shops_id": 11,
    "title": "product name 1"
}

$ http POST http://0.0.0.0:5000/shops/11/products title='product name 2' description='description2'
HTTP/1.0 201 CREATED
Content-Length: 188
Content-Type: application/json
Date: Wed, 17 Apr 2019 11:56:13 GMT
Server: Werkzeug/0.15.2 Python/3.6.2

{
    "created_at": "Wed, 17 Apr 2019 20:42:59 GMT",
    "description": "description2",
    "id": 49,
    "image_link": null,
    "link": null,
    "shops_id": 11,
    "title": "product name 2"
}
```
## all product list (having link and image_link, given shop)
```
$ http GET http://0.0.0.0:5000/shops/11/linked_imaged_products
http GET http://0.0.0.0:5000/shops/11/linked_imaged_products
HTTP/1.0 200 OK
Content-Length: 244
Content-Type: application/json
Date: Wed, 17 Apr 2019 11:56:30 GMT
Server: Werkzeug/0.15.2 Python/3.6.2

[
    {
        "created_at": "Wed, 17 Apr 2019 20:42:59 GMT",
        "description": "description1",
        "id": 48,
        "image_link": "http://image-link.com/",
        "link": "http://link.com/",
        "shops_id": 11,
        "title": "product name 1"
    }
]

```

# database
## create database schema
```
$ python do_create.py
```

## insert data
```
$ python do_insert.py 
```

