"""initial schema

Revision ID: 0001_initial
Revises: 
Create Date: 2026-02-23
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("users",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("tg_user_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=64)),
        sa.Column("first_name", sa.String(length=128)),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_banned", sa.Boolean(), nullable=False, server_default=sa.text("0")),
        sa.Column("flags", sa.JSON(), nullable=False),
        sa.UniqueConstraint("tg_user_id"),
    )
    op.create_index("ix_users_tg_user_id", "users", ["tg_user_id"])

    op.create_table("chats",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("tg_chat_id", sa.BigInteger(), nullable=False),
        sa.Column("title", sa.String(length=255)),
        sa.Column("type", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("settings", sa.JSON(), nullable=False),
        sa.UniqueConstraint("tg_chat_id"),
    )
    op.create_index("ix_chats_tg_chat_id", "chats", ["tg_chat_id"])

    op.create_table("topics",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text()),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.UniqueConstraint("slug"),
    )

    op.create_table("questions",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("topic_id", sa.Integer(), sa.ForeignKey("topics.id"), nullable=False),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("difficulty", sa.Enum("easy", "medium", "hard", name="difficulty"), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=False),
        sa.Column("correct_index", sa.Integer(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("tags", sa.JSON(), nullable=False),
        sa.Column("source", sa.Enum("bank", "llm", name="questionsource"), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("1")),
        sa.UniqueConstraint("content_hash"),
    )

    op.create_table("game_sessions",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("mode", sa.Enum("solo", "group", "duel", "tournament", name="gamemode"), nullable=False),
        sa.Column("chat_id", sa.BigInteger(), sa.ForeignKey("chats.id")),
        sa.Column("topic_id", sa.Integer(), sa.ForeignKey("topics.id")),
        sa.Column("language", sa.String(length=8), nullable=False),
        sa.Column("difficulty", sa.Enum("easy", "medium", "hard", name="difficulty"), nullable=False),
        sa.Column("status", sa.Enum("active", "finished", "cancelled", name="sessionstatus"), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ended_at", sa.DateTime(timezone=True)),
        sa.Column("config", sa.JSON(), nullable=False),
    )
    op.create_index("ix_game_sessions_status", "game_sessions", ["status"])
    op.create_index("ix_game_sessions_started_at", "game_sessions", ["started_at"])

    op.create_table("session_players",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.BigInteger(), sa.ForeignKey("game_sessions.id"), nullable=False),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.Column("joined_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("left_at", sa.DateTime(timezone=True)),
        sa.Column("stats", sa.JSON(), nullable=False),
    )

    op.create_table("question_instances",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.BigInteger(), sa.ForeignKey("game_sessions.id"), nullable=False),
        sa.Column("question_id", sa.BigInteger(), sa.ForeignKey("questions.id"), nullable=False),
        sa.Column("order_index", sa.Integer(), nullable=False),
        sa.Column("shown_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("meta", sa.JSON(), nullable=False),
    )

    op.create_table("answers",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.BigInteger(), sa.ForeignKey("game_sessions.id"), nullable=False),
        sa.Column("question_instance_id", sa.BigInteger(), sa.ForeignKey("question_instances.id"), nullable=False),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("selected_index", sa.Integer(), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("answer_time_ms", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index("ix_answers_session_user", "answers", ["session_id", "user_id"])

    op.create_table("game_events",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("session_id", sa.BigInteger(), sa.ForeignKey("game_sessions.id")),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id")),
        sa.Column("chat_id", sa.BigInteger(), sa.ForeignKey("chats.id")),
        sa.Column("event_type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("idempotency_key", sa.String(length=128), nullable=False),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index("ix_game_events_created_at", "game_events", ["created_at"])
    op.create_index("ix_game_events_session_id", "game_events", ["session_id"])

    op.create_table("rating_events",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("chat_id", sa.BigInteger(), sa.ForeignKey("chats.id")),
        sa.Column("session_id", sa.BigInteger(), sa.ForeignKey("game_sessions.id")),
        sa.Column("delta_points", sa.Integer(), nullable=False),
        sa.Column("reason", sa.String(length=64), nullable=False),
        sa.Column("meta", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table("leaderboards_cache",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("scope", sa.String(length=16), nullable=False),
        sa.Column("scope_id", sa.String(length=64)),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("rank", sa.Integer(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table("prompt_logs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id")),
        sa.Column("chat_id", sa.BigInteger(), sa.ForeignKey("chats.id")),
        sa.Column("session_id", sa.BigInteger(), sa.ForeignKey("game_sessions.id")),
        sa.Column("prompt_version", sa.String(length=32), nullable=False),
        sa.Column("params", sa.JSON(), nullable=False),
        sa.Column("prompt_text", sa.Text(), nullable=False),
        sa.Column("raw_response", mysql.MEDIUMTEXT(), nullable=False),
        sa.Column("parsed_response", sa.JSON()),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("latency_ms", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table("moderation_flags",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("question_id", sa.BigInteger(), sa.ForeignKey("questions.id")),
        sa.Column("session_id", sa.BigInteger(), sa.ForeignKey("game_sessions.id")),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id")),
        sa.Column("chat_id", sa.BigInteger(), sa.ForeignKey("chats.id")),
        sa.Column("type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True)),
    )

    op.create_table("achievements",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=128), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.UniqueConstraint("code"),
    )

    op.create_table("user_achievements",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("achievement_id", sa.BigInteger(), sa.ForeignKey("achievements.id"), nullable=False),
        sa.Column("awarded_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),
    )

    op.create_table("jobs",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("type", sa.String(length=64), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(length=16), nullable=False),
        sa.Column("attempts", sa.Integer(), nullable=False),
        sa.Column("run_after", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_error", sa.Text()),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table("rate_limits",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("scope_key", sa.String(length=128), nullable=False),
        sa.Column("window_start", sa.DateTime(timezone=True), nullable=False),
        sa.Column("hits", sa.Integer(), nullable=False),
        sa.UniqueConstraint("scope_key", "window_start", name="uq_rate_scope_window"),
    )


def downgrade() -> None:
    for table in [
        "rate_limits", "jobs", "user_achievements", "achievements", "moderation_flags", "prompt_logs",
        "leaderboards_cache", "rating_events", "game_events", "answers", "question_instances",
        "session_players", "game_sessions", "questions", "topics", "chats", "users"
    ]:
        op.drop_table(table)
