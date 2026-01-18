"""
Database connection module - PostgreSQL with SQLite fallback
Replaces: backend/database/db.py
"""
import os
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Handle Render's postgres:// URL format (needs to be postgresql://)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Fallback to SQLite for local development if no DATABASE_URL is set
if not DATABASE_URL:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DB_PATH = os.path.join(BASE_DIR, "preferences.db")
    DATABASE_URL = f"sqlite:///{DB_PATH}"
    print(f"⚠️  Using SQLite: {DB_PATH}")
else:
    print(f"✅ Using PostgreSQL")

# Create engine with appropriate settings
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        echo=False
    )

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Define the Preferences model (matching your existing schema)
class Preferences(Base):
    __tablename__ = "preferences"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_role = Column(Text, nullable=False)
    location = Column(Text, nullable=False)
    experience = Column(Integer, nullable=True)
    work_mode = Column(Text, nullable=True)
    email = Column(Text, nullable=False)

def get_db_connection():
    """
    Get a database session (replaces old sqlite3.connect)
    Returns a SQLAlchemy session that works like your old conn
    """
    return SessionLocal()

def init_db():
    """
    Create preferences table if not exists.
    This replaces your old init_db function.
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization failed: {str(e)}")
        return False

# Helper functions to maintain compatibility with your existing code
class DBConnectionWrapper:
    """
    Wrapper to make SQLAlchemy session work like sqlite3 connection
    This allows your existing code to work with minimal changes
    """
    def __init__(self, session):
        self.session = session
        self._cursor = None
    
    def cursor(self):
        if not self._cursor:
            self._cursor = CursorWrapper(self.session)
        return self._cursor
    
    def commit(self):
        self.session.commit()
    
    def close(self):
        self.session.close()
    
    def rollback(self):
        self.session.rollback()

class CursorWrapper:
    """
    Wrapper to make SQLAlchemy queries work like sqlite3 cursor
    """
    def __init__(self, session):
        self.session = session
        self._results = []
    
    def execute(self, query, params=None):
        """Execute SQL query"""
        from sqlalchemy import text
        
        if params:
            # Convert ? placeholders to :param format for SQLAlchemy
            param_dict = {}
            param_names = []
            
            for i, value in enumerate(params):
                param_name = f"param{i}"
                param_dict[param_name] = value
                param_names.append(f":{param_name}")
            
            # Replace ? with :param0, :param1, etc.
            converted_query = query
            for param_name in param_names:
                converted_query = converted_query.replace("?", param_name, 1)
            
            result = self.session.execute(text(converted_query), param_dict)
        else:
            result = self.session.execute(text(query))
        
        # Store results
        try:
            self._results = [RowWrapper(row) for row in result.fetchall()]
        except:
            self._results = []
        
        return self
    
    def fetchall(self):
        """Fetch all results"""
        return self._results
    
    def fetchone(self):
        """Fetch one result"""
        return self._results[0] if self._results else None

class RowWrapper:
    """
    Wrapper to make SQLAlchemy Row work like sqlite3.Row
    Allows both dict-like and attribute access
    """
    def __init__(self, row):
        self._row = row
        # Get column names
        self._keys = list(row._mapping.keys()) if hasattr(row, '_mapping') else []
    
    def __getitem__(self, key):
        """Allow row["column_name"] access"""
        if hasattr(self._row, '_mapping'):
            return self._row._mapping[key]
        return getattr(self._row, key)
    
    def __iter__(self):
        """Allow iteration over row"""
        return iter(self._keys)
    
    def keys(self):
        """Return column names"""
        return self._keys

# Override get_db_connection to return wrapped session
_original_get_db_connection = get_db_connection

def get_db_connection():
    """
    Get database connection that works like sqlite3.connect()
    This maintains compatibility with your existing code
    """
    session = _original_get_db_connection()
    return DBConnectionWrapper(session)




# import sqlite3
# import os

# # Database file path
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "preferences.db")


# def get_db_connection():
#     conn = sqlite3.connect(DB_PATH)
#     conn.row_factory = sqlite3.Row
#     return conn


# def init_db():
#     """Create preferences table if not exists."""
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS preferences (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             job_role TEXT NOT NULL,
#             location TEXT NOT NULL,
#             experience INTEGER,
#             work_mode TEXT,
#             email TEXT NOT NULL
#         )
#     """)

#     conn.commit()
#     conn.close()
