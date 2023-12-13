# exts.py：这个文件存在的意义就是为了解决循环引用的问题
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

db=SQLAlchemy()