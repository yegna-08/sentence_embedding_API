import configparser
import json
import logging.config
import socket
from typing import Any, Callable, Dict, List, Optional, Union

from fastapi import FastAPI, Request, Response
import numpy as np
import uvicorn

# Type alias for JSON
JSON = Dict[str, Any]

app = FastAPI()

async def get_valid_json(request: Request) -> Optional[JSON]:
    """Get the request data only if the data is a dict"""
    try:
        data = await request.json() # Can throw a ValueError if no data is passed in
        if not isinstance(data, dict):
            raise ValueError("Invalid type for JSON data")
        return data
    except ValueError:
        return None

@app.get('/')
def kubernetes_health_check():
    return {"status": "healthy"}

def generate_random_array(array_size: int, lower_bound: int, upper_bound: int) -> List[float]:
    """Generate random numbers using the array size and return them as list"""
    logger.info("Generating random array of size {} between {} and {}".format(array_size, lower_bound, upper_bound))
    random_array = np.random.uniform(low = lower_bound, high = upper_bound, size = array_size).tolist()
    return random_array

@app.post('/get_embeddings')
async def get_embeddings(request: Request) -> Union[str, JSON]:
    """
    Get an array of embeddings for the input sentence, as specified by the user.

    All parameters are optional.

    :return: (1) A message indicating that the input was incorrect
             (2) List of Floats containing the embeddings
    """
    try:
        req_data = await get_valid_json(request)
        if req_data is None:
            return Response("Please use JSON content type\n", 400)

        logger.info("Input request data {}".format(req_data))

        response_body = {
        "message": "JSON received!",
        "sender": "sentence_embedding_API",
        }

        sentence = req_data.get('sentence')

        if sentence is None:
            logger.info({"sentence": sentence, "response": ("Please provide an input sentence to embed\n", 400) })
            return Response("Please provide an input sentence to embed\n", 400)
        elif not isinstance(sentence, str):
            logger.info({"sentence": sentence, "response": ("Please use String data type for 'sentence' parameter\n", 400) })
            return Response("Please use String data type for 'sentence' parameter\n", 400)

        response_body.update({"embeddings": generate_random_array(RETURN_ARRAY_SIZE, ARRAY_LOWER_BOUND, ARRAY_UPPER_BOUND)})

    except Exception as err:
        logger.exception(err)
        return Response("Please retry again\n", 500)

    return response_body

def log_connection_url() -> None:
    """
    Log the url needed to connect to this pod. Since Uvicorn doesn't print
    its own IP, this is needed to know how to connect.
    """
    host_ip = socket.gethostbyname(socket.gethostname())
    logger.info(f"Connection URL: http://{host_ip}:{FASTAPI_PORT}")


if __name__ == "__main__":
    config = configparser.RawConfigParser()
    config.read('config/config.cfg')
    # CLASS_IMBALANCE = config.getboolean("main", "class_imbalance")
    main_config = dict(config.items("main"))
    LOGGER_FILE_PATH = main_config["logger_file_path"]

    #Reading logger configuration
    try: # Reading the file
        with open(LOGGER_FILE_PATH, 'r') as json_file:
            logger_config = json.load(json_file)

            # Override uvicorn logger to log correctly until it starts up
            logger_config["loggers"]["uvicorn"] = {}
            logger_config["loggers"]["uvicorn.error"] = {}

        #Setting up logger
        logging.config.dictConfig(logger_config)
        logger = logging.getLogger()
        logger.debug(logger)
        logger.info("Initiating the application")
    except Exception as e:
        raise

    FASTAPI_HOST = main_config["fastapi_host"]
    FASTAPI_PORT = int(main_config["fastapi_port"])
    RETURN_ARRAY_SIZE = int(main_config["return_array_size"])
    ARRAY_LOWER_BOUND = int(main_config["array_lower_bound"])
    ARRAY_UPPER_BOUND = int(main_config["array_upper_bound"])

    log_connection_url()
    uvicorn.run(app, host = FASTAPI_HOST, port = FASTAPI_PORT, log_config = logger_config)
