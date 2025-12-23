from typing import List, Optional
from app import db
from app.models.task import Task

class TaskService:
    """Service layer for task business logic."""
    
    @staticmethod
    def get_all_tasks() -> List[Task]:
        """Get all tasks."""
        return Task.query.order_by(Task.created_at.desc()).all()
    
    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        """Get a specific task by ID."""
        return Task.query.get(task_id)
    
    @staticmethod
    def create_task(data: dict) -> Task:
        """Create a new task."""
        if not data.get('title'):
            raise ValueError("Title is required")
        
        task = Task.from_dict(data)
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def update_task(task_id: int, data: dict) -> Optional[Task]:
        """Update an existing task."""
        task = Task.query.get(task_id)
        if not task:
            return None
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        
        db.session.commit()
        return task
    
    @staticmethod
    def delete_task(task_id: int) -> bool:
        """Delete a task and all its comments."""
        task = Task.query.get(task_id)
        if not task:
            return False
        
        db.session.delete(task)
        db.session.commit()
        return True
