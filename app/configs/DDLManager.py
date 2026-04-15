from sqlalchemy.ext.asyncio import AsyncEngine
from app.configs.Settings import get_settings, DDLAutoOption
from app.configs.Database import Base


async def apply_ddl(engine: AsyncEngine | None) -> None:
    """Aplica a estratégia de ALEMBIC_DDL_AUTO no banco."""
    if engine is None:
        return
    settings = get_settings()

    if settings.ALEMBIC_DDL_AUTO == DDLAutoOption.CREATE:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    elif settings.ALEMBIC_DDL_AUTO == DDLAutoOption.UPDATE:
        await _run_alembic_upgrade(engine)


async def _run_alembic_upgrade(engine: AsyncEngine):
    def upgrade(connection):
        from alembic.migration import MigrationContext
        from alembic.autogenerate import compare_metadata
        from alembic.operations import Operations

        context = MigrationContext.configure(connection)

        # 1. Obter diferenças entre o banco atual e o mapeamento das classes
        diffs = compare_metadata(context, Base.metadata)

        if not diffs:
            return

        # 2. Injetar as modicacoes faltantes dinamicamente
        op = Operations(context)
        for diff in diffs:
            op_type = diff[0]
            try:
                if op_type == "add_column":
                    schema, tname, col = diff[1], diff[2], diff[3]
                    op.add_column(tname, col, schema=schema)

                elif op_type == "add_table":
                    table = diff[1]
                    table.create(connection)

            except Exception:
                raise

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(upgrade)
