import { User, Task, Sprint, AISuggestion, Comment, Notification, TeamMetrics } from '@/types'

export const mockUsers: User[] = [
  {
    id: '1',
    name: 'Sarah Chen',
    email: 'sarah.chen@company.com',
    avatar: 'https://images.unsplash.com/photo-1494790108755-2616b1e10d44?w=150&h=150&fit=crop&crop=face',
    role: 'scrum-master',
    mood: 'happy',
    workload: 'medium'
  },
  {
    id: '2',
    name: 'Alex Rodriguez',
    email: 'alex.rodriguez@company.com',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face',
    role: 'developer',
    mood: 'neutral',
    workload: 'heavy'
  },
  {
    id: '3',
    name: 'Maya Patel',
    email: 'maya.patel@company.com',
    avatar: 'https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=150&h=150&fit=crop&crop=face',
    role: 'product-manager',
    mood: 'stressed',
    workload: 'overloaded'
  },
  {
    id: '4',
    name: 'Jordan Kim',
    email: 'jordan.kim@company.com',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&h=150&fit=crop&crop=face',
    role: 'developer',
    mood: 'happy',
    workload: 'light'
  },
  {
    id: '5',
    name: 'Emma Thompson',
    email: 'emma.thompson@company.com',
    avatar: 'https://images.unsplash.com/photo-1502685104226-ee32379fefbe?w=150&h=150&fit=crop&crop=face',
    role: 'stakeholder',
    mood: 'neutral',
    workload: 'medium'
  }
]

export const mockAISuggestions: AISuggestion[] = [
  {
    id: 'ai-1',
    type: 'task-creation',
    title: 'Create API integration tests',
    description: 'Based on recent code changes, I suggest adding comprehensive API integration tests to prevent regression issues.',
    confidence: 0.85,
    impact: 'high',
    reasoning: 'Recent changes to authentication endpoints show increased complexity. Historical data shows 40% of bugs in similar features come from integration issues.',
    actionable: true,
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000)
  },
  {
    id: 'ai-2',
    type: 'priority-adjustment',
    title: 'Increase priority of database optimization',
    description: 'Performance metrics indicate database queries are becoming a bottleneck. Consider prioritizing optimization tasks.',
    confidence: 0.92,
    impact: 'high',
    reasoning: 'Query response time has increased 40% over the last sprint. This affects 3 critical user flows.',
    actionable: true,
    createdAt: new Date(Date.now() - 4 * 60 * 60 * 1000)
  },
  {
    id: 'ai-3',
    type: 'resource-allocation',
    title: 'Redistribute frontend tasks',
    description: 'Alex Rodriguez appears to be overloaded with frontend tasks. Consider redistributing to Jordan Kim.',
    confidence: 0.78,
    impact: 'medium',
    reasoning: 'Alex has 8 active tasks vs team average of 4. Jordan has capacity and matching skill set.',
    actionable: true,
    createdAt: new Date(Date.now() - 6 * 60 * 60 * 1000)
  }
]

export const mockTasks: Task[] = [
  {
    id: 'task-1',
    title: 'Implement user authentication flow',
    description: 'Create secure login/logout functionality with JWT tokens and password reset capability.',
    status: 'in-progress',
    priority: 'high',
    assignee: mockUsers[1],
    reporter: mockUsers[2],
    storyPoints: 8,
    tags: ['backend', 'security', 'api'],
    dependencies: [],
    createdAt: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
    dueDate: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
    estimatedHours: 16,
    actualHours: 12,
    aiSuggestions: [mockAISuggestions[0]]
  },
  {
    id: 'task-2',
    title: 'Design dashboard wireframes',
    description: 'Create low-fidelity wireframes for the main dashboard interface.',
    status: 'done',
    priority: 'medium',
    assignee: mockUsers[4],
    reporter: mockUsers[2],
    storyPoints: 3,
    tags: ['design', 'ux'],
    dependencies: [],
    createdAt: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
    estimatedHours: 8,
    actualHours: 6
  },
  {
    id: 'task-3',
    title: 'Optimize database queries',
    description: 'Improve performance of user data queries and implement proper indexing.',
    status: 'todo',
    priority: 'critical',
    assignee: mockUsers[1],
    reporter: mockUsers[0],
    storyPoints: 5,
    tags: ['backend', 'performance', 'database'],
    dependencies: ['task-1'],
    createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
    dueDate: new Date(Date.now() + 5 * 24 * 60 * 60 * 1000),
    estimatedHours: 12,
    aiSuggestions: [mockAISuggestions[1]]
  },
  {
    id: 'task-4',
    title: 'Setup CI/CD pipeline',
    description: 'Configure automated testing and deployment pipeline using GitHub Actions.',
    status: 'blocked',
    priority: 'high',
    assignee: mockUsers[3],
    reporter: mockUsers[0],
    storyPoints: 13,
    tags: ['devops', 'automation'],
    dependencies: [],
    createdAt: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 1 * 60 * 60 * 1000),
    blockReason: 'Waiting for DevOps team to provide access credentials',
    estimatedHours: 20
  },
  {
    id: 'task-5',
    title: 'Implement responsive navigation',
    description: 'Create mobile-friendly navigation component with smooth animations.',
    status: 'review',
    priority: 'medium',
    assignee: mockUsers[3],
    reporter: mockUsers[2],
    storyPoints: 5,
    tags: ['frontend', 'responsive', 'ui'],
    dependencies: ['task-2'],
    createdAt: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000),
    updatedAt: new Date(Date.now() - 3 * 60 * 60 * 1000),
    estimatedHours: 10,
    actualHours: 9
  }
]

export const mockSprint: Sprint = {
  id: 'sprint-1',
  name: 'Sprint 23 - Authentication & Performance',
  goal: 'Deliver secure user authentication and improve system performance',
  startDate: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
  endDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000),
  status: 'active',
  tasks: mockTasks,
  capacity: 120,
  velocity: 28,
  burndownData: [
    {
      date: new Date(Date.now() - 7 * 24 * 60 * 60 * 1000),
      remaining: 34,
      ideal: 34,
      actual: 34
    },
    {
      date: new Date(Date.now() - 6 * 24 * 60 * 60 * 1000),
      remaining: 31,
      ideal: 31,
      actual: 32
    },
    {
      date: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000),
      remaining: 28,
      ideal: 28,
      actual: 29
    },
    {
      date: new Date(Date.now() - 4 * 24 * 60 * 60 * 1000),
      remaining: 25,
      ideal: 25,
      actual: 26
    },
    {
      date: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000),
      remaining: 22,
      ideal: 22,
      actual: 21
    },
    {
      date: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
      remaining: 19,
      ideal: 19,
      actual: 18
    },
    {
      date: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
      remaining: 16,
      ideal: 16,
      actual: 15
    },
    {
      date: new Date(),
      remaining: 13,
      ideal: 13,
      actual: 13
    }
  ]
}

export const mockComments: Comment[] = [
  {
    id: 'comment-1',
    content: 'Great progress on the authentication flow! The JWT implementation looks solid.',
    author: mockUsers[0],
    createdAt: new Date(Date.now() - 2 * 60 * 60 * 1000),
    reactions: [
      { emoji: '👍', users: [mockUsers[1], mockUsers[2]], count: 2 },
      { emoji: '🚀', users: [mockUsers[3]], count: 1 }
    ],
    mentions: ['alex.rodriguez']
  },
  {
    id: 'comment-2',
    content: 'Blocked on the CI/CD setup - still waiting for the DevOps team. @maya.patel can you help escalate?',
    author: mockUsers[3],
    createdAt: new Date(Date.now() - 1 * 60 * 60 * 1000),
    reactions: [],
    mentions: ['maya.patel']
  }
]

export const mockNotifications: Notification[] = [
  {
    id: 'notif-1',
    type: 'ai-suggestion',
    title: 'New AI Suggestion',
    message: 'AI suggests creating API integration tests based on recent code changes.',
    user: mockUsers[0],
    read: false,
    actionable: true,
    actionUrl: '/suggestions',
    createdAt: new Date(Date.now() - 30 * 60 * 1000),
    priority: 'medium'
  },
  {
    id: 'notif-2',
    type: 'task-assigned',
    title: 'New Task Assigned',
    message: 'You have been assigned to "Optimize database queries"',
    user: mockUsers[1],
    read: false,
    actionable: true,
    actionUrl: '/tasks/task-3',
    createdAt: new Date(Date.now() - 45 * 60 * 1000),
    priority: 'high'
  },
  {
    id: 'notif-3',
    type: 'blocker-reported',
    title: 'Blocker Reported',
    message: 'Jordan Kim reported a blocker on CI/CD pipeline setup',
    user: mockUsers[0],
    read: true,
    actionable: true,
    actionUrl: '/tasks/task-4',
    createdAt: new Date(Date.now() - 1 * 60 * 60 * 1000),
    priority: 'high'
  }
]

export const mockTeamMetrics: TeamMetrics = {
  velocity: [22, 28, 31, 25, 34, 29],
  burndownRate: 0.85,
  cycleTime: 4.2,
  leadTime: 8.7,
  defectRate: 0.12,
  teamMood: {
    happy: 40,
    neutral: 40,
    stressed: 15,
    blocked: 5
  },
  workloadDistribution: {
    light: 20,
    medium: 40,
    heavy: 30,
    overloaded: 10
  },
  blockerFrequency: 0.08,
  sprintCompletion: 0.92
}