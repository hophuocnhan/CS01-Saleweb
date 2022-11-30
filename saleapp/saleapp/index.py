from flask import render_template, request, redirect, session, jsonify
from saleapp import app, dao, admin, login, utils
from flask_login import login_user, logout_user, current_user, login_required
from saleapp.decorators import annoymous_user
import cloudinary.uploader


@app.route("/")
@login_required
def index():
    cate_id = request.args.get('category_id')
    kw = request.args.get('keyword')
    products = dao.load_products(cate_id, kw)
    return render_template('index.html', products=products)


@app.route('/products/<int:product_id>')
def details(product_id):
    p = dao.get_product_by_id(product_id)
    return render_template('details.html', product=p)


@app.route('/login-admin', methods=['post'])
def login_admin():
    username = request.form['username']
    password = request.form['password']

    user = dao.auth_user(username=username, password=password)
    if user:
        login_user(user=user)

    return redirect('/admin')


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method.__eq__('POST'):
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            avatar = ''
            if request.files:
                res = cloudinary.uploader.upload(request.files['image'])
                avatar = res['secure_url']
            try:
                dao.register(name=request.form['name'], username=request.form['username'], password=password,
                             image=avatar)
            except:
                err_msg = 'Hệ thống đang có lỗi! vui lòng quay lại sau!!'
        else:
            err_msg = 'Mật khẩu không khớp !!!'

    return render_template('register.html', err_msg=err_msg)


@app.route('/login', methods=['get', 'post'])
@annoymous_user
def login_my_user():
    # if current_user.is_authenticated:
    #     return redirect('/')
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            n = request.args.get("next")
            return redirect(n if n else '/')

    return render_template('login.html')


@app.route('/logout')
def logout_my_user():
    logout_user()
    return redirect('/login')


@app.route('/cart')
def cart():
    # session['cart'] = {
    #     "1": {
    #         "id": "1",
    #         "name": "Iphone 13",
    #         "price": 13000,
    #         "quantity": 1
    #     },
    #     "2": {
    #         "id": "2",
    #         "name": "Iphone 14",
    #         "price": 13000,
    #         "quantity": 1
    #     }
    # }
    return render_template('cart.html')


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    key = app.config['CART_KEY']
    cart = session[key] if key in session else {}
    data = request.json
    id = str(data['id'])
    name = data['name']
    price = data['price']
    if id in cart:
        cart[id]['quantity'] += 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }
    session[key] = cart
    return jsonify(utils.cart_stats(cart))


@app.context_processor
def common_attr():
    categories = dao.load_categories()
    return {
        'categories': categories,
        'cart': utils.cart_stats(session.get(app.config['CART_KEY']))
    }


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


if __name__ == "__main__":
    app.run(debug=True)
