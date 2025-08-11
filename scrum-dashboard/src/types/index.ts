export interface User {
  id: string
  name: string
  email: string
  avatar?: string
  role: 'scrum-master' | 'product-manager' | 'developer' | 'stakeholder'
  mood?: 'happy' | 'neutral' | 'stressed' | 'blocked'
  workload?: 'light' | 'medium' | 'heavy' | 'overloaded'
}

export interface Task {
  id: string
  title: string
  description?: string
  status: 'todo' | 'in-progress' | 'review' | 'done' | 'blocked'
  priority: 'low' | 'medium' | 'high' | 'critical'
  assignee?: User
  reporter: User
  storyPoints?: number
  tags: string[]
  dependencies: string[]
  createdAt: Date
  updatedAt: Date
  dueDate?: Date
  estimatedHours?: number
  actualHours?: number
  blockReason?: string
  aiSuggestions?: AISuggestion[]
}

export interface Sprint {
  id: string
  name: string
  goal: string
  startDate: Date
  endDate: Date
  status: 'planning' | 'active' | 'completed' | 'cancelled'
  tasks: Task[]
  capacity: number
  velocity?: number
  burndownData: BurndownPoint[]
}

export interface BurndownPoint {
  date: Date
  remaining: number
  ideal: number
  actual: number
}

export interface AISuggestion {
  id: string
  type: 'task-creation' | 'priority-adjustment' | 'resource-allocation' | 'risk-mitigation' | 'process-optimization'
  title: string
  description: string
  confidence: number
  impact: 'low' | 'medium' | 'high'
  reasoning: string
  actionable: boolean
  data?: any
  createdAt: Date
}

export interface Comment {
  id: string
  content: string
  author: User
  createdAt: Date
  updatedAt?: Date
  reactions: Reaction[]
  mentions: string[]
  attachments?: Attachment[]
}

export interface Reaction {
  emoji: string
  users: User[]
  count: number
}

export interface Attachment {
  id: string
  name: string
  url: string
  type: string
  size: number
}

export interface Notification {
  id: string
  type: 'task-assigned' | 'task-updated' | 'sprint-started' | 'blocker-reported' | 'ai-suggestion' | 'mention'
  title: string
  message: string
  user: User
  read: boolean
  actionable: boolean
  actionUrl?: string
  createdAt: Date
  priority: 'low' | 'medium' | 'high'
  groupId?: string
}

export interface TeamMetrics {
  velocity: number[]
  burndownRate: number
  cycleTime: number
  leadTime: number
  defectRate: number
  teamMood: Record<string, number>
  workloadDistribution: Record<string, number>
  blockerFrequency: number
  sprintCompletion: number
}

export interface RiskAssessment {
  id: string
  taskId: string
  riskLevel: 'low' | 'medium' | 'high' | 'critical'
  category: 'scope-creep' | 'technical-debt' | 'dependency' | 'resource' | 'external'
  description: string
  impact: string
  mitigation: string[]
  probability: number
  detectedAt: Date
  resolvedAt?: Date
}

export interface DragDropItem {
  id: string
  type: 'task' | 'epic' | 'story'
  content: any
}

export interface CanvasPosition {
  x: number
  y: number
}

export interface ViewportBounds {
  left: number
  top: number
  right: number
  bottom: number
}

export interface FilterOptions {
  status?: string[]
  priority?: string[]
  assignee?: string[]
  tags?: string[]
  dateRange?: {
    start: Date
    end: Date
  }
}

export interface SortOptions {
  field: keyof Task
  direction: 'asc' | 'desc'
}

export type Theme = 'light' | 'dark' | 'system'

export type ViewMode = 'kanban' | 'list' | 'calendar' | 'timeline' | 'canvas'