import traceback

from trading_engine_source.db.DBSession import DBSession
from trading_engine_source.email.EmailService import EmailService
from trading_engine_source.email.email_templates.lambda_error import LAMBDA_ERROR_TEMPLATE
from trading_engine_source.infrastructure.loggers.Logger import Logger
from trading_engine_source.utils.string_utils import to_json, to_html


class LambdaWrapper:
    def __init__(self, logger: Logger, max_log_size: int = 10000):
        self.logger: Logger = logger
        self.max_log_size: int = max_log_size
        self.email_service = EmailService.default(logger=logger)

    def run(self, handler, event, context, function_name='', is_test=False):
        try:
            with DBSession(logger=self.logger) as db_session:
                self.logger.info(f'Event:\n {to_json(event)[:self.max_log_size]}')
                self.logger.info(f'Context:\n {to_json(event)[:self.max_log_size]}')
                return handler(event=event, context=context, logger=self.logger, db_session=db_session)

        except Exception as e:
            if is_test:
                raise e

            error_message = str(e)
            stack_trace = traceback.format_exc()

            self.logger.error('Something happened during execution')
            self.logger.error(f'Exception: {error_message}')
            self.logger.error(f'Stacktrace: \n{stack_trace}')

            response = to_json({
                'status_code': 500,
                'message': 'Internal Server Error',
                'exception': error_message,
                'stack_trace': stack_trace,
                'context': context,

            })

            self.email_service.send_email_to_all_subscribers(
                email_subject='[TRADING ENGINE] -> Lambda Function Error',
                content_template=LAMBDA_ERROR_TEMPLATE,
                params={
                    'response': to_html(response),
                    'function_name': function_name,
                    'exception': to_html(error_message),
                    'stack_trace': to_html(stack_trace),
                    'log': to_html(self.logger.log_file)

                }
            )

            return response
