/**
 * Enhanced TaskCard component for displaying task information.
 * 
 * This component provides a comprehensive view of a task with actions,
 * status indicators, and responsive design.
 */

import React, { useMemo } from 'react';
import { 
  Task, 
  TaskStatus, 
  TaskPriority, 
  TaskCardProps,
  TASK_CONSTANTS 
} from '@/types';
import { PriorityIndicator } from './PriorityIndicator';
import { StatusBadge } from './StatusBadge';
import { CategoryBadge } from './CategoryBadge';
import { DeadlineIndicator } from './DeadlineIndicator';
import { ActionButtons } from './ActionButtons';
import { useCategories } from "@/contexts/CategoriesContext";

/**
 * TaskCard component
 */
export const TaskCard: React.FC<TaskCardProps> = ({
  task,
  onEdit,
  onDelete,
  onStatusChange,
  onPriorityChange,
  showActions = true,
  compact = false,
  className = '',
  disabled = false,
  loading = false,
}) => {
  const { categories } = useCategories();
  const category = categories.find((cat) => cat.id === task.category);

  /**
   * Calculate task urgency indicators
   */
  const urgencyIndicators = useMemo(() => {
    const now = new Date();
    const deadline = task.deadline ? new Date(task.deadline) : null;
    
    if (!deadline) {
      return {
        isOverdue: false,
        isDueSoon: false,
        daysUntilDeadline: null,
        urgencyLevel: 'normal' as const,
      };
    }

    const daysUntilDeadline = Math.ceil((deadline.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
    const isOverdue = daysUntilDeadline < 0;
    const isDueSoon = daysUntilDeadline >= 0 && daysUntilDeadline <= TASK_CONSTANTS.DUE_SOON_THRESHOLD_DAYS;
    
    let urgencyLevel: 'normal' | 'warning' | 'critical' = 'normal';
    if (isOverdue) {
      urgencyLevel = 'critical';
    } else if (isDueSoon) {
      urgencyLevel = 'warning';
    }

    return {
      isOverdue,
      isDueSoon,
      daysUntilDeadline,
      urgencyLevel,
    };
  }, [task.deadline]);

  /**
   * Handle status change
   */
  const handleStatusChange = (newStatus: TaskStatus) => {
    if (onStatusChange && !disabled) {
      onStatusChange(task.id, newStatus);
    }
  };

  /**
   * Handle priority change
   */
  const handlePriorityChange = (newPriority: TaskPriority) => {
    if (onPriorityChange && !disabled) {
      onPriorityChange(task.id, newPriority);
    }
  };

  /**
   * Handle edit action
   */
  const handleEdit = () => {
    if (onEdit && !disabled) {
      onEdit(task);
    }
  };

  /**
   * Handle delete action
   */
  const handleDelete = () => {
    if (onDelete && !disabled) {
      const confirmed = window.confirm(
        `Are you sure you want to delete "${task.title}"? This action cannot be undone.`
      );
      
      if (confirmed) {
        onDelete(task.id);
      }
    }
  };

  /**
   * Get card border color based on urgency
   */
  const getBorderColor = () => {
    if (urgencyIndicators.urgencyLevel === 'critical') {
      return 'border-red-300 dark:border-red-600';
    }
    if (urgencyIndicators.urgencyLevel === 'warning') {
      return 'border-yellow-300 dark:border-yellow-600';
    }
    return 'border-gray-200 dark:border-gray-700';
  };

  /**
   * Get card background color based on status
   */
  const getBackgroundColor = () => {
    if (task.status === TaskStatus.COMPLETED) {
      return 'bg-green-50 dark:bg-green-900/20';
    }
    if (task.status === TaskStatus.IN_PROGRESS) {
      return 'bg-blue-50 dark:bg-blue-900/20';
    }
    return 'bg-white dark:bg-gray-800';
  };

  return (
    <div className="group bg-white/80 dark:bg-slate-800/80 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 dark:border-slate-700/50 hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1">
      {/* Loading overlay */}
      {loading && (
        <div className="absolute inset-0 bg-white/50 dark:bg-gray-800/50 rounded-lg flex items-center justify-center z-10">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600"></div>
        </div>
      )}

      <div className="flex items-start gap-3">
        {/* Priority indicator */}
        <div className="flex-shrink-0">
          <PriorityIndicator 
            priority={task.priority}
            size={compact ? 'sm' : 'md'}
          />
        </div>

        {/* Main content */}
        <div className="flex-1 min-w-0">
          {/* Header with enhanced styling */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex-1 min-w-0">
              <h3 className="text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2 line-clamp-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors duration-200">
                {task.title}
              </h3>
              
              {task.description && (
                <p className="text-slate-600 dark:text-slate-400 text-sm line-clamp-3 leading-relaxed">
                  {task.description}
                </p>
              )}
            </div>
            
            <div className="flex items-center gap-2 ml-4">
              <StatusBadge 
                status={task.status}
                size={compact ? 'sm' : 'md'}
              />
            </div>
          </div>

          {/* Enhanced metadata section */}
          <div className="flex flex-wrap items-center gap-3 mb-4">
            {category && (
              <CategoryBadge name={category.name} />
            )}
            
            {task.deadline && (
              <DeadlineIndicator
                deadline={task.deadline}
                isOverdue={urgencyIndicators.isOverdue}
                isDueSoon={urgencyIndicators.isDueSoon}
                daysUntilDeadline={urgencyIndicators.daysUntilDeadline}
                compact={compact}
              />
            )}
            
            {/* Task ID for debugging */}
            {task.id && (
              <span className="text-xs text-slate-400 dark:text-slate-500 font-mono">
                #{task.id.slice(-6)}
              </span>
            )}
          </div>


        </div>

        {/* Action buttons */}
        {showActions && (
          <ActionButtons
            onEdit={handleEdit}
            onDelete={handleDelete}
            size={compact ? 'sm' : 'md'}
          />
        )}
      </div>

      {/* Urgency indicator bar */}
      {urgencyIndicators.urgencyLevel !== 'normal' && (
        <div 
          className={`
            absolute bottom-0 left-0 right-0 h-1 rounded-b-lg
            ${urgencyIndicators.urgencyLevel === 'critical' 
              ? 'bg-red-500' 
              : 'bg-yellow-500'
            }
          `}
        />
      )}

      {/* Subtle gradient overlay on hover */}
      <div className="absolute inset-0 bg-gradient-to-r from-blue-500/5 to-purple-500/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none" />
    </div>
  );
};

/**
 * Default export
 */
export default TaskCard; 