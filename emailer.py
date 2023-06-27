import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Your email server configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = ---
SMTP_USERNAME = 'youremail@email.com'
SMTP_PASSWORD = 'yourpassword'

# Create SQLAlchemy engine and session
engine = create_engine('sqlite:///instance/todo.db')
Session = sessionmaker(bind=engine)
session = Session()

# Create base class for models
Base = declarative_base()

# Define the Todo model
class Todo(Base):
    __tablename__ = 'todo'
    id = Column(Integer, primary_key=True)
    content = Column(String(200), nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    completion_date = Column(Date, nullable=True)
    completion_time = Column(DateTime, nullable=True)

    def __repr__(self):
        return '<Task %r>' % self.id

def send_email(subject, sender, recipients, body):
    # Create a MIME message
    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender
    message['To'] = ', '.join(recipients)

    # Attach the HTML body
    html_body = MIMEText(body, 'html')
    message.attach(html_body)

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(message)
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))

def main():
    # Query todos for today or without completion date
    today = date.today()
    todos = session.query(Todo).filter((Todo.completion_date == None) | (Todo.completion_date == today)).all()

    # Generate HTML for todos
    todos_html = "<ul style='font-size: 24px'>"
    for todo in todos:
        todos_html += f"<li>{todo.content}</li>"
    todos_html += "</ul>"

    # Construct email body with todos
    body = f"<html><body><h1>Important todos for {today}:</h1><p>{todos_html}<p></body></html>"

    # Example usage of send_email function
    subject = f"Important todos for {today}"
    sender = 'youremail@example.com'
    recipients = ['sender-email']

    send_email(subject, sender, recipients, body)

if __name__ == '__main__':
    main()
