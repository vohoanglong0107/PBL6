import contextlib

from app.utils import read_config
from loguru import logger
from sqlalchemy import Column, Integer, create_engine, select
from sqlalchemy.dialects.mysql import TEXT, insert
from sqlalchemy.engine import URL, make_url
from sqlalchemy.orm import declarative_base, sessionmaker


config = read_config()
engine = create_engine(
    config["QUERY"]["INDEX_DB_URI"],
    future=True,
    pool_recycle=3600,
    pool_size=10,
    pool_pre_ping=True,
)


def create_database_if_not_exist():
    url = make_url(config["QUERY"]["INDEX_DB_URI"])
    url_wo_host = URL.create(
        drivername=url.drivername,
        username=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        database=None,
        query=url.query,
    )

    engine = create_engine(url_wo_host)
    conn = engine.connect()
    try:
        logger.info(f"Ensuring database {url.database} exists")
        conn.execute("CREATE DATABASE IF NOT EXISTS %s" % url.database)
    except Exception as ex:
        logger.error(ex)
    finally:
        conn.close()


create_database_if_not_exist()

Base = declarative_base()
Session = sessionmaker(bind=engine)


class Song(Base):
    __tablename__ = "song"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(TEXT)


Base.metadata.create_all(engine)


@contextlib.contextmanager
def get_session():
    session = Session(bind=engine)
    Base.metadata.create_all(engine)

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()


def index_song(start_index, song_names):
    # with get_session() as session:
    #     for index, song_name in enumerate(song_names, start=start_index):
    #         session.add(Song(id=index, name=song_name))
    #     session.commit()
    #     session.commit()
    with engine.connect() as conn:
        for i, song_name in enumerate(song_names, start=start_index):
            insert_stmt = insert(Song).values(id=i, name=song_name)
            on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(name=song_name)
            conn.execute(on_duplicate_key_stmt)
        conn.commit()


def get_candidate_names(candidate_indices):
    with engine.connect() as conn:
        stmt = select(Song.name).where(Song.id.in_(candidate_indices)).distinct()
        candidates = conn.execute(stmt)
        candidate_names = []
        for candidate in candidates:
            candidate_names.append(candidate.name)
        return candidate_names
