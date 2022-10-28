from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from saleapp import db, app


class BaseModel(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)


class Category(BaseModel):
    __tablename__ = 'category'
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)


class Product(BaseModel):
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    description = Column(Text)
    image = Column(String(100))
    active = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)


if __name__ == '__main__':
    with app.app_context():
        # c1 = Category(name='Điện thoại')
        # c2 = Category(name='Máy tính bảng')
        # c3 = Category(name='Phụ kiện')
        #
        # db.session.add_all([c1, c2, c3])
        # db.session.commit()

        p1 = Product(name='Galaxy', price=31100000, description='Apple, 0311GB',
                     image='https:', category_id=1)
        p2 = Product(name='iPhone 12', price=28110000, description='Durian, 2811GB',
                     image='https:', category_id=2)

        db.session.add_all([p1, p2])
        db.session.commit()

        # db.create_all()
