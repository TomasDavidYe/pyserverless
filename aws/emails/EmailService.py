import boto3
from botocore.exceptions import ClientError
from logs.Logger import Logger


class EmailService:


    def __init__(self, sender: str, logger: Logger):
        self.ses = boto3.client(
            'ses',
            aws_access_key_id='AWS_ACCESS_KEY',
            aws_secret_access_key='AWS_SECRET_KEY',
            region_name='eu-west-1'
        )
        self.sender = sender
        self.char_set = "UTF-8"
        self.logger = logger

    @staticmethod
    def fill_template(template: str, params):
        result = template
        for key, value in params.items():
            if not key.startswith('_'):
                result = result.replace(f'$({key})', str(value))

        return result

    def send_email_to_all_subscribers(self, email_subject: str, content_template: str, params: dict, recipients: list):
        for recipient in recipients:
            email_content = self.fill_template(template=content_template,
                                               params=params)

            self.send_email(recipient_email=recipient,
                            email_subject=email_subject,
                            email_content=email_content)

    def send_email(self, recipient_email: str, email_subject: str, email_content: str):
        try:
            self.logger.info(f'Sending email to {recipient_email}')
            self.logger.info(f'Subject: {email_subject}')
            self.logger.info('Content:')
            self.logger.info(email_content)

            response = self.ses.send_email(
                Destination={
                    'ToAddresses': [
                        recipient_email,
                    ],
                },
                Message={
                    'Body': {
                        'Html': {
                            'Charset': self.char_set,
                            'Data': email_content,
                        },
                        'Text': {
                            'Charset': self.char_set,
                            'Data': email_content,
                        },
                    },
                    'Subject': {
                        'Charset': self.char_set,
                        'Data': email_subject,
                    },
                },
                Source=self.sender,
            )
        # Display an error if something goes wrong.
        except ClientError as e:
            self.logger.info(f'Something happened while sending an email to {recipient_email}')
            self.logger.info(e.response['Error']['Message'])
            raise e
        else:
            self.logger.info("Email sent! Message ID:"),
            self.logger.info(response['MessageId'])
