"""User, Animal

Revision ID: 8af18c4d5ff0
Revises: f6601f20d0ba
Create Date: 2022-10-13 15:41:05.712660

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8af18c4d5ff0'
down_revision = 'f6601f20d0ba'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animal', sa.Column('birth_date', sa.Date(), nullable=True))
    op.add_column('animal', sa.Column('sex', sa.String(length=6), nullable=True))
    op.add_column('animal', sa.Column('weight', sa.Float(), nullable=True))
    op.add_column('animal', sa.Column('height', sa.Float(), nullable=True))
    op.add_column('animal', sa.Column('photo', sa.String(length=50), nullable=True))
    op.add_column('animal', sa.Column('bio', sa.Text(), nullable=True))
    op.add_column('animal', sa.Column('pins', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('city', sa.String(length=30), nullable=True))
    op.add_column('user', sa.Column('email', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('age', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('phone_number', sa.String(length=15), nullable=True))
    op.add_column('user', sa.Column('login', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('password', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('photo', sa.String(length=50), nullable=True))
    op.add_column('user', sa.Column('regulations', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('sex', sa.String(length=6), nullable=True))
    op.add_column('user', sa.Column('hidden_posts', sa.Integer(), nullable=True))
    op.add_column('user', sa.Column('friends', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'user', ['login'])
    op.create_unique_constraint(None, 'user', ['phone_number'])
    op.create_unique_constraint(None, 'user', ['email'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_column('user', 'friends')
    op.drop_column('user', 'hidden_posts')
    op.drop_column('user', 'sex')
    op.drop_column('user', 'regulations')
    op.drop_column('user', 'photo')
    op.drop_column('user', 'password')
    op.drop_column('user', 'login')
    op.drop_column('user', 'phone_number')
    op.drop_column('user', 'age')
    op.drop_column('user', 'email')
    op.drop_column('user', 'city')
    op.drop_column('animal', 'pins')
    op.drop_column('animal', 'bio')
    op.drop_column('animal', 'photo')
    op.drop_column('animal', 'height')
    op.drop_column('animal', 'weight')
    op.drop_column('animal', 'sex')
    op.drop_column('animal', 'birth_date')
    # ### end Alembic commands ###
