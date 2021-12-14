from flask import Blueprint

routes = Blueprint('routes', __name__)

from .twitter_controller import *
from .instagram_controller import *
