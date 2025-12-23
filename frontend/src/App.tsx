import React from 'react';
import { Toaster } from 'react-hot-toast';
import './App.css';
import TaskList from './components/TaskList';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Task & Comment Management System</h1>
        <p>A Flask + React application for managing tasks and comments</p>
      </header>
      <main className="App-main">
        <TaskList />
      </main>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'rgba(255, 255, 255, 0.95)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: '12px',
            padding: '16px',
            color: '#333',
            boxShadow: '0 8px 32px rgba(0, 0, 0, 0.1)',
          },
          success: {
            iconTheme: {
              primary: '#667eea',
              secondary: '#fff',
            },
          },
          error: {
            iconTheme: {
              primary: '#f5576c',
              secondary: '#fff',
            },
          },
        }}
      />
    </div>
  );
}

export default App;
