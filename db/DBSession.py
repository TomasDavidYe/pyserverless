import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker



# Newer implementation of DB access than DB Connector.
# Use if you want to run multiple queries in a single session
class DBSession:
    def __init__(self, conn_string: str, logger):
        self.engine = create_engine(conn_string)
        self.get_session = sessionmaker(bind=self.engine)
        self.session = None
        self.logger = logger

    def __enter__(self):
        self.start_session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.logger.error('Something happened during BD session')
            self.logger.error(f'Exception: {str(exc_val)}')
            self.logger.error(f'Stacktrace: \n{exc_tb}')
            if self.session_in_progress():
                self.rollback_session()
                self.session = None
            else:
                self.logger.info('No session in progress -> Nothing to rollback')
            raise exc_val
        else:
            if self.session_in_progress():
                self.logger.info('Session in progress')
                self.commit_session()

    def execute_raw_sql(self, sql, params=None):
        def execute(session):
            self.logger.info('Executing the following query:')
            self.logger.info(sql)
            return session.execute(text(sql), params)

        return self.run(execute)

    def run(self, operation):
        return operation(self.session)

    def session_in_progress(self):
        return self.session is not None

    def check_session_not_in_progress(self):
        if self.session_in_progress():
            raise Exception('Session currently in progress. Cannot start a new one.')

    def start_session(self):
        self.logger.info('Starting a new session')
        self.session = self.get_session()

    def close_session(self):
        self.logger.info('Closing current session')
        self.session.close()
        self.session = None

    def rollback_session(self):
        self.logger.info('Rolling back current session')
        self.session.rollback()
        self.logger.info('Rollback successful')
        self.close_session()

    def commit_session(self):
        self.logger.info('Committing current session')
        self.session.commit()
        self.logger.info('Commit successful')
        self.close_session()

    def read_df_from_sql(self, sql: str, parse_date=None) -> pd.DataFrame:
        self.logger.info(f'Loading the following SQL query into dataframe')
        self.logger.info(sql)
        self.logger.info('Loading...')
        result = pd.read_sql(sql=sql,
                             con=self.engine,
                             parse_dates=parse_date)
        self.logger.info('Data loaded successfully')
        self.logger.info('DF Tail:')
        self.logger.info(result.tail())
        self.logger.info('DF Head:')
        self.logger.info(result.tail())
        return result
