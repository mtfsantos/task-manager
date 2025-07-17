import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Adicionar o caminho do diretório 'app' ao sys.path para que as importações funcionem
# Este passo é crucial para que 'app.db.base' e 'app.core.config' sejam encontrados.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importar o Base do seu models.py
from app.db.base import Base
# Importar as configurações para pegar a DATABASE_URL
from app.core.config import settings

import app.db.models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata # AQUI: Diga ao Alembic qual MetaData usar para detectar mudanças


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an actual Engine, though an Engine is thoroughly
    tested out in the methods in this module.
    """
    # Usar a DATABASE_URL do seu settings para o modo offline
    url = settings.DATABASE_URL
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.
    """
    # Usar a DATABASE_URL do seu settings para o modo online
    connectable = engine_from_config(
        {"sqlalchemy.url": settings.DATABASE_URL}, # Passar a URL via config dictionary
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True # Adicionar para autogenerate ser mais preciso com tipos
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
