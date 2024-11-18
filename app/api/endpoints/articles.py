from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ...database import get_db
from ...schemas import schemas
from ...models import models

router = APIRouter()

# CREATE ARTICLE
@router.post("/articles/", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    """
    Creates a new article in the database
    
    Why this endpoint?
    - Used by web scraper to save new articles
    - Handles both article creation and tag association
    - Validates input data through Pydantic schema
    """
    # Check if article already exists
    existing_article = db.query(models.Article).filter(
        models.Article.url == str(article.url)
    ).first()
    if existing_article:
        raise HTTPException(status_code=400, detail="Article already exists")
    
    # Create new article
    db_article = models.Article(
        url=str(article.url),
        title=article.title,
        content=article.content,
        summary=article.summary,
        source=article.source,
    )
    
    # Handle tags
    for tag_name in article.tags:
        # Get existing tag or create new one
        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
        db_article.tags.append(tag)
    
    try:
        db.add(db_article)
        db.commit()
        db.refresh(db_article)
        return db_article
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# GET ALL ARTICLES
@router.get("/articles/", response_model=List[schemas.Article])
def read_articles(
    skip: int = 0, 
    limit: int = 20, 
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    """
    Retrieves articles with pagination and sorting
    
    Why these parameters?
    - skip/limit: Enables pagination for better performance
    - sort_by: Allows different sorting criteria
    - order: Ascending or descending order
    """
    query = db.query(models.Article)
    
    # Handle sorting
    if hasattr(models.Article, sort_by):
        order_by = getattr(models.Article, sort_by)
        if order == "desc":
            order_by = order_by.desc()
        query = query.order_by(order_by)
    
    articles = query.offset(skip).limit(limit).all()
    return articles

# GET SINGLE ARTICLE
@router.get("/articles/{article_id}", response_model=schemas.Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a single article by ID
    
    Why? 
    - Detailed view of specific article
    - Access to all article relationships (tags, citations)
    """
    article = db.query(models.Article).filter(
        models.Article.id == article_id
    ).first()
    if article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

# UPDATE ARTICLE
@router.put("/articles/{article_id}", response_model=schemas.Article)
def update_article(
    article_id: int, 
    article_update: schemas.ArticleCreate, 
    db: Session = Depends(get_db)
):
    """
    Updates an existing article
    
    Why?
    - Update summaries after AI processing
    - Update content after re-scraping
    - Modify tags
    """
    db_article = db.query(models.Article).filter(
        models.Article.id == article_id
    ).first()
    if db_article is None:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Update basic fields
    for field, value in article_update.dict(exclude={'tags'}).items():
        setattr(db_article, field, value)
    
    # Update tags
    if article_update.tags is not None:
        # Clear existing tags
        db_article.tags = []
        # Add new tags
        for tag_name in article_update.tags:
            tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
            if not tag:
                tag = models.Tag(name=tag_name)
            db_article.tags.append(tag)
    
    try:
        db.commit()
        db.refresh(db_article)
        return db_article
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))