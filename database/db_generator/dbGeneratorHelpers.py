from database.models.UserModel import User as UserModel
from sqlalchemy.orm import Session

from faker import Faker

from helpers.passwordHelpers import get_password_hash

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
                            password=get_password_hash(str(i)), photo_url=None, is_admin=False, coins=0, favourites=[],
                            disabled=False)
        db.add(db_user)
    db.commit()
    return True


