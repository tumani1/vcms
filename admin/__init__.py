# coding: utf-8
from utils.connection import get_session

session = get_session(autocommit=False, autoflush=True)
