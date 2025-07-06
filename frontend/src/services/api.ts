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
  const res = await fetch('http://127.0.0.1:8000/api/categories/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name }),
  });
  
  const data = await res.json();
  
  if (!res.ok) {
    throw new Error(`Failed to create category: ${res.status} ${res.statusText} - ${JSON.stringify(data)}`);
  }
  
  // Return the actual category object from the response
  return data.data;
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
  // Convert category to category_id for backend compatibility
  const taskData: any = {
    ...task,
    category_id: task.category,
  };
  delete taskData.category;
  
  const res = await fetch('http://127.0.0.1:8000/api/tasks/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData),
  });
  
  const data = await res.json();
  
  if (!res.ok) {
    throw new Error(`Failed to create task: ${res.status} ${res.statusText} - ${JSON.stringify(data)}`);
  }
  
  // Return the actual task object from the response
  return data.data;
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
  // Convert category to category_id for backend compatibility
  const taskData: any = {
    ...task,
    category_id: task.category,
  };
  delete taskData.category;
  
  const res = await fetch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(taskData),
  });
  if (!res.ok) throw new Error('Failed to update task');
  
  const data = await res.json();
  // Return the actual task object from the response
  return data.data;
}

// deleting a task
export async function deleteTask(taskId: string) {
  const res = await fetch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete task');
  
  // DELETE requests often return empty responses, so we don't try to parse JSON
  if (res.status === 204 || res.headers.get('content-length') === '0') {
    return null;
  }
  
  // Only try to parse JSON if there's actually content
  const text = await res.text();
  if (text) {
    return JSON.parse(text);
  }
  
  return null;
}

// AI Service Functions
export async function aiHealthCheck() {
  const res = await fetch('http://127.0.0.1:8000/api/ai/health-check/');
  if (!res.ok) throw new Error('AI health check failed');
  return res.json();
}

export async function aiProcessTask(taskData: any, contextData?: any) {
  const res = await fetch('http://127.0.0.1:8000/api/ai/process-task/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task: taskData, context: contextData }),
  });
  if (!res.ok) throw new Error('AI task processing failed');
  return res.json();
}

export async function aiSuggestCategory(taskData: any) {
  const res = await fetch('http://127.0.0.1:8000/api/ai/suggest-category/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task: taskData }),
  });
  if (!res.ok) throw new Error('AI category suggestion failed');
  return res.json();
}

export async function aiEnhanceDescription(taskData: any, contextData?: any) {
  const res = await fetch('http://127.0.0.1:8000/api/ai/enhance-description/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ task: taskData, context: contextData }),
  });
  if (!res.ok) throw new Error('AI description enhancement failed');
  return res.json();
}

export async function aiAnalyzeContext(contextData: any) {
  const res = await fetch('http://127.0.0.1:8000/api/ai/analyze-context/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ context: contextData }),
  });
  if (!res.ok) throw new Error('AI context analysis failed');
  return res.json();
}

export async function aiCreateEnhancedTask(taskData: any, contextData?: any, autoCreate: boolean = false) {
  const res = await fetch('http://127.0.0.1:8000/api/ai/create-enhanced-task/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ 
      task: taskData, 
      context: contextData, 
      auto_create: autoCreate 
    }),
  });
  if (!res.ok) throw new Error('AI enhanced task creation failed');
  return res.json();
}