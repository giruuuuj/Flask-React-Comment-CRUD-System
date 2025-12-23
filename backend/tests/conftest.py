import pytest
from app import create_app, db
from app.models import Task, Comment

@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def sample_task(app):
    """Create a sample task for testing."""
    with app.app_context():
        task = Task(
            title="Test Task",
            description="This is a test task",
            status="pending",
            priority="medium"
        )
        db.session.add(task)
        db.session.commit()
        return task

@pytest.fixture
def sample_comment(app, sample_task):
    """Create a sample comment for testing."""
    with app.app_context():
        comment = Comment(
            content="This is a test comment",
            author_name="Test User",
            author_email="test@example.com",
            task_id=sample_task.id
        )
        db.session.add(comment)
        db.session.commit()
        return comment

@pytest.fixture
def auth_headers():
    """Mock authentication headers (for future auth implementation)."""
    return {}
