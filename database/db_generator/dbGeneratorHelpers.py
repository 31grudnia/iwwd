from database.models.UserModel import User as UserModel
from database.models.SubcategoryModel import Subcategory as SubcategoryModel
from database.models.CategoryModel import Category as CategoryModel
from database.models.BrandModel import Brand as BrandModel
from database.models.ProductModel import Product as ProductModel
from sqlalchemy.orm import Session

from faker import Faker

from helpers.passwordHelpers import get_password_hash
from helpers.productHelpers import calculate_product_price
from database.firebase_setup import DEFAULT_USER_IMAGES, DEFAULT_BRAMD_IMAGES

fake = Faker()

"""
    FAKER GENERATOR 
"""


# Generate a list of records to insert into the database
def generate_user_records(db: Session, n: int):
    Faker.seed(0)
    for i in range(n):
        db_user = UserModel(name=fake.name(), surname=fake.last_name(), email=fake.unique.ascii_email(),
                            phone_number=str(fake.unique.msisdn()), login=fake.unique.user_name(),
                            password=get_password_hash(str(i)), photo_url=DEFAULT_USER_IMAGES[i%2], is_admin=False, coins=0, favourites=[],
                            disabled=False)
        db.add(db_user)
    db.commit()
    return True


def generate_product_records(db: Session, n: int):
    Faker.seed(0)
    CATEGORIES = ["food", "toy"]
    TYPE = ["dog", "cat"]
    SUBCATEGORIES = ["adult food", "training", "child food", "plushies"]
    BRANDS = ["royal horse", "cats among us", "Silence of the dogs"]

    for i in range(len(CATEGORIES)):
        db_category = CategoryModel(name=CATEGORIES[i].title())
        db.add(db_category)
    db.commit()

    for i in range(len(SUBCATEGORIES)):
        db_subcat = SubcategoryModel(name=SUBCATEGORIES[i].title(), category_id=i%2+1)
        db.add(db_subcat)
    db.commit()

    for i in range(len(BRANDS)):
        db_brand = BrandModel(name=BRANDS[i].title(), photo=DEFAULT_BRAMD_IMAGES[i],
                              description=fake.paragraph(nb_sentences=4))
        db.add(db_brand)
    db.commit()

    for i in range(n):
        db_product = ProductModel(title=fake.text(max_nb_chars=20).title(), short_description=fake.paragraph(nb_sentences=1),
                                  long_description=fake.paragraph(nb_sentences=4), base_price=fake.pyint(min_value=20, max_value=300),
                                  discount_price=fake.pyint(min_value=0, max_value=5), discount_amount=fake.pyint(min_value=0, max_value=2),
                                  rate=fake.pyint(min_value=0, max_value=5), ingredients=fake.paragraph(nb_sentences=1),
                                  dosage=fake.paragraph(nb_sentences=1), type=TYPE[i%2].title(), subcategory_id=
                                  fake.pyint(min_value=1, max_value=4), brand_id=fake.pyint(min_value=1, max_value=3))
        db_product.price = calculate_product_price(base_price=db_product.base_price, discount_price=db_product.discount_price,
                                                   discount_amount=db_product.discount_amount)
        db.add(db_product)
    db.commit()




