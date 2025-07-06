/**
 * ActionButtons component for task actions.
 */

import React from 'react';

interface ActionButtonsProps {
  onEdit: () => void;
  onDelete: () => void;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
}

export const ActionButtons: React.FC<ActionButtonsProps> = ({
  onEdit,
  onDelete,
  className = '',
  size = 'md',
}) => {
  const getSizeClasses = (size: string) => {
    switch (size) {
      case 'sm':
        return 'p-1.5 text-sm';
      case 'lg':
        return 'p-3 text-lg';
      default:
        return 'p-2 text-base';
    }
  };

  const sizeClasses = getSizeClasses(size);

  return (
    <div className={`flex items-center gap-1 ${className}`}>
      <button
        onClick={onEdit}
        className={`
          ${sizeClasses}
          bg-blue-100 text-blue-600 hover:bg-blue-200 dark:bg-blue-900/30 dark:text-blue-400 dark:hover:bg-blue-900/50
          rounded-lg transition-all duration-200 hover:scale-105 hover:shadow-md
          focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800
        `}
        title="Edit task"
        aria-label="Edit task"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
        </svg>
      </button>
      
      <button
        onClick={onDelete}
        className={`
          ${sizeClasses}
          bg-red-100 text-red-600 hover:bg-red-200 dark:bg-red-900/30 dark:text-red-400 dark:hover:bg-red-900/50
          rounded-lg transition-all duration-200 hover:scale-105 hover:shadow-md
          focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 dark:focus:ring-offset-slate-800
        `}
        title="Delete task"
        aria-label="Delete task"
      >
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </button>
    </div>
  );
};

export default ActionButtons; 