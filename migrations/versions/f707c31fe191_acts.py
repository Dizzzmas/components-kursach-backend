"""Add Act model

Revision ID: f707c31fe191
Revises: 07546bcf6728
Create Date: 2021-05-24 23:52:54.765920

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "f707c31fe191"
down_revision = "07546bcf6728"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "act",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "extid",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("uuid_generate_v4()"),
            nullable=False,
        ),
        sa.Column(
            "type",
            sa.Enum("marriage", "birth", "death", name="acttype"),
            nullable=False,
        ),
        sa.Column("issued_by", sa.Integer(), nullable=True),
        sa.Column("issued_at", sa.Date(), nullable=True),
        sa.Column("created_by_id", sa.Integer(), nullable=True),
        sa.Column("father_id", sa.Integer(), nullable=True),
        sa.Column("mother_id", sa.Integer(), nullable=True),
        sa.Column("child_id", sa.Integer(), nullable=True),
        sa.Column("birthplace", sa.Text(), nullable=True),
        sa.Column("child_nationality", sa.Text(), nullable=True),
        sa.Column("deceased_id", sa.Integer(), nullable=True),
        sa.Column("deceased_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deceased_age", sa.Integer(), nullable=True),
        sa.Column("place_of_demise", sa.Text(), nullable=True),
        sa.Column("bride_id", sa.Integer(), nullable=True),
        sa.Column("groom_id", sa.Integer(), nullable=True),
        sa.Column("groom_last_name", sa.Text(), nullable=True),
        sa.Column("bride_last_name", sa.Text(), nullable=True),
        sa.Column("wed_at", sa.Date(), nullable=True),
        sa.ForeignKeyConstraint(["bride_id"], ["person.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["child_id"], ["person.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by_id"], ["user.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["deceased_id"], ["person.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["father_id"], ["person.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["groom_id"], ["person.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["mother_id"], ["person.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_act_extid"), "act", ["extid"], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_act_extid"), table_name="act")
    op.drop_table("act")
    # ### end Alembic commands ###
