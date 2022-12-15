from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from appbook import db, app
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum
#
#
# class BaseModel(db.Model):
#     __abstract__ = True
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#
#
# class UserRole(UserEnum):
#     ADMIN = 1
#     USER = 2
#
#
# class User(BaseModel, UserMixin):
#     name = Column(String(50), nullable=False)
#     username = Column(String(50), nullable=False, unique=True)
#     password = Column(String(50), nullable=False)
#     avatar = Column(String(100))
#     email = Column(String(50))
#     active = Column(Boolean, default=True)
#     joined_date = Column(DateTime, default=datetime.now())
#     user_role = Column(Enum(UserRole), default=UserRole.USER)
#
#     def __str__(self):
#         return self.name
#
#
# class Category(BaseModel):
#     __tablename__ = 'category'
#
#     name = Column(String(20), nullable=False)
#     products = relationship('Product', backref='category', lazy=True)
#
#     def __str__(self):
#         return self.name
#
#
# class Product(BaseModel):
#     __tablename__ = 'product'
#
#     name = Column(String(50), nullable=False)
#     description = Column(String(255))
#     price = Column(Float, default=0)
#     image = Column(String(100))
#     active = Column(Boolean, default=True)
#     created_date = Column(DateTime, default=datetime.now())
#     category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
#
#     def __str__(self):
#         return self.name
#
#
# with app.app_context():
#     if __name__ == '__main__':
#         db.create_all()
#
#


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class UserRole(UserEnum):
    ADMIN = 1
    USER = 2


class User(BaseModel, UserMixin):
    name = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    email = Column(String(50))
    active = Column(Boolean, default=True)
    joined_date = Column(DateTime, default=datetime.now())
    user_role = Column(Enum(UserRole), default=UserRole.USER)
    receipts = relationship('Receipt', backref='user', lazy=True)
    comments = relationship('Comment', backref='user', lazy=True)
    receipts_online = relationship('ReceiptOnline', backref='user', lazy=True)

    def __str__(self):
        return self.name


class Category(BaseModel):
    __tablename__ = 'category'

    name = Column(String(20), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Product(BaseModel):
    __tablename__ = 'product'
    name = Column(String(50), nullable=False)
    author = Column(String(50))
    description = Column(String(255))
    quantity = Column(Integer)
    price = Column(Float, default=0)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    receipt_details = relationship('ReceiptDetail', backref='product', lazy=True)
    comments = relationship('Comment', backref='product', lazy=True)
    receipt_details_online = relationship('ReceiptDetailOnline', backref='product', lazy=True)

    def __str__(self):
        return self.name


class Comment(BaseModel):
    content = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    created_date = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.content


class Receipt(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetail', backref='receipt', lazy=True)


class ReceiptDetail(db.Model):
    receipt_id = Column(Integer, ForeignKey(Receipt.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


class ReceiptOnline(BaseModel):
    created_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    details = relationship('ReceiptDetailOnline', backref='receipt_online', lazy=True)


class ReceiptDetailOnline(db.Model):
    receipt_online_id = Column(Integer, ForeignKey(ReceiptOnline.id), nullable=False, primary_key=True)
    product_id = Column(Integer, ForeignKey(Product.id), nullable=False, primary_key=True)
    quantity = Column(Integer, default=0)
    unit_price = Column(Float, default=0)


class UserInfo(BaseModel):
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    address = Column(String(255), nullable=False)
    phone = Column(Integer, nullable=False)


with app.app_context():
    if __name__ == '__main__':
        db.create_all()
    #
    # c1 = Category(name='Sách văn học')
    # c2 = Category(name='Sách thiếu nhi')
    # c3 = Category(name='Sách kinh tế')
    #
    # db.session.add(c1)
    # db.session.add(c2)
    # db.session.add(c3)
    #
    # db.session.commit()
    #
    # products =[{
    #             "id": 1,
    #             "name": "Nhà giả kim",
    #             "author": "Paulo Coelho",
    #             "description": "Nhà giả kim là tiểu thuyết được xuất bản lần đầu ở Brasil năm 1988, và là cuốn sách nổi tiếng nhất của nhà văn Paulo Coelho. Tác phẩm là một trong những cuốn sách bán chạy nhất mọi thời đại.",
    #             "price": 55000,
    #             "quantity": 300,
    #             "image": "image/p1.png",
    #             "category_id": 1
    #         }, {
    #             "id": 2,
    #             "name": "Hoàng tử bé",
    #             "author": "Antoine de Saint-Exupéry",
    #             "description": "Hoàng tử bé, được xuất bản năm 1943, là tiểu thuyết nổi tiếng nhất của nhà văn và phi công Pháp Antoine de Saint-Exupéry.",
    #             "price": 75000,
    #             "quantity": 300,
    #             "image": "image/p2.png",
    #             "category_id": 2
    #         }, {
    #             "id": 3,
    #             "name": "Tái tạo kép",
    #             "author": "Mark W. Johnson",
    #             "description": "Thị trường ngày nay liên tục thay đổi, các doanh nghiệp sinh ra và mất đi, và ngay cả các doanh nghiệp uy tín, lâu năm vẫn thường xuyên thất bại, thậm chí sụp đổ bởi những công nghệ đột phá.",
    #             "price": 128500,
    #             "quantity": 300,
    #             "image": "image/p3.png",
    #             "category_id": 3
    #             }]
    #
    # for p in products:
    #     pro = Product(name=p['name'], price=p['price'],
    #                   author=p['author'], quantity=p['quantity'], image=p['image'],
    #                   description=p['description'], category_id=p['category_id'])
    #     db.session.add(pro)
    #
    # db.session.commit()
    #
    #
    #
