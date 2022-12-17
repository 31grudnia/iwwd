from database.models.UserModel import User as UserModel
from sqlalchemy.orm import Session

from faker import Faker

from helpers.passwordHelpers import get_password_hash


# Generate a list of records to insert into the database
def generate_user_records(db: Session, n: int):
    fake = Faker()
    Faker.seed(0)
    for i in range(n):
        db_user = UserModel(name=fake.name(), surname=fake.last_name(), email=fake.unique.ascii_email(),
                            phone_number=str(fake.unique.msisdn()), login=fake.unique.user_name(),
                            password=get_password_hash(str(i)), photo=None, is_admin=False, coins=0)
        db.add(db_user)
    db.commit()
    return True


