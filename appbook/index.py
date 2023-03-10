from flask import render_template
from flask import render_template, request, redirect, url_for, session, jsonify
from appbook import app, login
from appbook.admin import *
import utils, math
import cloudinary.uploader
from flask_login import login_user, logout_user, login_required
from appbook.models import UserRole

#
# @app.route("/")
# def index():
#     cate_id = request.args.get('category_id')
#     kw = request.args.get('keyword')
#     page = request.args.get('page', 1)
#     products = utils.load_products(cate_id=cate_id, kw=kw, page=int(page))
#     counter = utils.count_products()
#
#     return render_template('index.html',
#                            products=products,
#                            pages=math.ceil(counter / app.config['PAGE_SIZE'])
#                            )
#
#
# @app.route('/register', methods=['get', 'post'])
# def user_register():
#     err_msg = ""
#     if request.method.__eq__('POST'):
#         name = request.form.get('name')
#         username = request.form.get('username')
#         password = request.form.get('password')
#         email = request.form.get('email')
#         confirm = request.form.get('confirm')
#         avatar_path = None
#         try:
#             if password.strip().__eq__(confirm.strip()):
#                 avatar = request.files.get('avatar')
#                 if avatar:
#                     res = cloudinary.uploader.upload(avatar)
#                     avatar_path = res['secure_url']
#                 utils.add_user(name=name, username=username, password=password,
#                                email=email, avatar=avatar_path)
#                 return redirect(url_for('user_signin'))
#             else:
#                 err_msg = 'Mật khẩu không khớp!'
#         except Exception as ex:
#             err_msg = 'Hệ thống đang có lỗi!!' + str(ex)
#
#     return render_template('register.html ', err_msg=err_msg)
#
#
# @app.route('/user-login', methods=['get', 'post'])
# def user_signin():
#     err_msg = ''
#     if request.method.__eq__('POST'):
#         username = request.form.get('username')
#         password = request.form.get('password')
#
#         user = utils.check_login(username=username, password=password)
#
#         if user:
#             login_user(user=user)
#             return redirect(url_for(request.args.get('next', 'index')))
#         else:
#             err_msg = 'Username hoặc password không chính xác!!!'
#
#     return render_template('login.html', err_msg=err_msg)
#
#
# @app.route('/user-logout')
# def user_signout():
#     logout_user()
#     return redirect(url_for('user_signin'))
#
#
# @app.route('/admin-login', methods=['post'])
# def signin_admin():
#     username = request.form['username']
#     password = request.form['password']
#
#     user = utils.check_login(username=username,
#                              password=password,
#                              role=UserRole.ADMIN)
#     if user:
#         login_user(user=user)
#
#     return redirect('/admin')
#
#
# @login.user_loader
# def user_load(user_id):
#     return utils.get_user_by_id(user_id=user_id)
#
#
# @app.route("/products")
# def product_list():
#     cate_id = request.args.get("category_id")
#     kw = request.args.get("keyword")
#     from_price = request.args.get("from_price")
#     to_price = request.args.get("to_price")
#
#     products = utils.load_products(cate_id=cate_id,
#                                    kw=kw,
#                                    from_price=from_price,
#                                    to_price=to_price)
#     return render_template('products.html',
#                            products=products)
#
#
# @app.context_processor
# def common_response():
#     return {
#         'categories': utils.load_categories(),
#         'cart_stats': utils.count_cart(session.get('cart'))
#     }
#
#
# @app.route("/products/<int:product_id>")
# def product_detail(product_id):
#     product = utils.get_product_by_id(product_id)
#
#     return render_template('product_detail.html', product=product)
#
#
# @app.route('/cart')
# def cart():
#     return render_template('cart.html', stats=utils.count_cart(session.get('cart')))
#
#
# @app.route('/api/add-cart', methods=['post'])
# def add_to_cart():
#     data = request.json
#     id = str(data.get('id'))
#     name = data.get('name')
#     price = data.get('price')
#     cart = session.get('cart')
#     if not cart:
#         cart = {}
#
#     if id in cart:
#         cart[id]['quantity'] = cart[id]['quantity'] + 1
#     else:
#         cart[id] = {
#             'id': id,
#             'name': name,
#             'price': price,
#             'quantity': 1
#         }
#     session['cart'] = cart
#
#     return jsonify(utils.count_cart(cart))
#
#
# if __name__ == "__main__":
#     app.run(debug=True)


@app.route("/")
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    page = request.args.get('page', 1)

    products = utils.load_products(cate_id=cate_id, kw=kw, page=int(page))
    counter = utils.count_products()

    return render_template('index.html',
                           products=products,
                           pages=math.ceil(counter / app.config['PAGE_SIZE'])
                           )


@app.route('/register', methods=['get', 'post'])
def user_register():
    err_msg = ""
    if request.method.__eq__('POST'):
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        confirm = request.form.get('confirm')
        avatar_path = None
        try:
            if password.strip().__eq__(confirm.strip()):
                avatar = request.files.get('avatar')
                if avatar:
                    res = cloudinary.uploader.upload(avatar)
                    avatar_path = res['secure_url']

                utils.add_user(name=name, username=username, password=password,
                               email=email, avatar=avatar_path)
                return redirect(url_for('user_signin'))
            else:
                err_msg = 'Mat khau khong khop!'
        except Exception as ex:
            err_msg = 'He thong dang co loi!!' + str(ex)
    return render_template('register.html ', err_msg=err_msg)


@app.route('/user-login', methods=['get', 'post'])
def user_signin():
    err_msg = ''
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = utils.check_login(username=username, password=password)

        if user:
            login_user(user=user)
            return redirect(url_for(request.args.get('next', 'index')))
        else:
            err_msg = 'username hoac password khong chinh xac!!!'

    return render_template('login.html', err_msg=err_msg)


@app.route('/user-logout')
def user_signout():
    logout_user()
    return redirect(url_for('user_signin'))


@app.route('/admin-login', methods=['post'])
def signin_admin():
    username = request.form['username']
    password = request.form['password']

    user = utils.check_login(username=username,
                             password=password,
                             role=UserRole.ADMIN)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.context_processor
def common_response():
    return {
        'categories': utils.load_categories(),
        'cart_stats': utils.count_cart(session.get('cart'))
    }


@app.route("/products")
def product_list():
    cate_id = request.args.get("categories_id")
    products = utils.load_products(cate_id=cate_id)
    kw = request.args.get("keyword")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")
    products = utils.load_products(cate_id=cate_id,
                                   kw=kw,
                                   from_price=from_price,
                                   to_price=to_price)
    return render_template('products.html', products=products)


@login.user_loader
def user_load(user_id):
    return utils.get_user_by_id(user_id=user_id)


@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = utils.get_product_by_id(product_id)
    comments = utils.get_comment(product_id=product_id, page=int(request.args.get('page', 1)))
    return render_template('product_detail.html', comments=comments, product=product, page=math.ceil(utils.count_comment(product_id=product_id)/app.config['COMMENT_SIZE']))


@app.route('/cart')
def cart():
    return render_template('cart.html', stats=utils.count_cart(session.get('cart')))


@app.route('/api/add-cart', methods=['post'])
def add_to_cart():
    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')
    cart = session.get('cart')
    if not cart:
        cart = {}

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            'id': id,
            'name': name,
            'price': price,
            'quantity': 1
        }
    session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/update-cart', methods=['put'])
def update_cart():
    data = request.json
    id = str(data.get('id'))
    quantity = data.get('quantity')

    cart = session.get('cart')
    if cart and id in cart:
        cart[id]['quantity'] = quantity
        session['cart'] = cart
    # key = app.config['CART_KEY']
    # cart = session.get(key)
    #
    # if cart and product_id in cart:
    #     cart[product_id]['quantity'] = int(request.json['quantity'])
    #
    # session[key] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/delete-cart/<product_id>', methods=['delete'])
def delete_cart(product_id):
    cart = session.get('cart')

    if cart and product_id in cart:
        del cart[product_id]
        session['cart'] = cart

    return jsonify(utils.count_cart(cart))


@app.route('/api/pay', methods=['post'])
@login_required
def pay():
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 404})

    return jsonify({'code': 200})


@app.route('/api/pay1', methods=['post'])
@login_required
def pay1():
    try:
        utils.add_receipt_online(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 404})

    return jsonify({'code': 200})


@app.route('/info')
@login_required
def info():
    return render_template('info.html')


@app.route('/api/getinfo',  methods=['post'])
def get_info():
    try:
        utils.add_receipt(session.get('cart'))
        del session['cart']
    except:
        return jsonify({'code': 404})

    return jsonify({'code': 200})


@app.route('/api/comments', methods=['post'])
@login_required
def add_comment():
    data = request.json
    content = data.get('content')
    product_id = data.get('product_id')

    try:
        c = utils.add_comment(content=content, product_id=product_id)
    except:
        return {'status': 404, 'err_msg': 'Chuong trinh dang bi loi!!'}

    return {'status': 201, 'comment': {
        'id': c.id,
        'content': c.content,
        'created_date': c.created_date,
        'user': {
            'username': current_user.username,
            'avatar': current_user.avatar
        }
    }}


if __name__ == "__main__":
    app.run(debug=True)
