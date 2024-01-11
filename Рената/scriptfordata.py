from app import app
from models import db, Category, Products, User

with app.app_context():
    # Добавление категорий
    category_1 = Category(name="Блузки")
    category_2 = Category(name="Брюки")
    category_3 = Category(name="Джинсы")
    category_4 = Category(name="Купальники")
    category_5 = Category(name="Куртки")
    category_6 = Category(name="Пижамы")
    category_7 = Category(name="Платья")
    category_8 = Category(name="Толстовки")
    category_9 = Category(name="Футболки")
    category_10 = Category(name="Шорты")
    category_11 = Category(name="Юбки")

    db.session.add(category_1)
    db.session.add(category_2)
    db.session.add(category_3)
    db.session.add(category_4)
    db.session.add(category_5)
    db.session.add(category_6)
    db.session.add(category_7)
    db.session.add(category_8)
    db.session.add(category_9)
    db.session.add(category_10)
    db.session.add(category_11)

    db.session.commit()
    test = 'test'
    db.session.add(User(email=test, password=test, roll=test))

    # Получение добавленных категорий
    category_blouses = Category.query.filter_by(name="Блузки").first()
    category_trousers = Category.query.filter_by(name="Брюки").first()
    category_jeans = Category.query.filter_by(name="Джинсы").first()
    category_swimwear = Category.query.filter_by(name="Купальники").first()
    category_jackets = Category.query.filter_by(name="Куртки").first()
    category_pajamas = Category.query.filter_by(name="Пижамы").first()
    category_dresses = Category.query.filter_by(name="Платья").first()
    category_hoodies = Category.query.filter_by(name="Толстовки").first()
    category_tshirts = Category.query.filter_by(name="Футболки").first()
    category_shorts = Category.query.filter_by(name="Шорты").first()
    category_skirts = Category.query.filter_by(name="Юбки").first()

    # Добавление продуктов с соответствующими категориями

    # Блузки
    blouse_1 = Products(
        user_id=1,
        name="Блуза",
        category_id=category_blouses.id,
        image="static/images/blouse_1.jpg",
        price=44.99
    )
    db.session.add(blouse_1)

    blouse_2 = Products(
        user_id=1,
        name="Блуза",
        category_id=category_blouses.id,
        image="static/images/blouse_2.jpg",
        price=64.99
    )
    db.session.add(blouse_2)

    blouse_3 = Products(
        user_id=1,
        name="Блуза",
        category_id=category_blouses.id,
        image="static/images/blouse_3.jpg",
        price=54.99
    )
    db.session.add(blouse_3)

    # Брюки

    trousers_1 = Products(
        user_id=1,
        name="Брюки Vittoria Vicci",
        category_id=category_trousers.id,
        image="static/images/trousers_1.jpg",
        price=74.99
    )
    db.session.add(trousers_1)

    trousers_2 = Products(
        user_id=1,
        name="Брюки Volento",
        category_id=category_trousers.id,
        image="static/images/trousers_2.jpg",
        price=94.99
    )
    db.session.add(trousers_2)

    trousers_3 = Products(
        user_id=1,
        name="Брюки Giulia Rossi",
        category_id=category_trousers.id,
        image="static/images/trousers_3.jpg",
        price=84.99
    )
    db.session.add(trousers_3)

    trousers_4 = Products(
        user_id=1,
        name="Брюки Zarina",
        category_id=category_trousers.id,
        image="static/images/trousers_4.jpg",
        price=84.99
    )
    db.session.add(trousers_4)

    # Джинсы

    jeans_1 = Products(
        user_id=1,
        name="Джинсы Flare",
        category_id=category_jeans.id,
        image="static/images/jeans_1.jpg",
        price=44.99
    )
    db.session.add(jeans_1)

    jeans_2 = Products(
        user_id=1,
        name="Джинсы",
        category_id=category_jeans.id,
        image="static/images/jeans_2.jpg",
        price=64.99
    )
    db.session.add(jeans_2)

    jeans_3 = Products(
        user_id=1,
        name="Джинсы Wideleg Pure denim",
        category_id=category_jeans.id,
        image="static/images/jeans_3.jpg",
        price=74.99
    )
    db.session.add(jeans_3)

    # Купальники

    swimwear_1 = Products(
        user_id=1,
        name="Купальник Fila",
        category_id=category_swimwear.id,
        image="static/images/swimwear_1.jpg",
        price=34.99
    )
    db.session.add(swimwear_1)

    swimwear_2 = Products(
        user_id=1,
        name="Купальник Karra",
        category_id=category_swimwear.id,
        image="static/images/swimwear_2.jpg",
        price=34.99
    )
    db.session.add(swimwear_2)

    swimwear_3 = Products(
        user_id=1,
        name="Купальник Swim Suit",
        category_id=category_swimwear.id,
        image="static/images/swimwear_3.jpg",
        price=44.99
    )
    db.session.add(swimwear_3)

    # Куртки

    jackets_1 = Products(
        user_id=1,
        name="Куртка утепленная",
        category_id=category_jackets.id,
        image="static/images/jackets_1.jpg",
        price=144.99
    )
    db.session.add(jackets_1)

    jackets_2 = Products(
        user_id=1,
        name="Куртка утепленная",
        category_id=category_jackets.id,
        image="static/images/jackets_2.jpg",
        price=124.99
    )
    db.session.add(jackets_2)

    jackets_3 = Products(
        user_id=1,
        name="Куртка утепленная Sela",
        category_id=category_jackets.id,
        image="static/images/jackets_3.jpg",
        price=74.99
    )
    db.session.add(jackets_3)

    # Пижамы

    pajamas_1 = Products(
        user_id=1,
        name="Пижама",
        category_id=category_pajamas.id,
        image="static/images/pajamas_1.jpg",
        price=74.99
    )
    db.session.add(pajamas_1)

    pajamas_2 = Products(
        user_id=1,
        name="Пижама Атласная в сердечко",
        category_id=category_pajamas.id,
        image="static/images/pajamas_2.jpg",
        price=154.99
    )
    db.session.add(pajamas_2)

    pajamas_3 = Products(
        user_id=1,
        name="Пижама",
        category_id=category_pajamas.id,
        image="static/images/pajamas_3.jpg",
        price=144.99
    )
    db.session.add(pajamas_3)

    # Платья

    dresses_1 = Products(
        user_id=1,
        name="Платье",
        category_id=category_dresses.id,
        image="static/images/dresses_1.jpg",
        price=134.99
    )
    db.session.add(dresses_1)

    dresses_2 = Products(
        user_id=1,
        name="Платье",
        category_id=category_dresses.id,
        image="static/images/dresses_2.jpg",
        price=114.99
    )
    db.session.add(dresses_2)

    dresses_3 = Products(
        user_id=1,
        name="Платье",
        category_id=category_dresses.id,
        image="static/images/dresses_3.jpg",
        price=84.99
    )
    db.session.add(dresses_3)

    # Толстовки

    hoodies_1 = Products(
        user_id=1,
        name="Худи adidas",
        category_id=category_hoodies.id,
        image="static/images/hoodies_1.jpg",
        price=104.99
    )
    db.session.add(hoodies_1)

    hoodies_2 = Products(
        user_id=1,
        name="Худи HOODIE",
        category_id=category_hoodies.id,
        image="static/images/hoodies_2.jpg",
        price=94.99
    )
    db.session.add(hoodies_2)

    hoodies_3 = Products(
        user_id=1,
        name="Худи Lime",
        category_id=category_hoodies.id,
        image="static/images/hoodies_3.jpg",
        price=64.99
    )
    db.session.add(hoodies_3)

    # Футболки

    tshirts_1 = Products(
        user_id=1,
        name="Футболка",
        category_id=category_tshirts.id,
        image="static/images/tshirts_1.jpg",
        price=44.99
    )
    db.session.add(tshirts_1)

    tshirts_2 = Products(
        user_id=1,
        name="Футболка",
        category_id=category_tshirts.id,
        image="static/images/tshirts_2.jpg",
        price=34.99
    )
    db.session.add(tshirts_2)

    tshirts_3 = Products(
        user_id=1,
        name="Футболка Тай Дай",
        category_id=category_tshirts.id,
        image="static/images/tshirts_3.jpg",
        price=34.99
    )
    db.session.add(tshirts_3)

    # Шорты

    shorts_1 = Products(
        user_id=1,
        name="Шорты кожаные",
        category_id=category_shorts.id,
        image="static/images/shorts_1.jpg",
        price=54.99
    )
    db.session.add(shorts_1)

    shorts_2 = Products(
        user_id=1,
        name="Шорты",
        category_id=category_shorts.id,
        image="static/images/shorts_2.jpg",
        price=54.99
    )
    db.session.add(shorts_2)

    shorts_3 = Products(
        user_id=1,
        name="Шорты спортивные",
        category_id=category_shorts.id,
        image="static/images/shorts_3.jpg",
        price=44.99
    )
    db.session.add(shorts_3)

    # Юбки

    skirts_1 = Products(
        user_id=1,
        name="Юбка джинсовая",
        category_id=category_skirts.id,
        image="static/images/skirts_1.jpg",
        price=114.99
    )
    db.session.add(skirts_1)

    skirts_2 = Products(
        user_id=1,
        name="Юбка",
        category_id=category_skirts.id,
        image="static/images/skirts_2.jpg",
        price=54.99
    )
    db.session.add(skirts_2)

    skirts_3 = Products(
        user_id=1,
        name="Юбка",
        category_id=category_skirts.id,
        image="static/images/skirts_3.jpg",
        price=64.99
    )
    db.session.add(skirts_3)

    db.session.commit()
