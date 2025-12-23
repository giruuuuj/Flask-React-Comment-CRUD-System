from datetime import datetime
from app import db

class Task(db.Model):
    """Task model representing a task that can have comments."""
    
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with comments
    comments = db.relationship('Comment', backref='task', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Task {self.id}: {self.title}>'
    
    def to_dict(self):
        """Convert task to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'comments_count': len(self.comments) if self.comments else 0
        }
    
    @staticmethod
    def from_dict(data):
        """Create task from dictionary."""
        return Task(
            title=data.get('title'),
            description=data.get('description'),
            status=data.get('status', 'pending'),
            priority=data.get('priority', 'medium')
        )
