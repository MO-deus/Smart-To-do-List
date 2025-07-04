import React, { useState, useEffect } from "react";
import { Task } from "@/types";

const categories = ["Work", "Personal", "Urgent"];
const priorityOptions = [
  { label: "High", value: 1 },
  { label: "Medium", value: 2 },
  { label: "Low", value: 3 },
];
const statusOptions = ["Pending", "In Progress", "Completed"];

interface EditTaskDrawerProps {
  open: boolean;
  onClose: () => void;
  task: Task | null;
  onSave: (updatedTask: Task) => void;
}

const EditTaskDrawer: React.FC<EditTaskDrawerProps> = ({ open, onClose, task, onSave }) => {
  const [form, setForm] = useState<Task | null>(task);

  useEffect(() => {
    setForm(task);
  }, [task]);

  if (!open || !form) return null;

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) {
    const { name, value } = e.target;
    setForm((prev) => prev ? { ...prev, [name]: name === "priority" ? Number(value) : value } : prev);
  }

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (form) onSave(form);
  }

  return (
    <>
      {/* Overlay */}
      <div
        className="fixed inset-0 z-40 bg-black bg-opacity-60 transition-opacity"
        onClick={onClose}
        aria-label="Close edit drawer"
      />  
      {/* Drawer */}
      <div className={`fixed top-0 right-0 h-full w-full max-w-md z-50 bg-white dark:bg-gray-900 shadow-lg transform transition-transform duration-300 ${open ? "translate-x-0" : "translate-x-full"}`}>
        <div className="p-6 h-full flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Edit Task</h2>
            <button onClick={onClose} className="text-gray-500 hover:text-gray-900 dark:hover:text-white text-2xl">&times;</button>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4 flex-1 overflow-y-auto">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Title</label>
              <input
                name="title"
                type="text"
                className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                value={form.title}
                onChange={handleChange}
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Description</label>
              <textarea
                name="description"
                className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                value={form.description}
                onChange={handleChange}
                rows={2}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Category</label>
              <select
                name="category"
                className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                value={form.category}
                onChange={handleChange}
              >
                {categories.map((cat) => (
                  <option key={cat} value={cat}>{cat}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Priority</label>
              <select
                name="priority"
                className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                value={form.priority}
                onChange={handleChange}
              >
                {priorityOptions.map((opt) => (
                  <option key={opt.value} value={opt.value}>{opt.label}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Status</label>
              <select
                name="status"
                className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                value={form.status}
                onChange={handleChange}
              >
                {statusOptions.map((opt) => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-200 mb-1">Deadline</label>
              <input
                name="deadline"
                type="datetime-local"
                className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
                value={form.deadline ? form.deadline.slice(0, 16) : ""}
                onChange={handleChange}
              />
            </div>
            <div className="flex justify-end gap-2 mt-4">
              <button type="button" className="px-4 py-2 rounded bg-gray-200 dark:bg-gray-700 text-gray-800 dark:text-gray-200" onClick={onClose}>Cancel</button>
              <button type="submit" className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700">Save Changes</button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
};

export default EditTaskDrawer; 