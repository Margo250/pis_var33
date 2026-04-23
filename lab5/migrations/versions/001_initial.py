"""initial migration

Revision ID: 001
Revises: 
Create Date: 2026-04-24

"""

from alembic import op
import sqlalchemy as sa


revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Таблица announcements
    op.create_table(
        'announcements',
        sa.Column('id', sa.String(36), nullable=False),
        sa.Column('group_id', sa.String(36), nullable=False),
        sa.Column('author_id', sa.String(36), nullable=False),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('content', sa.String(5000), nullable=False),
        sa.Column('status', sa.Enum('draft', 'scheduled', 'published', 'archived', name='status_enum'), 
                  nullable=False, server_default='draft'),
        sa.Column('attachments', sa.JSON, nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime, nullable=False),
        sa.Column('published_at', sa.DateTime, nullable=True),
        sa.Column('scheduled_for', sa.DateTime, nullable=True),
        sa.Column('updated_at', sa.DateTime, nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Индексы
    op.create_index('idx_announcements_group_id', 'announcements', ['group_id'])
    op.create_index('idx_announcements_author_id', 'announcements', ['author_id'])
    op.create_index('idx_announcements_status', 'announcements', ['status'])
    op.create_index('idx_announcements_created_at', 'announcements', ['created_at'])


def downgrade() -> None:
    op.drop_index('idx_announcements_created_at')
    op.drop_index('idx_announcements_status')
    op.drop_index('idx_announcements_author_id')
    op.drop_index('idx_announcements_group_id')
    op.drop_table('announcements')
    
    # Удаление Enum
    op.execute("DROP TYPE status_enum")
