import json
import logging.config

import uvicorn
from fastapi import FastAPI

from config.db import init_tables
from users.router import router


app = FastAPI()


@app.on_event("startup")
async def init_db():
    await init_tables()

@app.get('/')
def main():
    return {'Message': 'Hello Dance'}


logger_config_file = open('./config/logger.json')
logging.config.dictConfig(json.load(logger_config_file))

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
