import React from "react";
import PriorityIndicator from "@/components/PriorityIndicator";

interface TaskCardProps {
  id?: string;
  title?: string;
  description?: string;
  priority?: number;
  categoryName?: string;
  status?: string;
  onEdit?: () => void;
  onDelete?: (taskId: string) => void;
}

const TaskCard: React.FC<TaskCardProps> = ({
  id,
  title = "Sample Task Title",
  description = "This is a sample task description.",
  priority = 2,
  categoryName = "Work",
  status = "Pending",
  onEdit,
  onDelete,
}) => {
  const handleDelete = () => {
    if (!id || !onDelete) return;
    
    const confirmed = window.confirm(
      `Are you sure you want to delete "${title}"? This action cannot be undone.`
    );
    
    if (confirmed) {
      onDelete(id);
    }
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-4 flex items-start gap-4 border border-gray-100 dark:border-gray-700 relative min-h-[120px]">
      <PriorityIndicator priority={priority} />
      <div className="flex-1 flex flex-col justify-between min-h-[80px]">
        <div>
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-semibold text-gray-900 dark:text-white">{title}</h2>
          </div>
          <p className="text-gray-600 dark:text-gray-300 mt-1">{description}</p>
          <div className="mt-2 flex items-center gap-2">
            <span className="text-xs text-gray-500 dark:text-gray-400">Status: {status}</span>
          </div>
        </div>
        <div className="flex justify-end mt-2">
          <span className="text-xs px-2 py-1 rounded bg-blue-100 text-blue-700 dark:bg-blue-900 dark:text-blue-200">{categoryName}</span>
        </div>
      </div>
      <div className="absolute top-2 right-2 flex gap-1">
        {onEdit && (
          <button
            onClick={onEdit}
            className="text-xs px-2 py-1 rounded bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-200 hover:bg-blue-500 hover:text-white transition"
            aria-label="Edit Task"
          >
            Edit
          </button>
        )}
        {onDelete && id && (
          <button
            onClick={handleDelete}
            className="text-xs px-2 py-1 rounded bg-red-200 dark:bg-red-900 text-red-700 dark:text-red-200 hover:bg-red-500 hover:text-white transition"
            aria-label="Delete Task"
          >
            Delete
          </button>
        )}
      </div>
    </div>
  );
};

export default TaskCard; 