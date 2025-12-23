import pytest
import json
from app.models import Task

class TestTaskRoutes:
    """Test cases for task API routes."""
    
    def test_get_tasks_empty(self, client):
        """Test getting all tasks when none exist."""
        response = client.get('/api/tasks/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'tasks' in data
        assert 'count' in data
        assert len(data['tasks']) == 0
        assert data['count'] == 0
    
    def test_get_tasks_with_data(self, client, sample_task):
        """Test getting all tasks when tasks exist."""
        response = client.get('/api/tasks/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data['tasks']) == 1
        assert data['tasks'][0]['id'] == sample_task.id
        assert data['tasks'][0]['title'] == sample_task.title
    
    def test_create_task_success(self, client):
        """Test successful task creation."""
        task_data = {
            'title': 'New Test Task',
            'description': 'This is a new test task',
            'status': 'pending',
            'priority': 'high'
        }
        
        response = client.post('/api/tasks/',
                            data=json.dumps(task_data),
                            content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['title'] == task_data['title']
        assert data['description'] == task_data['description']
        assert data['status'] == task_data['status']
        assert data['priority'] == task_data['priority']
        assert 'id' in data
        assert 'created_at' in data
    
    def test_create_task_missing_title(self, client):
        """Test creating task without title."""
        task_data = {
            'description': 'Task without title'
        }
        
        response = client.post('/api/tasks/',
                            data=json.dumps(task_data),
                            content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Title is required' in data['error']
    
    def test_create_task_no_json(self, client):
        """Test creating task without JSON data."""
        response = client.post('/api/tasks/')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'No JSON data provided' in data['error']
    
    def test_get_task_by_id(self, client, sample_task):
        """Test getting a specific task by ID."""
        response = client.get(f'/api/tasks/{sample_task.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == sample_task.id
        assert data['title'] == sample_task.title
    
    def test_get_nonexistent_task(self, client):
        """Test getting a non-existent task."""
        response = client.get('/api/tasks/999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error']
    
    def test_update_task_success(self, client, sample_task):
        """Test successful task update."""
        update_data = {
            'title': 'Updated Task Title',
            'status': 'completed'
        }
        
        response = client.put(f'/api/tasks/{sample_task.id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == update_data['title']
        assert data['status'] == update_data['status']
        assert data['id'] == sample_task.id
    
    def test_update_nonexistent_task(self, client):
        """Test updating a non-existent task."""
        update_data = {'title': 'Updated Title'}
        
        response = client.put('/api/tasks/999',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error']
    
    def test_delete_task_success(self, client, sample_task):
        """Test successful task deletion."""
        response = client.delete(f'/api/tasks/{sample_task.id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        assert 'deleted successfully' in data['message']
    
    def test_delete_nonexistent_task(self, client):
        """Test deleting a non-existent task."""
        response = client.delete('/api/tasks/999')
        
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data
        assert 'not found' in data['error']
    
    def test_get_task_comments(self, client, sample_task, sample_comment):
        """Test getting comments for a specific task."""
        response = client.get(f'/api/tasks/{sample_task.id}/comments')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'task' in data
        assert 'comments' in data
        assert 'comments_count' in data
        assert data['task']['id'] == sample_task.id
        assert len(data['comments']) == 1
        assert data['comments_count'] == 1
