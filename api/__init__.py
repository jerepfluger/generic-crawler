from flask import Blueprint

routes = Blueprint('routes', __name__)

from .linkedin_controller import *
from .twitter_controller import *
