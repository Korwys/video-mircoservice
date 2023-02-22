import json
import logging.config

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def main():
    return {'Message': 'Hello Dance'}


logger_config_file = open('./config/logger.json')
logging.config.dictConfig(json.load(logger_config_file))

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8080)
