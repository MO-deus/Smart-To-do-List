export async function fetchTasks() {
  const res = await fetch('http://127.0.0.1:8000/api/tasks/');
  if (!res.ok) throw new Error('Failed to fetch tasks');
  return res.json();
}

export async function fetchCategories() {
  const res = await fetch('http://127.0.0.1:8000/api/categories/');
  if (!res.ok) throw new Error('Failed to fetch categories');
  return res.json();
}

export async function fetchContextEntries() {
  const res = await fetch('http://127.0.0.1:8000/api/context/');
  if (!res.ok) throw new Error('Failed to fetch context entries');
  return res.json();
}

export async function createCategory(name: string) {
  const res = await fetch('http://127.0.0.1:8000/api/categories/create/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error('Failed to create category');
  return res.json();
}

// creating a new task
export async function createTask(task: {
  title: string;
  description: string;
  category: string;
  priority: number;
  deadline?: string;
  status?: string;
}) {
  const res = await fetch('http://127.0.0.1:8000/api/tasks/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(task),
  });
  if (!res.ok) throw new Error('Failed to create task');
  return res.json();
}

// updating an existing task
export async function updateTask(taskId: string, task: {
  title: string;
  description: string;
  category: string;
  priority: number;
  deadline?: string;
  status?: string;
}) {
  const res = await fetch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(task),
  });
  if (!res.ok) throw new Error('Failed to update task');
  return res.json();
}