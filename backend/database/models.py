from sqlalchemy import Column, Integer, String, ARRAY, DateTime, Boolean, LargeBinary, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    display_name = Column(String(30))
    note = Column(String(255))
    password = Column(LargeBinary)
    badges = Column(ARRAY(String))
    account_creation_date = Column(DateTime, nullable=False)
    friends = Column(ARRAY(Integer))
    avatar_id = Column(ForeignKey("Files.id"))

class User_Server(Base):
    __tablename__ = "User_Server"
    id = Column(Integer, primary_key=True) # Żeby sqlalchemy sie odwaliło
    user_id = Column(Integer, ForeignKey("Users.id"))
    server_id = Column(Integer, ForeignKey("Servers.id"))
    roles = Column(ARRAY(Integer))  # If your reading this, please forgive me for this abomination
    muted = Column(DateTime, nullable=True, default=None)

class Server(Base):
    __tablename__ = "Servers"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    invite_link = Column(String, nullable=False, unique=True) # For localhost:2137/invite/__code__, store here only __code__
    role_order = Column(ARRAY(Integer))   

class Channel(Base):
    __tablename__ = "Channels"
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey("Servers.id"), nullable=False)
    name = Column(String, nullable=False)
    role_needed = Column(String, nullable=True)
    color = Column(String, default="#FF00E6")

class Message(Base):
    __tablename__ = "Messages"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    channel_id = Column(Integer, ForeignKey("Channels.id"))
    date = Column(DateTime, nullable=False)
    text = Column(String)
    attachment_id = Column(Integer, ForeignKey("Files.id"), nullable=True)

class File(Base):
    __tablename__ = "Files"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    content = Column(LargeBinary, nullable=False)

class DM(Base):
    __tablename__ = "DMs"
    id = Column(Integer, primary_key=True)
    text = Column(String)
    date = Column(DateTime)
    attachment_id = Column(Integer, ForeignKey("Files.id"), nullable=True)
    user_id_1 = Column(Integer, ForeignKey("Users.id"), nullable=False) # Author
    user_id_2 = Column(Integer, ForeignKey("Users.id"), nullable=False)

class Friend_request(Base):
    __tablename__ = "Friends"
    id = Column(Integer, primary_key=True)
    user_id_1 = Column(Integer, ForeignKey("Users.id"))
    user_id_2 = Column(Integer, ForeignKey("Users.id"))

class Role(Base):
    __tablename__ = "Roles"
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey("Servers.id"), nullable=False)
    role_name = Column(String, nullable=False)
    permissions = Column(String, default="")
    color = Column(String, default="#FF00E6")

class Ban(Base):
    __tablename__ = "Bans"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("Users.id"), nullable=False)
    server_id = Column(Integer, ForeignKey("Servers.id"), nullable=False)
    ban_date = Column(DateTime, nullable=False)
    reason = Column(String, nullable=True)

import os, dotenv
from sqlalchemy import create_engine
dotenv.load_dotenv()
engine = create_engine(f'postgresql+psycopg2://{os.getenv("DB_USER")}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv("DB_NAME")}')

Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False,)

def init_db(engine_url: str):
    global engine, SessionLocal
    engine = create_engine(engine_url)
    SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
