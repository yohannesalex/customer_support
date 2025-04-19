from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from support_assistant_backend.routes.ai_route import router as ai_router
from support_assistant_backend.routes.auth_route import router as auth_router
from support_assistant_backend.routes.ticket_route import router as tickets_router

from support_assistant_backend.db.base_class import Base
from support_assistant_backend.db.session import async_engine, AsyncSessionLocal

from support_assistant_backend.schemas.users import UserCreate
from support_assistant_backend.services.auth_service import AuthService
import os

admin_email = os.getenv("ADMIN_EMAIL")
admin_password = os.getenv("ADMIN_PASS")

app = FastAPI(title="Customer Support API")

@app.on_event("startup")
async def on_startup():
    # 1) Create all tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 2) Seed the one admin user if not already present
    async with AsyncSessionLocal() as db:  
        svc = AuthService(db)
        existing = await svc.get_user_by_email(admin_email)
        if not existing:
            await svc.signup(
                UserCreate(
                    email= admin_email,
                    password= admin_password,
                    role="admin",
                )
            )


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include your routers
app.include_router(ai_router,      prefix="/tickets", tags=["tickets"])
app.include_router(auth_router,    prefix="/auth",    tags=["auth"])
app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "support_assistant_backend.main:app",
        host="0.0.0.0",
        port=9000,
        reload=True,
    )
