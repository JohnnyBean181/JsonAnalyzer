import pandas as pd
from sqlalchemy import create_engine
from contextlib import contextmanager

from sqlalchemy.orm import sessionmaker

from comm_tools.logger import log_progress
from comm_tools.config import Config
from sqlalchemy.ext.declarative import declarative_base




def load_to_MySQL_on_Cloud(df, sql_connection, table_name):
    """
    This function saves the final data frame to a database
    table with the provided name. Function returns nothing.

    :param df: data to be saved
    :param sql_connection: MySQL conn
    :param table_name: table name
    :return: none
    """
    try:
        df.to_sql(name=table_name, con=sql_connection, index=False, if_exists='append')  # 'append' 追加数据
        log_progress("Data loaded to Database as a table, Executing queries")
    except Exception as e:
        if "Duplicate" in str(e):
            log_progress("Data not loaded due to duplicate entry")


def run_query(query_statement, sql_connection):
    """
    This function runs the query on the database table and
    prints the output on the terminal. Function returns nothing.

    :param query_statement:
    :param sql_connection:
    :return: retrieved data as dataframe
    """
    log_progress(f"Query statement is : {query_statement}")
    query_output = pd.read_sql(query_statement, sql_connection)
    log_progress(f"Query output is : {query_output}")
    return query_output


@contextmanager
def open_mysql(c:Config):
    """
    Deprecated function. Save data using df.
    :param c:
    :return:
    """
    global engine
    try:
        # 创建 SQLAlchemy 引擎
        connection_string = (f"mysql+mysqlconnector://{c.user}:{c.password}"
                             f"@{c.host}:{c.port}/{c.database}")
        engine = create_engine(connection_string)
        yield engine
    finally:
        if engine is not None:
            # 释放引擎
            engine.dispose()

@contextmanager
def open_mysql_plus(c:Config):
    """
    Save data into tables using model. This makes handling relationships between
    tables become easy.
    :param c: c is used to save configure information.
    :return: return session which is used to communicate with database.
    """
    global session
    Base = declarative_base()
    try:
        engine = create_engine(f"mysql+mysqlconnector://{c.user}:{c.password}"
                             f"@{c.host}:{c.port}/{c.database}")
        Base.metadata.create_all(engine)  # 创建所有表结构
        Session = sessionmaker(bind=engine)
        session = Session()
        yield session
    finally:
        if session is not None:
            # 释放引擎
            session.close()