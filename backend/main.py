from fastapi import FastAPI, Request
from app.api import conversation
from app.config import settings

app = FastAPI(title=settings.app_name, debug=settings.app_debug, 
               description="Autonomous agent: natural-language instruction in ",
               version="1.0.0")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[settings.frontend_url],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Adds a request ID header to every HTTP response for traceability.
# @app.middleware("http")
# async def request_id_middleware(request: Request, call_next):
#     request_id = request.headers.get("X-Request-ID", generate_request_id())
#     response = await call_next(request)
#     response.headers["X-Request-ID"] = request_id
#     return response

# Returns a lightweight health check for local dev and Docker health probes.
@app.get("/health")
async def health_check():
    return {"status": "ok", "app": settings.app_name}


app.include_router(conversation.router, prefix=settings.api_v1_prefix)
# app.include_router(auth.router, prefix=settings.api_v1_prefix)
# app.include_router(conversations.router, prefix=settings.api_v1_prefix)
# app.include_router(messages.router, prefix=settings.api_v1_prefix)
# app.include_router(models.router, prefix=settings.api_v1_prefix)
# app.include_router(model_runs.router, prefix=settings.api_v1_prefix)
# app.include_router(web_search.router, prefix=settings.api_v1_prefix)