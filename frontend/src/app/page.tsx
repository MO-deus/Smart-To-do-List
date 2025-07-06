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
      .then(data => setTasks(data.data))
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
    // Ensure the task has an id before adding it to the list
    if (newTask && newTask.id) {
      setTasks([newTask, ...tasks]);
    } else {
      console.error('Task created but missing ID:', newTask);
      // Refresh the task list to get the latest data
      fetchTasks()
        .then(data => setTasks(data.data))
        .catch(error => {
          console.error('Failed to refresh tasks after creation:', error);
          alert('Task created but failed to refresh the list. Please refresh the page.');
        });
    }
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
    <main className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 dark:from-slate-900 dark:via-slate-800 dark:to-slate-900">
      <div className="max-w-7xl mx-auto p-6">
        {/* Header with enhanced styling */}
        <header className="mb-8">
          <div className="text-center mb-6">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-indigo-600 bg-clip-text text-transparent mb-2">
              Smart Todo Dashboard
            </h1>
            <p className="text-slate-600 dark:text-slate-400 text-lg">
              Organize your tasks with AI-powered insights
            </p>
          </div>
          
          <div className="flex justify-center">
            <button
              className="group relative px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-semibold shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-1 hover:scale-105"
              onClick={() => setShowModal(true)}
            >
              <span className="flex items-center gap-2">
                <svg className="w-5 h-5 group-hover:rotate-90 transition-transform duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                </svg>
                Add New Task
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-blue-700 to-purple-700 rounded-xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 -z-10"></div>
            </button>
          </div>
        </header>

        {/* Enhanced Filters Section */}
        <section className="mb-8 relative z-30 overflow-visible">
          <div className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 dark:border-slate-700/50 overflow-visible">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="space-y-2 relative overflow-visible">
                <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">Category</label>
                <CategoryFilter value={category} onChange={setCategory} />
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">Status</label>
                <select
                  className="w-full px-4 py-2 bg-white/80 dark:bg-slate-700/80 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={status}
                  onChange={(e) => setStatus(e.target.value)}
                >
                  {statusOptions.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">Priority</label>
                <select
                  className="w-full px-4 py-2 bg-white/80 dark:bg-slate-700/80 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                >
                  {priorityOptions.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              </div>
              
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-700 dark:text-slate-300">Search</label>
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search tasks..."
                    className="w-full px-4 py-2 pl-10 bg-white/80 dark:bg-slate-700/80 border border-slate-200 dark:border-slate-600 rounded-xl text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                  />
                  <svg className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Enhanced Tasks Section */}
        <section>
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-slate-800 dark:text-slate-200">
              Your Tasks
              <span className="ml-2 text-sm font-normal text-slate-500 dark:text-slate-400">
                ({filteredTasks.length} {filteredTasks.length === 1 ? 'task' : 'tasks'})
              </span>
            </h2>
            
            {loading && (
              <div className="flex items-center gap-2 text-slate-600 dark:text-slate-400">
                <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
                Loading tasks...
              </div>
            )}
          </div>
          
          <div className="space-y-4">
            {filteredTasks.length === 0 ? (
              <div className="text-center py-12">
                <div className="bg-white/70 dark:bg-slate-800/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20 dark:border-slate-700/50">
                  <svg className="w-16 h-16 mx-auto text-slate-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                  <h3 className="text-lg font-semibold text-slate-700 dark:text-slate-300 mb-2">No tasks found</h3>
                  <p className="text-slate-500 dark:text-slate-400">
                    {search || category !== "All" || status !== "All" || priority !== "All" 
                      ? "Try adjusting your filters to see more tasks."
                      : "Get started by adding your first task!"}
                  </p>
                </div>
              </div>
            ) : (
              filteredTasks.map((task) => (
                <div key={task.id || `task-${Math.random()}`} className="card-hover">
                  <TaskCard
                    task={task}
                    onEdit={() => setEditTask(task)}
                    onDelete={handleDeleteTask}
                  />
                </div>
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
