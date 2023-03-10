"""
init

Revision ID:275f4df1dc0b
Revises:
Create Date:2023-01-28 06:30:16.371691
"""

import sqlalchemy as sa
from alembic import op

from models.currency import Currency

# revision identifiers, used by Alembic.
revision = '275f4df1dc0b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'currencies',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('char_code', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('char_code'),
    )
    op.bulk_insert(
        Currency.__table__,
        [
            {'id': 1, 'char_code': 'aud'},
            {'id': 2, 'char_code': 'azn'},
            {'id': 3, 'char_code': 'gbp'},
            {'id': 4, 'char_code': 'amd'},
            {'id': 5, 'char_code': 'byn'},
            {'id': 6, 'char_code': 'bgn'},
            {'id': 7, 'char_code': 'brl'},
            {'id': 8, 'char_code': 'huf'},
            {'id': 9, 'char_code': 'vnd'},
            {'id': 10, 'char_code': 'hkd'},
            {'id': 11, 'char_code': 'gel'},
            {'id': 12, 'char_code': 'dkk'},
            {'id': 13, 'char_code': 'aed'},
            {'id': 14, 'char_code': 'usd'},
            {'id': 15, 'char_code': 'eur'},
            {'id': 16, 'char_code': 'egp'},
            {'id': 17, 'char_code': 'inr'},
            {'id': 18, 'char_code': 'idr'},
            {'id': 19, 'char_code': 'kzt'},
            {'id': 20, 'char_code': 'cad'},
            {'id': 21, 'char_code': 'qar'},
            {'id': 22, 'char_code': 'kgs'},
            {'id': 23, 'char_code': 'cny'},
            {'id': 24, 'char_code': 'mdl'},
            {'id': 25, 'char_code': 'nzd'},
            {'id': 26, 'char_code': 'nok'},
            {'id': 27, 'char_code': 'pln'},
            {'id': 28, 'char_code': 'ron'},
            {'id': 29, 'char_code': 'jpy'},
            {'id': 30, 'char_code': 'sgd'},
            {'id': 31, 'char_code': 'tjs'},
            {'id': 32, 'char_code': 'thb'},
            {'id': 33, 'char_code': 'tmt'},
            {'id': 34, 'char_code': 'uzs'},
            {'id': 35, 'char_code': 'uah'},
            {'id': 36, 'char_code': 'czk'},
            {'id': 37, 'char_code': 'sek'},
            {'id': 38, 'char_code': 'chf'},
            {'id': 39, 'char_code': 'rsd'},
            {'id': 40, 'char_code': 'zar'},
            {'id': 41, 'char_code': 'krw'},
        ],
    )
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger(), autoincrement=False, nullable=False),
        sa.Column('first_name', sa.String(), nullable=True),
        sa.Column('last_name', sa.String(), nullable=True),
        sa.Column('username', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=True)
    op.create_table(
        'currency_users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=True),
        sa.Column('currency_id', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ['currency_id'],
            ['currencies.id'],
        ),
        sa.ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    op.drop_table('currency_users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_table('currencies')
