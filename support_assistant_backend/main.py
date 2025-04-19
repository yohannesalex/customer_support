from fastapi import FastAPI
from support_assistant_backend.routes.ai_route import router as ai_roiuter
from support_assistant_backend.routes.auth_route import router as auth_router
from support_assistant_backend.routes.ticket_route import router as tickets_router
from fastapi.middleware.cors import CORSMiddleware  


app = FastAPI(title="Customer Support API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(ai_roiuter, prefix="/tickets", tags=["tickets"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tickets_router, prefix="/tickets", tags=["tickets"])
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9000)
