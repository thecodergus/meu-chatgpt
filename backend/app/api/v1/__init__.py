# Versão 1 da API.
# Contém os endpoints principais da primeira versão da API.

from fastapi import APIRouter
from . import health

router = APIRouter()
router.include_router(health.router)
