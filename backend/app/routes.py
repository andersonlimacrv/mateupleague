from fastapi import FastAPI
from app.core.config import settings  
from app.routers.api_test import (
    ambiente, bomba_condensador, chiller, compressor, condensador,
    energia, linha_liquido, regime, regime_condensacao,
    ventilador_condensador, login
) 
from app.routers import ( users, auth, company, unidade, group )


def register_routes(app: FastAPI):
    
    app.include_router(users.router, tags=["Users 💁🏻‍♂️"], prefix="/users")
    app.include_router(auth.router, tags=["Auth 🔑"], prefix="/auth")
    app.include_router(company.router, tags=["Empresas 🏭"], prefix="/company")
    app.include_router(unidade.router, tags=["Unidades 🏢"], prefix="/unidade")
    app.include_router(group.router, tags=["Grupos 💼"], prefix="/group")

    if not settings.enable_api_test_routes:
        return  
    """ routes for api test readings """
    api_prefix = "/api"
    tag = "API Test - Leituras"
    app.include_router(ambiente.router, prefix=api_prefix, tags=[tag])
    app.include_router(bomba_condensador.router, prefix=api_prefix, tags=[tag])
    app.include_router(chiller.router, prefix=api_prefix, tags=[tag])
    app.include_router(compressor.router, prefix=api_prefix, tags=[tag])
    app.include_router(condensador.router, prefix=api_prefix, tags=[tag])
    app.include_router(energia.router, prefix=api_prefix, tags=[tag])
    app.include_router(linha_liquido.router, prefix=api_prefix, tags=[tag])
    app.include_router(regime.router, prefix=api_prefix, tags=[tag])
    app.include_router(regime_condensacao.router, prefix=api_prefix, tags=[tag])
    app.include_router(ventilador_condensador.router, prefix=api_prefix, tags=[tag])
    app.include_router(login.router, prefix=api_prefix, tags=[tag])

