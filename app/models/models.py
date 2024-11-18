from sqlalchemy import Column, Integer, String, ForeignKey, Table, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

article_tags = Table(
    'article_tags',
    Base.metadata,
    Column('article_id', Integer, ForeignKey('articles.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Article(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, index=True)  # Indexed for faster lookups
    title = Column(String)
    content = Column(String)
    summary = Column(String)
    source = Column(String)
    #relationships
    tags = relationship("Tag", secondary=article_tags, back_populates="articles")
    citations = relationship("Citation", back_populates="article")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)
    articles = relationship("Article", secondary=article_tags, back_populates="tags")

class Citation(Base):
    """
    Citation model - tracks references in articles
    
    Why track citations?
    - Verify article credibility
    - Link to related research
    - Enable academic references
    """
    __tablename__ = "citations"

    id = Column(Integer, primary_key=True)
    text = Column(String)
    article_id = Column(Integer, ForeignKey("articles.id"))
    article = relationship("Article", back_populates="citations")