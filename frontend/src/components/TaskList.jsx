import React from 'react';
import TaskCard from './TaskCard';
import './TaskList.css'; // Crie este arquivo CSS


function TaskList ({ tasks, onAddTask, onEditTask, filterStatus }) {

  return (
    <div className="task-list-container">
      <div className="task-list-header">
        <h1>My Tasks</h1>
        <div>Filter by status:
          <select onChange={(e) => filterStatus(e.target.value)}>
          <option value="">All</option>
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="completed">Completed</option>
          </select>
        </div>
        <button onClick={onAddTask} className="button primary">
          + Add New Task
        </button>
      </div>
      <div className="tasks-grid">
        {tasks.length === 0 ? (
          <p>No tasks found. Start by adding one!</p>
        ) : (
          tasks.map((task) => (
            <TaskCard key={task.id} task={task} onClick={onEditTask} />
          ))
        )}
      </div>
    </div>
  );
};

export default TaskList;
