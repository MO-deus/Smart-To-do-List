"use client";
import { useEffect, useState } from "react";
import TaskCard from "@/components/TaskCard";
import CategoryFilter from "@/components/CategoryFilter";
import QuickAddTaskModal from "@/components/QuickAddTaskModal";
import EditTaskDrawer from "@/components/EditTaskDrawer";
import { fetchTasks, deleteTask } from "@/services/api";
import { Task } from "@/types";
import { useCategories } from "@/contexts/CategoriesContext";


const statusOptions = ["All", "Pending", "In Progress", "Completed"];
const priorityOptions = ["All", "High", "Medium", "Low"];

function getPriorityNumber(label: string) {
  if (label === "High") return 1;
  if (label === "Medium") return 2;
  if (label === "Low") return 3;
  return undefined;
}

export default function DashboardPage() {
  const [category, setCategory] = useState<string | "All">("All");
  const [status, setStatus] = useState("All");
  const [priority, setPriority] = useState("All");
  const [search, setSearch] = useState("");
  const [showModal, setShowModal] = useState(false);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [editTask, setEditTask] = useState<Task | null>(null);
  const { categories } = useCategories();

  useEffect(() => {
    fetchTasks()
      .then(data => setTasks(data))
      .catch(() => setTasks([]))
      .finally(() => setLoading(false));
  }, []);

  const filteredTasks = tasks.filter((task) => {
    const matchesCategory = category === "All" || task.category === category;
    const matchesStatus = status === "All" || task.status === status;
    const matchesPriority =
      priority === "All" || task.priority === getPriorityNumber(priority);
    const matchesSearch =
      search === "" ||
      task.title.toLowerCase().includes(search.toLowerCase()) ||
      task.description.toLowerCase().includes(search.toLowerCase());
    return (
      matchesCategory && matchesStatus && matchesPriority && matchesSearch
    );
  });

  function handleAddTask(newTask: Task) {
    setTasks([newTask, ...tasks]);
  }

  function handleSaveTask(updatedTask: Task) {
    setTasks((prev) => prev.map((t) => t.id === updatedTask.id ? updatedTask : t));
    setEditTask(null);
  }

  async function handleDeleteTask(taskId: string) {
    try {
      await deleteTask(taskId);
      setTasks((prev) => prev.filter((t) => t.id !== taskId));
    } catch (error) {
      console.error("Failed to delete task:", error);
      alert("Failed to delete task. Please try again.");
    }
  }

  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 p-6">
      <div className="max-w-4xl mx-auto">
        <header className="flex items-center justify-between mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Smart Todo Dashboard</h1>
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
            onClick={() => setShowModal(true)}
          >
            + Add Task
          </button>
        </header>
        <section className="mb-6 flex flex-col gap-4 sm:flex-row sm:items-center sm:gap-6">
          <div>
            <CategoryFilter value={category} onChange={setCategory} />
          </div>
          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-200 mr-2">Status:</label>
            <select
              className="border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              value={status}
              onChange={(e) => setStatus(e.target.value)}
            >
              {statusOptions.map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="text-sm font-medium text-gray-700 dark:text-gray-200 mr-2">Priority:</label>
            <select
              className="border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
            >
              {priorityOptions.map((opt) => (
                <option key={opt} value={opt}>{opt}</option>
              ))}
            </select>
          </div>
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search tasks..."
              className="w-full border border-gray-300 dark:border-gray-700 rounded px-2 py-1 bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
        </section>
        <section>
          <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">Your Tasks</h2>
          <div className="space-y-4">
            {filteredTasks.length === 0 ? (
              <div className="text-gray-500 dark:text-gray-400">No tasks found.</div>
            ) : (
              filteredTasks.map((task) => (
                <TaskCard
                  key={task.id}
                  id={task.id}
                  title={task.title}
                  description={task.description}
                  priority={task.priority}
                  categoryName={categories.find(cat => cat.id === task.category)?.name || "Unknown"}
                  status={task.status}
                  onEdit={() => setEditTask(task)}
                  onDelete={handleDeleteTask}
                />
              ))
            )}
          </div>
        </section>
        <QuickAddTaskModal
          open={showModal}
          onClose={() => setShowModal(false)}
          onAddTask={handleAddTask}
        />
        <EditTaskDrawer
          open={!!editTask}
          onClose={() => setEditTask(null)}
          task={editTask}
          onSave={handleSaveTask}
        />
      </div>
    </main>
  );
}
