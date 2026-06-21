"""
Prisma client singleton for CodeCache.
Provides async database access via Prisma ORM.
"""

import os
from prisma import Prisma

_prisma_client = None


def get_prisma() -> Prisma:
    """Get or create the Prisma client singleton."""
    global _prisma_client
    if _prisma_client is None:
        database_url = os.getenv('DATABASE_URL')
        _prisma_client = Prisma(datasource={'url': database_url})
    return _prisma_client


async def connect_prisma():
    """Connect to the database."""
    prisma = get_prisma()
    await prisma.connect()
    return prisma


async def disconnect_prisma():
    """Disconnect from the database."""
    global _prisma_client
    if _prisma_client:
        await _prisma_client.disconnect()
        _prisma_client = None
