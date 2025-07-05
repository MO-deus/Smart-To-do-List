import React, { useState, useEffect } from "react";
import { createCategory, createTask } from "@/services/api";
import CategoryDropdown from "@/components/CategoryDropdown";
import { useCategories } from "@/contexts/CategoriesContext";

interface QuickAddTaskModalProps {
  open: boolean;
  onClose: () => void;
  onAddTask: (task: any) => void;
}

const priorityOptions = [
  { label: "High", value: 1 },
  { label: "Medium", value: 2 },
  { label: "Low", value: 3 },
];

const QuickAddTaskModal: React.FC<QuickAddTaskModalProps> = ({ open, onClose, onAddTask }) => {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [category, setCategory] = useState<string>("");
  const [priority, setPriority] = useState(2);
  const [showNewCategory, setShowNewCategory] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const { refreshCategories } = useCategories();

  // Reset form when modal opens/closes
  useEffect(() => {
    if (!open) {
      setTitle("");
      setDescription("");
      setCategory("");
      setPriority(2);
      setShowNewCategory(false);
      setNewCategoryName("");
    }
  }, [open]);

  const handleCreateCategory = async () => {
    if (!newCategoryName.trim()) return;
    
    try {
      setIsLoading(true);
      const newCat = await createCategory(newCategoryName.trim());
      await refreshCategories(); // Refresh the categories list
      setCategory(newCat.id);
      setShowNewCategory(false);
      setNewCategoryName("");
    } catch (error) {
      console.error("Failed to create category:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !category) return;
    
    try {
      setIsLoading(true);
      const newTask = await createTask({
        title: title.trim(),
        description: description.trim(),
        category: category,
        priority,
        status: 'Pending'
      });
      
      // Call the parent's onAddTask with the created task
      onAddTask(newTask);
      
      // Reset form
      setTitle("");
      setDescription("");
      setCategory("");
      setPriority(2);
      onClose();
    } catch (error) {
      console.error("Failed to create task:", error);
    } finally {
      setIsLoading(false);
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-60">
      <div className="bg-white dark:bg-gray-900 rounded-lg shadow-lg p-6 w-full max-w-md">
        <h2 className="text-xl font-bold mb-4 text-gray-900 dark:text-white">Quick Add Task</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Title</label>
            <input
              type="text"
              className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Description</label>
            <textarea
              className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={2}
              disabled={isLoading}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Category</label>
            <CategoryDropdown
              value={category}
              onChange={setCategory}
              onCreateNewCategory={() => setShowNewCategory(true)}
              disabled={isLoading}
            />
            {showNewCategory && (
              <div className="flex gap-2 mt-2">
                <input
                  type="text"
                  value={newCategoryName}
                  onChange={e => setNewCategoryName(e.target.value)}
                  placeholder="New category name"
                  className="border px-2 py-1 rounded flex-1"
                  required
                  disabled={isLoading}
                />
                <button 
                  type="button" 
                  onClick={handleCreateCategory} 
                  className="bg-blue-600 text-white px-3 py-1 rounded disabled:opacity-50"
                  disabled={isLoading}
                >
                  Add
                </button>
                <button 
                  type="button" 
                  onClick={() => setShowNewCategory(false)} 
                  className="px-3 py-1 rounded"
                  disabled={isLoading}
                >
                  Cancel
                </button>
              </div>
            )}
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Priority</label>
            <select
              className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              value={priority}
              onChange={(e) => setPriority(Number(e.target.value))}
              disabled={isLoading}
            >
              {priorityOptions.map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          </div>
          <div className="flex justify-end gap-2 mt-4">
            <button 
              type="button" 
              className="px-4 py-2 rounded bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200" 
              onClick={onClose}
              disabled={isLoading}
            >
              Cancel
            </button>
            <button 
              type="submit" 
              className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50"
              disabled={isLoading}
            >
              {isLoading ? "Adding..." : "Add Task"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default QuickAddTaskModal; 