import uvicorn

def dev():
    """Servidor de desenvolvimento com hot-reload"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,
        reload=True,
        log_level="debug"
    )
def start():
    """Servidor de produção single-worker"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,
        log_level="info"
    )
def prod():
    """Servidor de produção multi-worker"""
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        workers=4,
        log_level="info"
    )
if __name__ == "__main__":
    dev()