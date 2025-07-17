// src/components/TaskModal.jsx
import React, { useState, useEffect } from 'react';
import './TaskModal.css'; // Crie este arquivo CSS para estilizar o modal

// Enum de status (poderia vir de um arquivo de constantes)
const TaskStatusEnum = {
  PENDING: "pending",
  IN_PROGRESS: "in_progress",
  COMPLETED: "completed",
};

const TaskModal = ({ isOpen, onClose, task, onSubmit, onDelete }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState(TaskStatusEnum.PENDING);

  // Efeito para preencher o formulário quando uma tarefa é passada (modo edição)
  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || ''); // Descrição pode ser nula
      setStatus(task.status);
    } else {
      // Limpa o formulário para adicionar nova tarefa
      setTitle('');
      setDescription('');
      setStatus(TaskStatusEnum.PENDING);
    }
  }, [task, isOpen]); // Recarregar quando a tarefa ou a visibilidade do modal mudar

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ title, description, status });
    onClose(); // Fecha o modal após a submissão
  };

  const handleDelete = () => {
    if (window.confirm('Tem certeza que deseja excluir esta tarefa?')) {
      onDelete(task.id);
      onClose(); // Fecha o modal após a exclusão
    }
  };

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>{task ? 'Edit Task' : 'Add New Task'}</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title:</label>
            <input
              type="text"
              id="title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">Description:</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
            ></textarea>
          </div>
          <div className="form-group">
            <label htmlFor="status">Status:</label>
            <select
              id="status"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              {Object.values(TaskStatusEnum).map((s) => (
                <option key={s} value={s}>
                  {s.replace('_', ' ').toUpperCase()}
                </option>
              ))}
            </select>
          </div>
          <div className="modal-actions">
            <button type="submit" className="button primary">
              {task ? 'Save Changes' : 'Add Task'}
            </button>
            {task && ( // Botão de deletar aparece apenas em modo edição
              <button type="button" onClick={handleDelete} className="button danger">
                Delete
              </button>
            )}
            <button type="button" onClick={onClose} className="button secondary">
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default TaskModal;