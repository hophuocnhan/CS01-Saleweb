import json
from saleapp import app
from saleapp.models import Category, Product


def load_categories():
    return Category.query.all()


def load_products(cate_id=None, kw=None):
    query = Product.query

    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))
    if kw:
        query = query.filter(Product.name.contains(kw))

    return query.all();


def get_product_by_id(product_id):
    return Product.query.get(product_id)
