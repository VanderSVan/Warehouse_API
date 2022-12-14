"""replace_warehouse_field_product_count_model

Revision ID: 7a5fb77d2394
Revises: 435c4a7e31d3
Create Date: 2022-09-18 12:58:45.105126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7a5fb77d2394'
down_revision = '435c4a7e31d3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_counts', sa.Column('warehouse_id', sa.Integer(), nullable=True))
    op.drop_constraint('product_counts_warehouse_group_id_fkey', 'product_counts', type_='foreignkey')
    op.create_foreign_key(None, 'product_counts', 'warehouse_groups', ['warehouse_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('product_counts', 'warehouse_group_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_counts', sa.Column('warehouse_group_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'product_counts', type_='foreignkey')
    op.create_foreign_key('product_counts_warehouse_group_id_fkey', 'product_counts', 'warehouse_groups', ['warehouse_group_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    op.drop_column('product_counts', 'warehouse_id')
    # ### end Alembic commands ###
