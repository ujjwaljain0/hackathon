// User types
export interface User {
  id: string;
  name: string;
  email: string;
  avatar: string;
  role: 'scrum-master' | 'developer' | 'product-manager' | 'stakeholder';
  mood: 'happy' | 'neutral' | 'stressed' | 'blocked';
  workload: 'light' | 'medium' | 'heavy' | 'overloaded';
}

// Task types
export interface Task {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in-progress' | 'review' | 'blocked' | 'done';
  priority: 'low' | 'medium' | 'high' | 'critical';
  assignee?: User;
  reporter: User;
  storyPoints: number;
  tags: string[];
  dependencies: string[];
  createdAt: Date;
  updatedAt: Date;
  dueDate?: Date;
  estimatedHours?: number;
  actualHours?: number;
  blockReason?: string;
  aiSuggestions?: AISuggestion[];
}

// Sprint types
export interface Sprint {
  id: string;
  name: string;
  goal: string;
  startDate: Date;
  endDate: Date;
  status: 'planning' | 'active' | 'review' | 'completed';
  tasks: Task[];
  capacity: number;
  velocity: number;
  burndownData: BurndownDataPoint[];
}

export interface BurndownDataPoint {
  date: Date;
  remaining: number;
  ideal: number;
  actual: number;
}

// AI types
export interface AISuggestion {
  id: string;
  type: 'task-creation' | 'priority-adjustment' | 'resource-allocation';
  title: string;
  description: string;
  confidence: number;
  impact: 'low' | 'medium' | 'high';
  reasoning: string;
  actionable: boolean;
  createdAt: Date;
}

// Comment types
export interface Comment {
  id: string;
  content: string;
  author: User;
  createdAt: Date;
  reactions: Reaction[];
  mentions: string[];
}

export interface Reaction {
  emoji: string;
  users: User[];
  count: number;
}

// Notification types
export interface Notification {
  id: string;
  type: 'ai-suggestion' | 'task-assigned' | 'blocker-reported' | 'comment' | 'mention';
  title: string;
  message: string;
  user: User;
  read: boolean;
  actionable: boolean;
  actionUrl?: string;
  createdAt: Date;
  priority: 'low' | 'medium' | 'high';
}

// Team metrics
export interface TeamMetrics {
  velocity: number[];
  burndownRate: number;
  cycleTime: number;
  leadTime: number;
  defectRate: number;
  teamMood: {
    happy: number;
    neutral: number;
    stressed: number;
    blocked: number;
  };
  workloadDistribution: {
    light: number;
    medium: number;
    heavy: number;
    overloaded: number;
  };
  blockerFrequency: number;
  sprintCompletion: number;
}

// UI types
export type Theme = 'light' | 'dark' | 'system';
export type ViewMode = 'kanban' | 'list' | 'calendar' | 'timeline';

export interface FilterOptions {
  status?: string[];
  priority?: string[];
  assignee?: string[];
  tags?: string[];
}

export interface SortOptions {
  field: string;
  direction: 'asc' | 'desc';
}
