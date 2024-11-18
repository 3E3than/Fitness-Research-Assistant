from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_
from sqlalchemy.sql import func
from typing import List
from ...database import get_db
from ...schemas import schemas
from ...models import models

router = APIRouter()

@router.post("/search/", response_model=List[schemas.Article])
def search_articles(query: schemas.SearchQuery, db: Session = Depends(get_db)):
    """
    Searches articles based on various criteria
    
    Why this endpoint?
    - Main search functionality for the frontend
    - Supports multiple search criteria
    - Includes pagination for performance
    """
    # Build base query
    base_query = db.query(models.Article)
    
    # Add search conditions
    if query.query:
        search_terms = query.query.split()
        search_conditions = []
        for term in search_terms:
            # Search in title and content
            search_conditions.append(models.Article.title.ilike(f"%{term}%"))
            search_conditions.append(models.Article.content.ilike(f"%{term}%"))
        
        # Combine conditions with OR
        base_query = base_query.filter(or_(*search_conditions))
    
    # Apply source filter
    if query.sources:
        base_query = base_query.filter(models.Article.source.in_(query.sources))
    
    # Apply tag filter
    if query.tags:
        base_query = base_query.join(models.Article.tags).filter(
            models.Tag.name.in_(query.tags)
        ).group_by(models.Article.id)
    

    # Add pagination
    offset = (query.page - 1) * query.per_page
    articles = base_query.offset(offset).limit(query.per_page).all()
    
    return articles

# GET TAGS
@router.get("/tags/", response_model=List[schemas.Tag])
def get_tags(db: Session = Depends(get_db)):
    """
    Retrieves all available tags
    
    Why?
    - Populate frontend filters
    - Show available categories
    """
    return db.query(models.Tag).all()