/** Essential TypeScript types for the todo application. */

// ============================================================================
// ENUMS
// ============================================================================

export enum TaskPriority { HIGH = 1, MEDIUM = 2, LOW = 3 }
export enum TaskStatus { PENDING = 'Pending', IN_PROGRESS = 'In Progress', COMPLETED = 'Completed' }
export enum ContextSourceType { WHATSAPP = 'WhatsApp', EMAIL = 'Email', NOTE = 'Note' }

// ============================================================================
// CORE ENTITIES
// ============================================================================

export interface Task {
  id: string;
  title: string;
  description: string;
  category?: string;
  categoryName?: string;
  priority: TaskPriority;
  deadline?: string;
  status: TaskStatus;
  createdAt: string;
  updatedAt: string;
}

export interface Category {
  id: string;
  name: string;
  usageFrequency: number;
}

export interface ContextEntry {
  id: string;
  content: string;
  sourceType: ContextSourceType;
  processedInsights?: string;
  createdAt: string;
}

// ============================================================================
// API TYPES
// ============================================================================

export interface CreateTaskRequest {
  title: string;
  description: string;
  category?: string;
  priority: TaskPriority;
  deadline?: string;
  status?: TaskStatus;
}

export interface CreateCategoryRequest { 
  name: string; 
}

// ============================================================================
// AI TYPES
// ============================================================================

export interface DeadlineSuggestion {
  date: string; // ISO format (YYYY-MM-DD)
  reason: string;
  urgency: 'high' | 'medium' | 'low';
  confidence: number;
}

export interface ContextAnalysisResult {
  extracted_tasks?: Array<{
    title: string;
    description: string;
    priority: 'high' | 'medium' | 'low';
    deadline?: string;
    category?: string;
    confidence: number;
  }>;
  priority_insights?: {
    urgency_level?: 'high' | 'medium' | 'low';
    insights?: string;
  };
  workload_analysis?: {
    workload_level?: 'high' | 'medium' | 'low';
    suggested_deadlines?: DeadlineSuggestion[];
    insights?: string;
  };
  category_suggestions?: Array<{
    name: string;
    reason: string;
    confidence: number;
    relevance: 'high' | 'medium' | 'low';
  }>;
  context_summary?: string;
}

// ============================================================================
// COMPONENT PROPS
// ============================================================================

export interface TaskCardProps {
  task: Task;
  onEdit?: (task: Task) => void;
  onDelete?: (taskId: string) => void;
  onStatusChange?: (taskId: string, status: TaskStatus) => void;
  onPriorityChange?: (taskId: string, priority: TaskPriority) => void;
  showActions?: boolean;
  compact?: boolean;
  className?: string;
  disabled?: boolean;
  loading?: boolean;
}

// ============================================================================
// CONSTANTS
// ============================================================================

export const TASK_CONSTANTS = {
  DUE_SOON_THRESHOLD_DAYS: 7,
} as const;

// ============================================================================
// TYPE GUARDS
// ============================================================================

export function isTask(obj: any): obj is Task {
  return obj && typeof obj.id === 'string' && typeof obj.title === 'string' && 
         typeof obj.description === 'string' && typeof obj.priority === 'number' && 
         typeof obj.status === 'string';
}

export function isCategory(obj: any): obj is Category {
  return obj && typeof obj.id === 'string' && typeof obj.name === 'string' && 
         typeof obj.usageFrequency === 'number';
}

export function isTaskPriority(value: any): value is TaskPriority {
  return Object.values(TaskPriority).includes(value);
}

export function isTaskStatus(value: any): value is TaskStatus {
  return Object.values(TaskStatus).includes(value);
} 