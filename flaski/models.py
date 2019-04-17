from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from flaski.database import Base
from datetime import datetime

class Shop(Base):
    __tablename__ = 'shops'
    id = Column(Integer, primary_key=True)          
    name = Column(String(128), nullable=False)       
    created_at = Column(DateTime, default=datetime.now()) 

    products = relationship("Product", backref="products")

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            created_at=self.created_at
        )

    def __init__(self, name, id=None,  created_at=None):
        self.id = id
        self.name = name
        self.created_at = created_at

    def __repr__(self):
        return '<Name %r>' % (self.name)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    shops_id = Column(Integer, ForeignKey('shops.id'))
    title = Column(String, nullable=False)
    link = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image_link = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now()) 
 
    shop = relationship("Shop")  

    def to_dict(self):
        return dict(
            id=self.id,
            shops_id=self.shops_id,
            title=self.title,
            link=self.link,
            description=self.description,
            image_link=self.image_link,
            created_at=self.created_at
        )          

    def __init__(self, shops_id, title, link=None, description=None, image_link=None, created_at=None):
        self.shops_id = shops_id
        self.title = title
        self.link = link
        self.description = description
        self.image_link = image_link
        self.created_at = created_at

    def __repr__(self):
        return '<Title %r>' % (self.title)
