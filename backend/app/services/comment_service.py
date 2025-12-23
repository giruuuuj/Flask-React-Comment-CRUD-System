from typing import List, Optional
from app import db
from app.models.comment import Comment
from app.models.task import Task

class CommentService:
    """Service layer for comment business logic."""
    
    @staticmethod
    def get_comments_by_task(task_id: int) -> List[Comment]:
        """Get all comments for a specific task."""
        return Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.desc()).all()
    
    @staticmethod
    def get_comment_by_id(comment_id: int) -> Optional[Comment]:
        """Get a specific comment by ID."""
        return Comment.query.get(comment_id)
    
    @staticmethod
    def create_comment(data: dict) -> Comment:
        """Create a new comment."""
        # Validate task exists
        task = Task.query.get(data.get('task_id'))
        if not task:
            raise ValueError(f"Task with ID {data.get('task_id')} not found")
        
        # Validate required fields
        if not data.get('content') or not data.get('author_name'):
            raise ValueError("Content and author_name are required")
        
        comment = Comment.from_dict(data)
        db.session.add(comment)
        db.session.commit()
        return comment
    
    @staticmethod
    def update_comment(comment_id: int, data: dict) -> Optional[Comment]:
        """Update an existing comment."""
        comment = Comment.query.get(comment_id)
        if not comment:
            return None
        
        # Validate content if provided
        if 'content' in data and not data['content']:
            raise ValueError("Content cannot be empty")
        
        comment.update_from_dict(data)
        db.session.commit()
        return comment
    
    @staticmethod
    def delete_comment(comment_id: int) -> bool:
        """Delete a comment."""
        comment = Comment.query.get(comment_id)
        if not comment:
            return False
        
        db.session.delete(comment)
        db.session.commit()
        return True
    
    @staticmethod
    def validate_comment_data(data: dict, is_update: bool = False) -> dict:
        """Validate comment data and return cleaned data."""
        errors = []
        
        if not is_update:
            # Required fields for creation
            if not data.get('content'):
                errors.append("Content is required")
            if not data.get('author_name'):
                errors.append("Author name is required")
            if not data.get('task_id'):
                errors.append("Task ID is required")
        else:
            # For updates, at least one field should be provided
            if not any(key in data for key in ['content', 'author_name', 'author_email']):
                errors.append("At least one field must be provided for update")
        
        # Validate email format if provided
        if data.get('author_email'):
            import re
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, data['author_email']):
                errors.append("Invalid email format")
        
        if errors:
            raise ValueError("; ".join(errors))
        
        return data
