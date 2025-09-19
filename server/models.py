from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, name):
        if not name or name.strip() == "":
            raise ValueError("Author must have a name")

        # Query the database to check if name already exists (excluding self if updating)
        existing_author = Author.query.filter(Author.name == name).first()

        # If this is a new record (no id yet) or editing to a duplicate name
        if existing_author and (not self.id or existing_author.id != self.id):
            raise ValueError("Author name must be unique")

        return name

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        # Check if phone number is exactly 10 digits (only digits allowed)
        if phone_number is None or not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return phone_number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('content')
    def validate_content(self, key, content):
        if content is None or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if summary is None:
            return summary
        if len(summary) > 250:
            raise ValueError("Post summary must be at most 250 characters")
        return summary

    @validates('category')
    def validate_category(self, key, category):
        if category not in ["Fiction", "Non-Fiction"]:
            raise ValueError("Category must be either 'Fiction' or 'Non-Fiction'")
        return category

    @validates('title')
    def validate_title(self, key, title):
        # Title must contain at least one of these phrases
        required_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in required_phrases):
            raise ValueError(f"Title must contain one of: {', '.join(required_phrases)}")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title}, content={self.content}, summary={self.summary})'
