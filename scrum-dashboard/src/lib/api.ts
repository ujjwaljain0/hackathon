import { Task, Sprint, User, AISuggestion, Notification, TeamMetrics } from '@/types'

// Simulate API delay
const delay = (ms: number) => new Promise(resolve => setTimeout(resolve, ms))

// Mock API responses
export class APIClient {
  private baseUrl: string
  
  constructor(baseUrl = '/api') {
    this.baseUrl = baseUrl
  }

  // Tasks API
  async getTasks(sprintId?: string): Promise<Task[]> {
    await delay(500)
    
    // In a real app, this would make an HTTP request
    // For now, we'll return mock data that matches the current state
    const response = await fetch(`${this.baseUrl}/tasks${sprintId ? `?sprintId=${sprintId}` : ''}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      }
    }).catch(() => {
      // Fallback to mock data if fetch fails (for demo purposes)
      return {
        ok: true,
        json: async () => {
          const { mockTasks } = await import('@/mocks/data')
          return mockTasks
        }
      } as Response
    })
    
    if (!response.ok) {
      throw new Error('Failed to fetch tasks')
    }
    
    return response.json()
  }

  async createTask(task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>): Promise<Task> {
    await delay(800)
    
    const newTask: Task = {
      ...task,
      id: `task-${Date.now()}`,
      createdAt: new Date(),
      updatedAt: new Date()
    }

    const response = await fetch(`${this.baseUrl}/tasks`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newTask)
    }).catch(() => {
      // Return mock success response
      return {
        ok: true,
        json: async () => newTask
      } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to create task')
    }

    return response.json()
  }

  async updateTask(taskId: string, updates: Partial<Task>): Promise<Task> {
    await delay(300)
    
    const response = await fetch(`${this.baseUrl}/tasks/${taskId}`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updates)
    }).catch(async () => {
      // Return mock updated task
      const { mockTasks } = await import('@/mocks/data')
      const existingTask = mockTasks.find(t => t.id === taskId)
      if (!existingTask) throw new Error('Task not found')
      
      return {
        ok: true,
        json: async () => ({
          ...existingTask,
          ...updates,
          updatedAt: new Date()
        })
      } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to update task')
    }

    return response.json()
  }

  async deleteTask(taskId: string): Promise<void> {
    await delay(300)
    
    const response = await fetch(`${this.baseUrl}/tasks/${taskId}`, {
      method: 'DELETE'
    }).catch(() => {
      // Return mock success response
      return { ok: true } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to delete task')
    }
  }

  // Sprint API
  async getCurrentSprint(): Promise<Sprint | null> {
    await delay(400)
    
    const response = await fetch(`${this.baseUrl}/sprints/current`).catch(async () => {
      const { mockSprint } = await import('@/mocks/data')
      return {
        ok: true,
        json: async () => mockSprint
      } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to fetch current sprint')
    }

    return response.json()
  }

  async getSprints(limit = 10): Promise<Sprint[]> {
    await delay(600)
    
    const response = await fetch(`${this.baseUrl}/sprints?limit=${limit}`).catch(async () => {
      const { mockSprint } = await import('@/mocks/data')
      return {
        ok: true,
        json: async () => [mockSprint]
      } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to fetch sprints')
    }

    return response.json()
  }

  // Users API
  async getUsers(): Promise<User[]> {
    await delay(300)
    
    const response = await fetch(`${this.baseUrl}/users`).catch(async () => {
      const { mockUsers } = await import('@/mocks/data')
      return {
        ok: true,
        json: async () => mockUsers
      } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to fetch users')
    }

    return response.json()
  }

  // AI Suggestions API
  async getAISuggestions(): Promise<AISuggestion[]> {
    await delay(700)
    
    const response = await fetch(`${this.baseUrl}/ai/suggestions`).catch(async () => {
      const { mockAISuggestions } = await import('@/mocks/data')
      return {
        ok: true,
        json: async () => mockAISuggestions
      } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to fetch AI suggestions')
    }

    return response.json()
  }

  async acceptAISuggestion(suggestionId: string): Promise<void> {
    await delay(500)
    
    const response = await fetch(`${this.baseUrl}/ai/suggestions/${suggestionId}/accept`, {
      method: 'POST'
    }).catch(() => {
      return { ok: true } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to accept AI suggestion')
    }
  }

  async dismissAISuggestion(suggestionId: string): Promise<void> {
    await delay(200)
    
    const response = await fetch(`${this.baseUrl}/ai/suggestions/${suggestionId}/dismiss`, {
      method: 'POST'
    }).catch(() => {
      return { ok: true } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to dismiss AI suggestion')
    }
  }

  // Notifications API
  async getNotifications(): Promise<Notification[]> {
    await delay(300)
    
    const response = await fetch(`${this.baseUrl}/notifications`).catch(async () => {
      const { mockNotifications } = await import('@/mocks/data')
      return {
        ok: true,
        json: async () => mockNotifications
      } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to fetch notifications')
    }

    return response.json()
  }

  async markNotificationRead(notificationId: string): Promise<void> {
    await delay(200)
    
    const response = await fetch(`${this.baseUrl}/notifications/${notificationId}/read`, {
      method: 'POST'
    }).catch(() => {
      return { ok: true } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to mark notification as read')
    }
  }

  // Analytics API
  async getTeamMetrics(sprintId?: string): Promise<TeamMetrics> {
    await delay(800)
    
    const response = await fetch(`${this.baseUrl}/analytics/team${sprintId ? `?sprintId=${sprintId}` : ''}`).catch(async () => {
      const { mockTeamMetrics } = await import('@/mocks/data')
      return {
        ok: true,
        json: async () => mockTeamMetrics
      } as Response
    })

    if (!response.ok) {
      throw new Error('Failed to fetch team metrics')
    }

    return response.json()
  }

  // Real-time updates (WebSocket simulation)
  subscribeToUpdates(onUpdate: (update: any) => void): () => void {
    // Simulate real-time updates with periodic events
    const interval = setInterval(() => {
      // Randomly generate different types of updates
      const updateTypes = ['task_updated', 'new_ai_suggestion', 'new_notification']
      const randomType = updateTypes[Math.floor(Math.random() * updateTypes.length)]
      
      const update = {
        type: randomType,
        timestamp: new Date(),
        data: {
          // Mock update data based on type
          ...(randomType === 'task_updated' && {
            taskId: `task-${Math.floor(Math.random() * 5) + 1}`,
            changes: { status: 'in-progress' }
          }),
          ...(randomType === 'new_ai_suggestion' && {
            suggestion: {
              id: `ai-${Date.now()}`,
              type: 'task-creation',
              title: 'AI detected a potential issue',
              description: 'Consider adding tests for the new authentication module',
              confidence: 0.87,
              impact: 'medium',
              reasoning: 'Test coverage analysis shows gaps in error handling',
              actionable: true,
              createdAt: new Date()
            }
          }),
          ...(randomType === 'new_notification' && {
            notification: {
              id: `notif-${Date.now()}`,
              type: 'task-updated',
              title: 'Task Status Changed',
              message: 'Authentication flow task moved to review',
              user: { id: '1', name: 'System' },
              read: false,
              actionable: true,
              createdAt: new Date(),
              priority: 'medium'
            }
          })
        }
      }
      
      onUpdate(update)
    }, 15000) // Update every 15 seconds

    // Return cleanup function
    return () => clearInterval(interval)
  }
}

// Export singleton instance
export const apiClient = new APIClient()

// Query keys for React Query
export const queryKeys = {
  tasks: (sprintId?: string) => ['tasks', sprintId].filter(Boolean),
  currentSprint: () => ['sprint', 'current'],
  sprints: (limit?: number) => ['sprints', limit],
  users: () => ['users'],
  aiSuggestions: () => ['ai', 'suggestions'],
  notifications: () => ['notifications'],
  teamMetrics: (sprintId?: string) => ['analytics', 'team', sprintId].filter(Boolean),
}