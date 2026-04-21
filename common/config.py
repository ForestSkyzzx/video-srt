# -*- encoding: utf-8 -*-
import os


class Config:
    OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")
    os.makedirs(OUTPUT_PATH, exist_ok=True)
