// src/App.jsx
import React, { useState, useEffect, useCallback } from 'react';
import TaskList from '../components/TaskList';
import TaskModal from '../components/TaskModal';
import { getTasks, createTask, updateTask, deleteTask } from '../api/tasks';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';


function DashboardPage() {
  const [tasks, setTasks] = useState([]);
  const [statusFilter, setStatusFilter] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [currentTask, setCurrentTask] = useState(null);
  const updateStatusFilter = (newStatus) => {
    setStatusFilter(newStatus);
  };

  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const fetchTasks = useCallback(async () => {
    try {
      const params = statusFilter ? { status: statusFilter } : {};
      const data = await getTasks(params);
      setTasks(data);
    } catch (error) {
      if (error.response && error.response.status === 401) {
        handleLogout();
      }
      console.error('Failed to fetch tasks:', error);
    }
  }, [statusFilter]);;

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleAddTask = () => {
    setCurrentTask(null);
    setIsModalOpen(true);
  };

  const handleEditTask = (task) => {
    setCurrentTask(task);
    setIsModalOpen(true);
  };

  const handleSubmitTask = async (taskData) => {
    try {
      if (currentTask) {
        await updateTask(currentTask.id, taskData);
      } else {
        await createTask(taskData);
      }
      fetchTasks();
    } catch (error) {
      console.error('Error submitting task:', error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await deleteTask(taskId);
      fetchTasks();
    } catch (error) {
      console.error(`Error deleting task ${taskId}:`, error);
    }
  };

  return (
    <div className="DashboardPage">
      <TaskList
        tasks={tasks}
        onAddTask={handleAddTask}
        onEditTask={handleEditTask}
        filterStatus={updateStatusFilter}
      />

      <TaskModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        task={currentTask}
        onSubmit={handleSubmitTask}
        onDelete={handleDeleteTask}
      />
    </div>
  );
}

export default DashboardPage;