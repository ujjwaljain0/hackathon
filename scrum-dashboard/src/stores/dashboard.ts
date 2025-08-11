import { create } from 'zustand'
import { devtools, persist } from 'zustand/middleware'
import { Task, Sprint, User, AISuggestion, Notification, ViewMode, Theme, FilterOptions, SortOptions } from '@/types'
import { mockTasks, mockSprint, mockUsers, mockAISuggestions, mockNotifications } from '@/mocks/data'

interface DashboardState {
  // Data
  currentSprint: Sprint | null
  tasks: Task[]
  users: User[]
  aiSuggestions: AISuggestion[]
  notifications: Notification[]
  
  // UI State
  theme: Theme
  viewMode: ViewMode
  sidebarOpen: boolean
  filterOptions: FilterOptions
  sortOptions: SortOptions
  selectedTaskId: string | null
  
  // Loading states
  isLoading: boolean
  isTasksLoading: boolean
  isSprintLoading: boolean
  
  // Actions
  setTheme: (theme: Theme) => void
  setViewMode: (mode: ViewMode) => void
  setSidebarOpen: (open: boolean) => void
  setFilterOptions: (options: FilterOptions) => void
  setSortOptions: (options: SortOptions) => void
  setSelectedTaskId: (id: string | null) => void
  
  // Data actions
  loadInitialData: () => void
  updateTask: (taskId: string, updates: Partial<Task>) => void
  createTask: (task: Omit<Task, 'id' | 'createdAt' | 'updatedAt'>) => void
  deleteTask: (taskId: string) => void
  moveTask: (taskId: string, newStatus: Task['status']) => void
  
  // AI actions
  acceptAISuggestion: (suggestionId: string) => void
  dismissAISuggestion: (suggestionId: string) => void
  
  // Notification actions
  markNotificationRead: (notificationId: string) => void
  markAllNotificationsRead: () => void
  
  // Real-time updates
  addRealtimeUpdate: (update: any) => void
}

export const useDashboardStore = create<DashboardState>()(
  devtools(
    persist(
      (set, get) => ({
        // Initial state
        currentSprint: null,
        tasks: [],
        users: [],
        aiSuggestions: [],
        notifications: [],
        
        theme: 'system',
        viewMode: 'kanban',
        sidebarOpen: true,
        filterOptions: {},
        sortOptions: { field: 'priority', direction: 'desc' },
        selectedTaskId: null,
        
        isLoading: false,
        isTasksLoading: false,
        isSprintLoading: false,
        
        // Theme actions
        setTheme: (theme) => set({ theme }),
        setViewMode: (viewMode) => set({ viewMode }),
        setSidebarOpen: (sidebarOpen) => set({ sidebarOpen }),
        setFilterOptions: (filterOptions) => set({ filterOptions }),
        setSortOptions: (sortOptions) => set({ sortOptions }),
        setSelectedTaskId: (selectedTaskId) => set({ selectedTaskId }),
        
        // Data actions
        loadInitialData: () => {
          set({ isLoading: true })
          
          // Simulate API delay
          setTimeout(() => {
            set({
              currentSprint: mockSprint,
              tasks: mockTasks,
              users: mockUsers,
              aiSuggestions: mockAISuggestions,
              notifications: mockNotifications,
              isLoading: false
            })
          }, 1000)
        },
        
        updateTask: (taskId, updates) => {
          set((state) => ({
            tasks: state.tasks.map((task) =>
              task.id === taskId
                ? { ...task, ...updates, updatedAt: new Date() }
                : task
            )
          }))
        },
        
        createTask: (taskData) => {
          const newTask: Task = {
            ...taskData,
            id: `task-${Date.now()}`,
            createdAt: new Date(),
            updatedAt: new Date()
          }
          
          set((state) => ({
            tasks: [...state.tasks, newTask]
          }))
        },
        
        deleteTask: (taskId) => {
          set((state) => ({
            tasks: state.tasks.filter((task) => task.id !== taskId)
          }))
        },
        
        moveTask: (taskId, newStatus) => {
          set((state) => ({
            tasks: state.tasks.map((task) =>
              task.id === taskId
                ? { ...task, status: newStatus, updatedAt: new Date() }
                : task
            )
          }))
        },
        
        // AI actions
        acceptAISuggestion: (suggestionId) => {
          const suggestion = get().aiSuggestions.find(s => s.id === suggestionId)
          if (!suggestion) return
          
          // Handle different suggestion types
          switch (suggestion.type) {
            case 'task-creation':
              // Create a new task based on the suggestion
              get().createTask({
                title: suggestion.title,
                description: suggestion.description,
                status: 'todo',
                priority: 'medium',
                reporter: get().users[0], // Current user
                storyPoints: 3,
                tags: [],
                dependencies: []
              })
              break
              
            case 'priority-adjustment':
              // Find related tasks and update priority
              const tasksToUpdate = get().tasks.filter(task => 
                task.title.toLowerCase().includes('database') ||
                task.tags.includes('performance')
              )
              
              tasksToUpdate.forEach(task => {
                get().updateTask(task.id, { priority: 'high' })
              })
              break
              
            default:
              console.log('Handling suggestion:', suggestion.type)
          }
          
          // Remove the suggestion
          set((state) => ({
            aiSuggestions: state.aiSuggestions.filter(s => s.id !== suggestionId)
          }))
        },
        
        dismissAISuggestion: (suggestionId) => {
          set((state) => ({
            aiSuggestions: state.aiSuggestions.filter(s => s.id !== suggestionId)
          }))
        },
        
        // Notification actions
        markNotificationRead: (notificationId) => {
          set((state) => ({
            notifications: state.notifications.map(notif =>
              notif.id === notificationId
                ? { ...notif, read: true }
                : notif
            )
          }))
        },
        
        markAllNotificationsRead: () => {
          set((state) => ({
            notifications: state.notifications.map(notif => ({ ...notif, read: true }))
          }))
        },
        
        // Real-time updates
        addRealtimeUpdate: (update) => {
          console.log('Real-time update received:', update)
          // Handle different types of real-time updates
          switch (update.type) {
            case 'task_updated':
              get().updateTask(update.taskId, update.changes)
              break
            case 'new_ai_suggestion':
              set((state) => ({
                aiSuggestions: [...state.aiSuggestions, update.suggestion]
              }))
              break
            case 'new_notification':
              set((state) => ({
                notifications: [...state.notifications, update.notification]
              }))
              break
            default:
              console.log('Unknown update type:', update.type)
          }
        }
      }),
      {
        name: 'dashboard-store',
        partialize: (state) => ({
          theme: state.theme,
          viewMode: state.viewMode,
          sidebarOpen: state.sidebarOpen,
          filterOptions: state.filterOptions,
          sortOptions: state.sortOptions
        })
      }
    )
  )
)

// Computed selectors
export const useFilteredTasks = () => {
  const { tasks, filterOptions, sortOptions } = useDashboardStore()
  
  let filteredTasks = tasks
  
  // Apply filters
  if (filterOptions.status?.length) {
    filteredTasks = filteredTasks.filter(task => 
      filterOptions.status!.includes(task.status)
    )
  }
  
  if (filterOptions.priority?.length) {
    filteredTasks = filteredTasks.filter(task => 
      filterOptions.priority!.includes(task.priority)
    )
  }
  
  if (filterOptions.assignee?.length) {
    filteredTasks = filteredTasks.filter(task => 
      task.assignee && filterOptions.assignee!.includes(task.assignee.id)
    )
  }
  
  if (filterOptions.tags?.length) {
    filteredTasks = filteredTasks.filter(task => 
      task.tags.some(tag => filterOptions.tags!.includes(tag))
    )
  }
  
  // Apply sorting
  filteredTasks.sort((a, b) => {
    const field = sortOptions.field
    const direction = sortOptions.direction === 'asc' ? 1 : -1
    
    let aVal: any = a[field]
    let bVal: any = b[field]
    
    // Handle different field types
    if (field === 'priority') {
      const priorityOrder = { low: 1, medium: 2, high: 3, critical: 4 }
      aVal = priorityOrder[a.priority]
      bVal = priorityOrder[b.priority]
    } else if (field === 'createdAt' || field === 'updatedAt') {
      aVal = (aVal as Date).getTime()
      bVal = (bVal as Date).getTime()
    }
    
    // Handle undefined values
    if (aVal == null && bVal == null) return 0
    if (aVal == null) return -1 * direction
    if (bVal == null) return 1 * direction
    
    if (aVal < bVal) return -1 * direction
    if (aVal > bVal) return 1 * direction
    return 0
  })
  
  return filteredTasks
}

export const useUnreadNotifications = () => {
  const notifications = useDashboardStore(state => state.notifications)
  return notifications.filter(notif => !notif.read)
}