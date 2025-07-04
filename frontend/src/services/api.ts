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