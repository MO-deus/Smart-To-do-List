export interface Task {
  id: string;
  title: string;
  description: string;
  category: string;
  priority: number; // 1=High, 2=Medium, 3=Low
  deadline: string; // ISO date string
  status: "Pending" | "In Progress" | "Completed";
  createdAt: string;
  updatedAt: string;
}

export interface ContextEntry {
  id: string;
  content: string;
  sourceType: "WhatsApp" | "Email" | "Note";
  processedInsights?: string;
  createdAt: string;
}

export interface Category {
  id: string;
  name: string;
  usageFrequency: number;
} 