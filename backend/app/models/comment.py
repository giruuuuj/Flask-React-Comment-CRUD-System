from datetime import datetime
from app import db

class Comment(db.Model):
    """Comment model representing a comment on a task."""
    
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author_name = db.Column(db.String(100), nullable=False)
    author_email = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign key to task
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    
    def __repr__(self):
        return f'<Comment {self.id}: {self.content[:50]}...>'
    
    def to_dict(self):
        """Convert comment to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'content': self.content,
            'author_name': self.author_name,
            'author_email': self.author_email,
            'task_id': self.task_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @staticmethod
    def from_dict(data):
        """Create comment from dictionary."""
        return Comment(
            content=data.get('content'),
            author_name=data.get('author_name'),
            author_email=data.get('author_email'),
            task_id=data.get('task_id')
        )
    
    def update_from_dict(self, data):
        """Update comment from dictionary."""
        if 'content' in data:
            self.content = data['content']
        if 'author_name' in data:
            self.author_name = data['author_name']
        if 'author_email' in data:
            self.author_email = data['author_email']
        self.updated_at = datetime.utcnow()
