from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class TagBase(BaseModel):
    """Base Tag schema with common attributes"""
    name: str

class TagCreate(TagBase):
    """Schema for creating new tags
    Inherits from TagBase but could add additional fields needed for creation"""
    pass

class Tag(TagBase):
    """Schema for returning tags
    Adds database-specific fields"""
    id: int

    class Config:
        from_attributes = True  # Allows converting SQLAlchemy models to JSON

class CitationBase(BaseModel):
    """Base Citation schema with common attributes"""
    text: str  # Citation text, which could be a quote or reference

class CitationCreate(CitationBase):
    """Schema for creating new citations
    Can include additional fields for creation, if needed"""
    pass

class Citation(CitationBase):
    """Schema for returning citations
    Adds database-specific fields like the citation's ID and the associated article"""
    id: int  # Citation ID, assigned by the database
    article_id: int  # The ID of the article this citation belongs to

    class Config:
        from_attributes = True  # Allows converting SQLAlchemy models to JSON

class ArticleBase(BaseModel):
    """Base Article schema with common attributes
    
    Why these fields?
    - content/summary: Optional because they might be added later
    """
    url: str  # Validates URL format
    title: str
    content: Optional[str] = None
    summary: Optional[str] = None
    source: str

class ArticleCreate(ArticleBase):
    """Schema for creating new articles
    Adds tags field for creation"""
    tags: Optional[List[str]] = []  # Accept list of tag names

class Article(ArticleBase):
    """Schema for returning articles
    Adds all database-specific fields and relationships"""
    id: int
    tags: List[Tag]
    citations: List[Citation]

    class Config:
        from_attributes = True

class SearchQuery(BaseModel):
    """Schema for search requests
    
    Why these fields?
    - query: Main search term
    - sources/tags: Optional filters
    - page/per_page: Pagination control
    """
    query: str
    sources: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    page: int = 1
    per_page: int = 10