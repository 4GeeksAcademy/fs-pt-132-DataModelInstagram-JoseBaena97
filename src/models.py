import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__= "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(25), nullable=False)
    lastname: Mapped[str] = mapped_column(String(40), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)

    #Relationships
    posts: Mapped[List["Post"]] = relationship(back_populates="user")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,

            # do not serialize the password, its a security breach
        }

class Post(db.Model):
    __tablename__= "post"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)

    #Relationships
    user: Mapped["User"] = relationship(back_populates="posts")
    media: Mapped[List["Media"]] = relationship(back_populates="post")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }

class MediaType(enum.Enum):
    IMAGE = "image"
    VIDEO = "video"

class Media(db.Model):
    __tablename__="media"
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[MediaType] = mapped_column(Enum(MediaType), nullable=False)
    url: Mapped[str] = mapped_column(String(250), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    #Relationships
    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type.value,
            "url": self.url,
            "post_id": self.post_id,
        }
    
class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(Text, nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey('post.id'), nullable=False)

    #Realtionships
    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "comment_text": self.comment_text,
            "author_id": self.author_id,
            "post_id": self.post_id,
        }
    
class Follower(db.Model):
    __tablename__ = "follower"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user_to_id: Mapped[int] = mapped_column(ForeignKey('user.id'))

    def serialize(self):
        return {
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }
    