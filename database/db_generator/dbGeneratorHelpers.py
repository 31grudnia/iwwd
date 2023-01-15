from database.models.UserModel import User as UserModel
from database.models.SubcategoryModel import Subcategory as SubcategoryModel
from database.models.CategoryModel import Category as CategoryModel
from database.models.BrandModel import Brand as BrandModel
from database.models.ProductModel import Product as ProductModel
from database.models.BreedModel import Breed as BreedModel
from database.models.ProductImageModel import ProductImage as ProductImageModel
from database.models.AnimalModel import Animal as AnimalModel
from database.models.WalkModel import Walk as WalkModel
from database.models.PinModel import Pin as PinModel
from database.models.StatusModel import Status as StatusModel
from database.models.PaymentMethodModel import PaymentMethod as PaymentMethodModel
from database.models.OrderModel import Order as OrderModel
from database.models.OrderProductModel import OrderProduct as OrderProductModel
from database.models.PostOfficeAddressModel import PostOfficeAddress as PostOfficeAddressModel
from database.models.PostOfficeModel import PostOffice as PostOfficeModel
from database.models.PostOfficeWorkTimeModel import PostOfficeWorkTime as PostOfficeWorkTimeModel
from database.models.DeliveryMethodModel import DeliveryMethod as DeliveryMethodModel

from sqlalchemy.orm import Session
from faker import Faker

from static.animal_static.breed_static import STATIC_BREEDS
from helpers.passwordHelpers import get_password_hash
from helpers.productHelpers import calculate_product_price
from database.firebase_setup import DEFAULT_USER_IMAGES, DEFAULT_BRAMD_IMAGES, DEFAULT_PRODUCT_IMAGE, \
    DEFAULT_ANIMAL_IMAGE
from static.order_static.delivery_static import DELIVERY_METHOD_STATIC
from static.order_static.payment_method_static import PAYMENT_METHOD_STATIC
from static.order_static.post_office_work_time_static import POST_OFFCIE_WORK_TIME_STATIC
from static.order_static.status_static import STATIC_STATUS

fake = Faker()

"""
    FAKER GENERATOR 
"""


# Generate a list of records to insert into the database
def generate_all_records(db: Session, n: int):
    CATEGORIES = ["food", "toy"]
    TYPE = ["dog", "cat"]
    SUBCATEGORIES = ["adult food", "training", "child food", "plushies"]
    BRANDS = ["royal horse", "cats among us", "Silence of the dogs"]
    sex = ["Male", "Female"]

    Faker.seed(0)
    for i in STATIC_BREEDS:
        db_breed = BreedModel(name=i)
        db.add(db_breed)
    db.commit()

    Faker.seed(0)
    for i in range(n):
        db_user = UserModel(name=fake.name(), surname=fake.last_name(), email=fake.unique.ascii_email(),
                            phone_number=str(fake.unique.msisdn()), login=fake.unique.user_name(),
                            password=get_password_hash(str(i)), photo_url=DEFAULT_USER_IMAGES[i%2],
                            coins=0, favourites=[])
        db.add(db_user)
    db.commit()

    Faker.seed(0)
    for i in range(n):
        db_animal = AnimalModel(name=fake.last_name_nonbinary().title(), sex=sex[i % 2],
                                weight=fake.pyfloat(left_digits=2, right_digits=2, positive=True,
                                                    min_value=5, max_value=30),
                                height=fake.pyfloat(left_digits=1, right_digits=2, positive=True,
                                                    min_value=0.01, max_value=1),
                                photo_url=DEFAULT_ANIMAL_IMAGE, bio=fake.paragraph(nb_sentences=3), pins=[],
                                user_id=i+1, breed_id=fake.random_int(min=2, max=270), birth_date=fake.date())
        db.add(db_animal)
    db.commit()

    Faker.seed(0)
    for j in range(2):
        for i in range(n):
            db_walk = WalkModel(time=fake.time(), distance=fake.pyfloat(left_digits=2, right_digits=2, positive=True,
                                                    min_value=5, max_value=30),
                                coins_gained=fake.random_int(min=10, max=1000), animals_id=[i+1], user_id=i+1, photo=[])
            db.add(db_walk)
    db.commit()

    Faker.seed(0)
    for j in range(2):
        for i in range(n):
            db_pin = PinModel(name=fake.street_name(), latitude=fake.latitude(), longtitude=fake.longitude(),
                              description=fake.paragraph(nb_sentences=1),
                              user_id=i+1, animal_id=i+1)
            db.add(db_pin)
    db.commit()

    Faker.seed(0)
    for i in range(len(STATIC_STATUS)):
        db_status = StatusModel(name=STATIC_STATUS[i])
        db.add(db_status)
    db.commit()

    Faker.seed(0)
    for i in range(len(CATEGORIES)):
        db_category = CategoryModel(name=CATEGORIES[i].title())
        db.add(db_category)
    db.commit()

    for i in range(len(SUBCATEGORIES)):
        db_subcat = SubcategoryModel(name=SUBCATEGORIES[i].title(), category_id=i % 2 + 1)
        db.add(db_subcat)
    db.commit()

    for i in range(len(BRANDS)):
        db_brand = BrandModel(name=BRANDS[i].title(), photo=DEFAULT_BRAMD_IMAGES[i],
                              description=fake.paragraph(nb_sentences=4))
        db.add(db_brand)
    db.commit()

    Faker.seed(0)
    for i in range(n+10):
        db_product = ProductModel(title=fake.text(max_nb_chars=20).title(),
                                  short_description=fake.paragraph(nb_sentences=1),
                                  long_description=fake.paragraph(nb_sentences=4),
                                  base_price=fake.pyint(min_value=20, max_value=300),
                                  discount_price=fake.pyint(min_value=0, max_value=5),
                                  discount_amount=fake.pyint(min_value=0, max_value=2),
                                  rate=fake.pyint(min_value=0, max_value=5), ingredients=fake.paragraph(nb_sentences=1),
                                  dosage=fake.paragraph(nb_sentences=1), type=TYPE[i % 2].title(), subcategory_id=
                                  fake.pyint(min_value=1, max_value=4), brand_id=fake.pyint(min_value=1, max_value=3),
                                  amount=fake.pyint(min_value=10, max_value=100))
        db_product.price = calculate_product_price(base_price=db_product.base_price,
                                                   discount_price=db_product.discount_price,
                                                   discount_amount=db_product.discount_amount)
        db.add(db_product)
    db.commit()

    for i in range(n):
        db_product_image = ProductImageModel(photo_url=DEFAULT_PRODUCT_IMAGE, product_id=i + 1)
        db.add(db_product_image)
    db.commit()

    for i in range(len(PAYMENT_METHOD_STATIC)):
        db_payment_method = PaymentMethodModel(name=PAYMENT_METHOD_STATIC[i], photo_url="https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/payment_method_images%2FPayment_method_placeholder.png?alt=media&token=46e3488b-9b42-47e3-82c5-ad10ce5f0d84")
        db.add(db_payment_method)
    db.commit()

    Faker.seed(0)
    for i in range(n):
        db_order = OrderModel(order_code=fake.isbn13(), city=fake.city(), street=fake.street_name(),
                              home_number=fake.building_number(), post_code=fake.postcode(), status_id=1,
                              payment_method_id=1, user_id=i+1)
        db.add(db_order)
    db.commit()

    for j in range(2):
        for i in range(n):
            db_order_product = OrderProductModel(order_id=i+1, product_id=i+j+1,
                                                 amount=i+j+1)
            db.add(db_order_product)

    db.commit()

    Faker.seed(0)
    for i in range(n*3):
        db_po_address = PostOfficeAddressModel(city=fake.city(), street=fake.street_name(), longtitude=fake.longitude(),
                                               building_number=fake.building_number(), latitude=fake.latitude())
        db.add(db_po_address)
    db.commit()

    Faker.seed(0)
    for i in range(n):
        db_post_office = PostOfficeModel(name=fake.street_name(), order_id=i+1, post_office_address_id=i+1)
        db.add(db_post_office)
    db.commit()

    for i in range(len(POST_OFFCIE_WORK_TIME_STATIC)):
        for j in range(n):
            db_po_work_time = PostOfficeWorkTimeModel(name=POST_OFFCIE_WORK_TIME_STATIC[i], work_time="07:00 - 23:00",
                                                      post_office_id=j+1)
            db.add(db_po_work_time)
    db.commit()

    Faker.seed(0)
    for i in range(len(DELIVERY_METHOD_STATIC)):
        db_delivery_method = DeliveryMethodModel(name=DELIVERY_METHOD_STATIC[i], logo="https://firebasestorage.googleapis.com/v0/b/iwwd-77dbe.appspot.com/o/delivery_method_images%2FDelivery_method_placeholder.png?alt=media&token=1fdd2ee5-bcc5-48be-9737-c3eed31bc033"
                                                 , delivery_payment=5.00,
                                                 delivery_time=fake.date_this_month(before_today=False, after_today=True),
                                                 postal_points=[i, i+1, i+2])
        db.add(db_delivery_method)
    db.commit()