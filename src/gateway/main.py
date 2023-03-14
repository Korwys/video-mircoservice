import json
import logging.config

import uvicorn
from fastapi import FastAPI

from gateway.router import router

app = FastAPI()

logger_config_file = open('./config/logger.json')
logging.config.dictConfig(json.load(logger_config_file))

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7000)
