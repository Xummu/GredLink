import os



#local host mysql 연결

DB_USER = 'root'
DB_PASSWORD = '12345678'
DB_NAME = 'GredLink'
DB_HOST = 'localhost'

SQLALCHEMY_DATABASE_URI = (f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?charset=utf8mb4' )

# Flask config
SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key' # 로그인 상태 보안용
SQLALCHEMY_TRACK_MODIFICATIONS = False