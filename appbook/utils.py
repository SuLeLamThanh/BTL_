import json, os
from appbook import app
from appbook.models import Category, Product, User, UserRole, Receipt, ReceiptDetail, Comment, ReceiptOnline, ReceiptDetailOnline, UserInfo
from appbook import app, db
from appbook.models import Category, Product, User, UserRole
from sqlalchemy import func
from flask_login import current_user
from sqlalchemy.sql import extract
import hashlib

#
# def read_json(path):
#     with open(path, "r", encoding='utf-8') as f:
#         return json.load(f)
#
#
# def load_categories():
#     return Category.query.all()
#     # return read_json(os.path.join(app.root_path, 'data/categories.json'))
#
# #
# # def load_products(cate_id=None, kw=None, from_price=None, to_price=None):
# #     return Category.query.all()
#     # products = read_json(os.path.join(app.root_path, 'data/products.json'))
#     #
#     # if kw:
#     #     products = [p for p in products if p["name"].lower().find(kw.lower()) >= 0]
#     # if cate_id:
#     #     products = [p for p in products if p["category_id"] == int(cate_id)]
#     # if from_price:
#     #     products = [p for p in products if p["price"] >= float(from_price)]
#     # if to_price:
#     #     products = [p for p in products if p["category_id"] <= float(to_price)]
#     # return products
#
#
# def load_products(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
#     products = Product.query.filter(Product.active.__eq__(True))
#
#     if cate_id:
#         products = products.filter(Product.category_id.__eq__(cate_id))
#
#     if kw:
#         products = products.filter(Product.name.contains(kw))
#
#     if from_price:
#         products = products.filter(Product.price.__ge__(from_price))
#
#     if to_price:
#         products = products.filter(Product.price.__le__(from_price))
#
#     page_size = app.config['PAGE_SIZE']
#     start = (page - 1) * page_size
#     end = start + page_size
#
#     return products.slice(start, end).all()
#
#
# def add_user(name, username, password, **kwargs):
#     password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#     user = User(name=name.strip(),
#                 username=username.strip(),
#                 password=password,
#                 email=kwargs.get('email'),
#                 avatar=kwargs.get('avatar'))
#
#     db.session.add(user)
#     db.session.commit()
#
#
# def get_user_by_id(user_id):
#     return User.query.get(user_id)
#
#
# def check_login(username, password, role=UserRole.USER):
#     if username and password:
#         password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
#
#         return User.query.filter(User.username.__eq__(username.strip()),
#                                  User.password.__eq__(password),
#                                  User.user_role.__eq__(role)).first()
#
#
# def count_products():
#     return Product.query.filter(Product.active.__eq__(True)).count()
#
#
# def category_stats():
#     # return Category.query.join(Product, Product.category_id.__eq__(Category.id)).add_columns(func.count(Product.id)).group_by(Category.id, Category.name).all()
#     return db.session.query(Category.id, Category.name, func.count(Product.id)) \
#                      .join(Product, Product.category_id.__eq__(Category.id), isouter=True) \
#                      .group_by(Category.id).all()
#
#
# def count_cart(cart):
#     total_quantity, total_amount = 0, 0
#
#     if cart:
#         for c in cart.values():
#             total_quantity += c['quantity']
#             total_amount += c['quantity'] * c['price']
#
#     return {
#         'total_quantity': total_quantity,
#         'total_amount': total_amount
#     }
#
#
# def get_product_by_id(product_id):
#     return Product.query.get(product_id)
#     # products = read_json(os.path.join(app.root_path, 'data/products.json'))
#     # for p in products:
#     #     if p['id'] == product_id:
#     #         return p


def read_json(path):
    with open(path, "r") as f:
        return json.load(f)


def load_categories():
    return Category.query.all()
    # return read_json(os.path.join(app.root_path, 'data/categories.json'))


def load_products(cate_id=None, kw=None, from_price=None, to_price=None, page=1):
    products = Product.query.filter(Product.active.__eq__(True))

    if cate_id:
        products = products.filter(Product.category_id.__eq__(cate_id))

    if kw:
        products = products.filter(Product.name.contains(kw))

    if from_price:
        products = products.filter(Product.price.__ge__(from_price))

    if to_price:
        products = products.filter(Product.price.__le__(from_price))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1) * page_size
    end = start + page_size

    return products.slice(start, end).all()


def count_products():
    return Product.query.filter(Product.active.__eq__(True)).count()
    # products = read_json(os.path.join(app.root_path, 'data/products.json'))
    # if cate_id:
    #     products = [p for p in products if p['category_id'] == int(cate_id)]
    #
    # if kw:
    #     products = [p for p in products if p['name'].lower().find(kw.lower()) >=0]
    #
    # if from_price:
    #     products = [p for p in products if p['price'] >= float(from_price)]
    # if to_price:
    #     products = [p for p in products if p['price'] <= float(to_price)]
    # return products


def get_product_by_id(product_id):
    return Product.query.get(product_id)
    # products = read_json(os.path.join(app.root_path, 'data/products.json'))
    # for p in products:
    #     if p['id'] == product_id:
    #         return p


def add_user(name, username, password, **kwargs):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(name=name.strip(),
                username=username.strip(),
                password=password,
                email=kwargs.get('email'),
                avatar=kwargs.get('avatar'))

    db.session.add(user)
    db.session.commit()


def check_login(username, password, role=UserRole.USER):
    if username and password:
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

        return User.query.filter(User.username.__eq__(username.strip()),
                                 User.password.__eq__(password),
                                 User.user_role.__eq__(role)).first()


def get_user_by_id(user_id):
    return User.query.get(user_id)


# with app.app_context():
#     if __name__ == '__main__':
#         db.create_all()


def add_receipt(cart):
    if cart:
        receipt = Receipt(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
            d = ReceiptDetail(receipt=receipt,
                              product_id=c['id'],
                              quantity=c['quantity'],
                              unit_price=c['price'])
            db.session.add(d)

        db.session.commit()


def category_stats():

    # return Category.query.join(Product, Product.category_id.__eq__(Category.id)).add_columns(func.count(Product.id)).group_by(Category.id, Category.name).all()
    return db.session.query(Category.id, Category.name, func.count(Product.id)) \
                     .join(Product, Product.category_id.__eq__(Category.id), isouter=True) \
                     .group_by(Category.id).all()


def count_cart(cart):
    total_quantity, total_amount=0, 0

    if cart:
        for c in cart.values():
            total_quantity += c['quantity']
            total_amount += c['quantity'] * c['price']

    return {
        'total_quantity': total_quantity,
        'total_amount': total_amount
    }

#
# def count_product_after_sell(product_id, cart):
#     p = db.session()
#     for p in product_id.values():
#         if cart:
#             for c in cart.values():
#                 p.quantity -= c['quantity']


def product_stats(kw=None, from_date=None, to_date=None):
    p = db.session.query(extract('month', Receipt.created_date), Category.name,
                         func.sum(ReceiptDetail.quantity * ReceiptDetail.unit_price))\
                  .join(Product, Product.category_id.__eq__(Category.id), isouter=True)\
                  .join(ReceiptDetail, ReceiptDetail.product_id.__eq__(Product.id), isouter=True)\
                  .join(Receipt, Receipt.id.__eq__(ReceiptDetail.receipt_id))\
                  .group_by(extract('month', Receipt.created_date), Category.name)

    if kw:
        p = p.filter(Product.name.contains(kw))

    if from_date:
        p = p.filter(Receipt.created_date.__ge__(from_date))

    if to_date:
        p = p.filter(Receipt.created_date.__le__(to_date))

    return p.order_by(extract('month', Receipt.created_date)).all()


def product_month_stats(year):
    return db.session.query(Product.name, extract('month', Receipt.created_date), func.count(ReceiptDetail.product_id))\
                     .join(ReceiptDetail, ReceiptDetail.receipt_id.__eq__(Receipt.id)) \
                     .filter(extract('year', Receipt.created_date) == year)\
                     .group_by(extract('month', Receipt.created_date), Product.name)\
                     .order_by(extract('month', Receipt.created_date)).all()


def add_comment(content, product_id):
    c = Comment(content=content, product_id=product_id, user=current_user)

    db.session.add(c)
    db.session.commit()
    return c


def get_comment(product_id, page=1):
    page_size = app.config['COMMENT_SIZE']
    start = (page - 1) * page_size
    end = start + page_size
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).order_by(-Comment.id).slice(start, start + page_size).all()


def count_comment(product_id):
    return Comment.query.filter(Comment.product_id.__eq__(product_id)).count()


def add_receipt_online(cart):
    if cart:
        receipt = ReceiptOnline(user=current_user)
        db.session.add(receipt)

        for c in cart.values():
             d = ReceiptDetailOnline(receipt=receipt,
                                     product_id=c['id'],
                                     quantity=c['quantity'],
                                     unit_price=c['price'],
                                     take_up=c['take_up'])
             db.session.add(d)

        db.session.commit()


def add_info(info):
    info = UserInfo(user=current_user)
    db.session.add(info)
    db.session.commit()