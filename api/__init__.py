"""API route registration."""

from fastapi import APIRouter

from api.generate import router as generate_router
from api.health import router as health_router
from api.keys import router as keys_router
from api.providers import router as providers_router
from api.templates import router as templates_router

router = APIRouter()
router.include_router(generate_router, tags=["Generation"])
router.include_router(templates_router, tags=["Templates"])
router.include_router(keys_router, tags=["API Keys"])
router.include_router(providers_router, tags=["Providers"])
router.include_router(health_router, tags=["Health"])
