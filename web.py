# -*- coding: utf-8 -*-
from loguru import logger
import subprocess


class WebApp:
    def __init__(self, port: int):
        self.port = port

    def run(self):
        try:
            command = f"streamlit run st_app.py --server.port {self.port}"
            logger.info(f"Starting Web application on port {self.port}")
            process = subprocess.Popen(command, shell=True)
            process.wait()
        except KeyboardInterrupt:
            logger.info("Web application stopped by user")
            process.terminate()
