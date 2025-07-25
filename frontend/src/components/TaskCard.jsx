// src/components/TaskCard.jsx
import React from 'react';
import './TaskCard.css'; // Crie este arquivo CSS para estilizar o card

const TaskCard = ({ task, onClick }) => {
  return (
    <div className={`task-card ${task.status}`} onClick={() => onClick(task)}>
      <h3>{task.title}</h3>
      <p>{task.description}</p>
      <div className="task-meta">
        <span>Status: {task.status.replace('_', ' ').toUpperCase()}</span>
        {task.updated_at ? (
          <span>Updated at: {new Date(task.updated_at).toLocaleDateString()}</span>
        ) : (
          <span>Created at: {new Date(task.created_at).toLocaleDateString()}</span>
        )}
      </div>
    </div>
  );
};

export default TaskCard;