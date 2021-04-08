import traceback

from aws.emails.EmailService import EmailService
from aws.lambdas.lambda_error_template import LAMBDA_ERROR_TEMPLATE
from db.DBSession import DBSession
from logs.Logger import Logger
from utils.string_utils import to_json, to_html


class LambdaWrapper:
    def __init__(self, logger: Logger, email_sender_address, recipient_list, max_log_size: int = 10000):
        self.email_sender_address = email_sender_address
        self.recipient_list = recipient_list
        self.logger: Logger = logger
        self.max_log_size: int = max_log_size
        self.email_service = EmailService(sender=self.email_sender_address, logger=self.logger)

    def run(self, handler, event, context, function_name, send_email_on_error=True):
        try:
            with DBSession(logger=self.logger, conn_string='postgresql+pg8000://user:pass@host/dbname') as db_session:
                self.logger.info(f'Event:\n {to_json(event)[:self.max_log_size]}')
                self.logger.info(f'Context:\n {to_json(event)[:self.max_log_size]}')
                return handler(event=event, context=context, logger=self.logger, db_session=db_session)

        except Exception as e:
            if send_email_on_error:
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
                email_subject='[YOUR APP NAME] -> Lambda Function Error',
                content_template=LAMBDA_ERROR_TEMPLATE,
                recipients=self.recipient_list,
                params={
                    'response': to_html(response),
                    'function_name': function_name,
                    'exception': to_html(error_message),
                    'stack_trace': to_html(stack_trace),
                    'log': to_html(self.logger.log_file)

                }
            )

            return response
