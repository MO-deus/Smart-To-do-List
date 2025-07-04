import { Task, ContextEntry, Category } from "@/types";

export const mockTasks: Task[] = [
  {
    id: "1",
    title: "Finish AI-powered todo app",
    description: "Complete the frontend and backend for the smart todo list.",
    category: "Work",
    priority: 1,
    deadline: "2024-07-05T17:00:00Z",
    status: "In Progress",
    createdAt: "2024-07-01T09:00:00Z",
    updatedAt: "2024-07-02T10:00:00Z",
  },
  {
    id: "2",
    title: "Buy groceries",
    description: "Milk, eggs, bread, and vegetables.",
    category: "Personal",
    priority: 3,
    deadline: "2024-07-03T18:00:00Z",
    status: "Pending",
    createdAt: "2024-07-01T12:00:00Z",
    updatedAt: "2024-07-01T12:00:00Z",
  },
  {
    id: "3",
    title: "Reply to client emails",
    description: "Respond to all pending client queries.",
    category: "Work",
    priority: 2,
    deadline: "2024-07-02T15:00:00Z",
    status: "Pending",
    createdAt: "2024-07-01T10:00:00Z",
    updatedAt: "2024-07-01T10:00:00Z",
  },
];

export const mockContextEntries: ContextEntry[] = [
  {
    id: "c1",
    content: "Don't forget the team meeting at 3pm.",
    sourceType: "WhatsApp",
    processedInsights: "Meeting scheduled for 3pm.",
    createdAt: "2024-07-01T08:00:00Z",
  },
  {
    id: "c2",
    content: "Grocery list: Milk, eggs, bread, vegetables.",
    sourceType: "Note",
    createdAt: "2024-07-01T09:30:00Z",
  },
  {
    id: "c3",
    content: "Client: Please send the updated proposal by tomorrow.",
    sourceType: "Email",
    processedInsights: "Proposal deadline: tomorrow.",
    createdAt: "2024-07-01T11:00:00Z",
  },
];

export const mockCategories: Category[] = [
  { id: "cat1", name: "Work", usageFrequency: 12 },
  { id: "cat2", name: "Personal", usageFrequency: 7 },
  { id: "cat3", name: "Urgent", usageFrequency: 3 },
]; 