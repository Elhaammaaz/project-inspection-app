import os

class Config:
    """Base Flask configuration settings"""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production-12345'
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL:
        # Convert postgres:// to postgresql:// for SQLAlchemy 1.4+
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        # Add SSL requirement for Railway PostgreSQL (uses self-signed certs)
        if 'postgresql://' in DATABASE_URL and '?sslmode=' not in DATABASE_URL:
            DATABASE_URL = DATABASE_URL + '?sslmode=require'
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        # Local development fallback
        SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Connection pool settings for production
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Verify connections before using
        'pool_recycle': 3600,   # Recycle connections after 1 hour
        'pool_size': 10,        # Connection pool size
        'max_overflow': 20,     # Max overflow connections
    }
    
    # Flask-WTF
    WTF_CSRF_ENABLED = True
    
    # Session
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours in seconds


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# Get config based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# Default to development
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')
config_instance = config.get(FLASK_ENV, DevelopmentConfig)
