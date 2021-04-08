from flask import Blueprint

public = Blueprint('public', __name__, url_prefix='/',template_folder='templates')

from app.public import views