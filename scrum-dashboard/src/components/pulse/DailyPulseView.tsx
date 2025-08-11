'use client'

import React, { useState, useEffect, useMemo } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Task, User, Notification, AISuggestion } from '@/types'
import { useDashboardStore } from '@/stores/dashboard'
import { cn, formatRelativeTime, getStatusColor } from '@/lib/utils'
import {
  Activity,
  AlertCircle,
  CheckCircle,
  Clock,
  MessageSquare,
  TrendingUp,
  TrendingDown,
  Zap,
  Brain,
  Users,
  Calendar,
  Target,
  Coffee,
  Gauge,
  ArrowUp,
  ArrowDown,
  Minus,
  RefreshCw
} from 'lucide-react'

interface TimelineEvent {
  id: string
  type: 'task_update' | 'comment' | 'blocker' | 'ai_suggestion' | 'sprint_update' | 'standup'
  title: string
  description: string
  timestamp: Date
  user?: User
  task?: Task
  priority: 'low' | 'medium' | 'high'
  icon: React.ReactNode
  color: string
}

interface PulseMetric {
  id: string
  label: string
  value: number
  change: number
  changeType: 'increase' | 'decrease' | 'neutral'
  icon: React.ReactNode
  color: string
  description: string
}

function generateTimelineEvents(tasks: Task[], notifications: Notification[], aiSuggestions: AISuggestion[]): TimelineEvent[] {
  const events: TimelineEvent[] = []

  // Recent task updates
  tasks
    .filter(task => task.updatedAt > new Date(Date.now() - 24 * 60 * 60 * 1000))
    .forEach(task => {
      events.push({
        id: `task-${task.id}`,
        type: 'task_update',
        title: `Task ${task.status === 'done' ? 'completed' : 'updated'}`,
        description: task.title,
        timestamp: task.updatedAt,
        user: task.assignee,
        task,
        priority: task.priority === 'critical' ? 'high' : task.priority === 'high' ? 'medium' : 'low',
        icon: task.status === 'done' ? <CheckCircle className="w-4 h-4" /> : <Activity className="w-4 h-4" />,
        color: task.status === 'done' ? 'text-green-500' : 'text-blue-500'
      })
    })

  // Blockers
  tasks
    .filter(task => task.status === 'blocked')
    .forEach(task => {
      events.push({
        id: `blocker-${task.id}`,
        type: 'blocker',
        title: 'Task blocked',
        description: `${task.title} - ${task.blockReason || 'No reason provided'}`,
        timestamp: task.updatedAt,
        user: task.assignee,
        task,
        priority: 'high',
        icon: <AlertCircle className="w-4 h-4" />,
        color: 'text-red-500'
      })
    })

  // AI suggestions
  aiSuggestions.forEach(suggestion => {
    events.push({
      id: `ai-${suggestion.id}`,
      type: 'ai_suggestion',
      title: 'AI Suggestion',
      description: suggestion.title,
      timestamp: suggestion.createdAt,
      priority: suggestion.impact === 'high' ? 'high' : suggestion.impact === 'medium' ? 'medium' : 'low',
      icon: <Brain className="w-4 h-4" />,
      color: 'text-purple-500'
    })
  })

  // Mock standup notes
  events.push({
    id: 'standup-today',
    type: 'standup',
    title: 'Daily Standup',
    description: 'Team sync completed - 3 blockers identified, 2 tasks completed',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
    priority: 'medium',
    icon: <Coffee className="w-4 h-4" />,
    color: 'text-orange-500'
  })

  // Sort by timestamp descending
  return events.sort((a, b) => b.timestamp.getTime() - a.timestamp.getTime())
}

function TimelineEventCard({ event }: { event: TimelineEvent }) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.3 }}
      className="relative"
    >
      {/* Timeline line */}
      <div className="absolute left-6 top-8 bottom-0 w-px bg-gradient-to-b from-gray-300 to-transparent dark:from-gray-600" />
      
      {/* Timeline dot */}
      <div className={cn(
        'absolute left-4 top-4 w-4 h-4 rounded-full border-2 bg-white dark:bg-gray-900 flex items-center justify-center',
        event.priority === 'high' ? 'border-red-400' :
        event.priority === 'medium' ? 'border-yellow-400' : 'border-green-400'
      )}>
        <div className={cn(
          'w-2 h-2 rounded-full',
          event.priority === 'high' ? 'bg-red-400' :
          event.priority === 'medium' ? 'bg-yellow-400' : 'bg-green-400'
        )} />
      </div>
      
      {/* Content */}
      <div className="ml-12">
        <Card variant="default" className="hover:shadow-md transition-shadow">
          <CardContent className="p-4">
            <div className="space-y-2">
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2">
                  <span className={event.color}>
                    {event.icon}
                  </span>
                  <h4 className="font-medium text-sm">
                    {event.title}
                  </h4>
                </div>
                <span className="text-xs text-muted-foreground">
                  {formatRelativeTime(event.timestamp)}
                </span>
              </div>
              
              <p className="text-sm text-muted-foreground">
                {event.description}
              </p>
              
              {event.user && (
                <div className="flex items-center gap-2 pt-1">
                  <div className="w-4 h-4 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center text-xs font-semibold text-white">
                    {event.user.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <span className="text-xs text-muted-foreground">
                    {event.user.name}
                  </span>
                </div>
              )}
              
              {event.task && (
                <div className="flex items-center gap-2 pt-1">
                  <span className={cn(
                    'px-2 py-1 rounded-full text-xs font-medium border',
                    getStatusColor(event.task.status)
                  )}>
                    {event.task.status.replace('-', ' ')}
                  </span>
                  {event.task.storyPoints && (
                    <span className="text-xs px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-800">
                      {event.task.storyPoints}sp
                    </span>
                  )}
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </motion.div>
  )
}

function PulseMetricsGrid({ metrics }: { metrics: PulseMetric[] }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {metrics.map((metric, index) => (
        <motion.div
          key={metric.id}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: index * 0.1 }}
        >
          <Card variant="elevated" interactive>
            <CardContent className="p-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className={metric.color}>
                    {metric.icon}
                  </span>
                  <div className={cn(
                    'flex items-center gap-1 text-xs px-2 py-1 rounded-full',
                    metric.changeType === 'increase' ? 'text-green-700 bg-green-100 dark:text-green-300 dark:bg-green-900/30' :
                    metric.changeType === 'decrease' ? 'text-red-700 bg-red-100 dark:text-red-300 dark:bg-red-900/30' :
                    'text-gray-700 bg-gray-100 dark:text-gray-300 dark:bg-gray-800'
                  )}>
                    {metric.changeType === 'increase' && <ArrowUp className="w-3 h-3" />}
                    {metric.changeType === 'decrease' && <ArrowDown className="w-3 h-3" />}
                    {metric.changeType === 'neutral' && <Minus className="w-3 h-3" />}
                    {Math.abs(metric.change)}%
                  </div>
                </div>
                
                <div>
                  <div className="text-2xl font-bold">
                    {typeof metric.value === 'number' ? 
                      metric.value % 1 === 0 ? metric.value : metric.value.toFixed(1)
                      : metric.value
                    }
                  </div>
                  <div className="text-xs text-muted-foreground">
                    {metric.label}
                  </div>
                </div>
                
                <p className="text-xs text-muted-foreground leading-relaxed">
                  {metric.description}
                </p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      ))}
    </div>
  )
}

function LiveActivityFeed({ events }: { events: TimelineEvent[] }) {
  const [autoRefresh, setAutoRefresh] = useState(true)
  const [lastUpdate, setLastUpdate] = useState(new Date())

  useEffect(() => {
    if (!autoRefresh) return

    const interval = setInterval(() => {
      setLastUpdate(new Date())
      // In a real app, this would trigger a data refresh
    }, 30000) // Refresh every 30 seconds

    return () => clearInterval(interval)
  }, [autoRefresh])

  return (
    <Card variant="elevated">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Zap className="w-5 h-5 text-yellow-500" />
            Live Activity Feed
          </CardTitle>
          <div className="flex items-center gap-2">
            <span className="text-xs text-muted-foreground">
              Last updated {formatRelativeTime(lastUpdate)}
            </span>
            <Button
              size="sm"
              variant="ghost"
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={cn(
                'h-7 px-2',
                autoRefresh && 'text-green-600 dark:text-green-400'
              )}
            >
              <RefreshCw className={cn(
                'w-3 h-3',
                autoRefresh && 'animate-spin'
              )} />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4 max-h-96 overflow-y-auto scrollbar-thin">
          <AnimatePresence>
            {events.slice(0, 10).map((event) => (
              <TimelineEventCard key={event.id} event={event} />
            ))}
          </AnimatePresence>
          
          {events.length === 0 && (
            <div className="text-center py-8 text-muted-foreground">
              <Activity className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p>No recent activity</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )
}

export default function DailyPulseView() {
  const { 
    tasks, 
    users, 
    notifications, 
    aiSuggestions, 
    currentSprint 
  } = useDashboardStore()

  const timelineEvents = useMemo(() => 
    generateTimelineEvents(tasks, notifications, aiSuggestions), 
    [tasks, notifications, aiSuggestions]
  )

  const pulseMetrics: PulseMetric[] = useMemo(() => {
    const completedTasks = tasks.filter(task => task.status === 'done').length
    const totalTasks = tasks.length
    const blockedTasks = tasks.filter(task => task.status === 'blocked').length
    const velocity = currentSprint?.velocity || 0
    
    return [
      {
        id: 'completion',
        label: 'Completion Rate',
        value: totalTasks ? Math.round((completedTasks / totalTasks) * 100) : 0,
        change: 12,
        changeType: 'increase',
        icon: <Target className="w-5 h-5" />,
        color: 'text-green-500',
        description: 'Tasks completed in current sprint'
      },
      {
        id: 'velocity',
        label: 'Team Velocity',
        value: velocity,
        change: -5,
        changeType: 'decrease',
        icon: <Gauge className="w-5 h-5" />,
        color: 'text-blue-500',
        description: 'Story points per sprint'
      },
      {
        id: 'blockers',
        label: 'Active Blockers',
        value: blockedTasks,
        change: blockedTasks > 2 ? 25 : -15,
        changeType: blockedTasks > 2 ? 'increase' : 'decrease',
        icon: <AlertCircle className="w-5 h-5" />,
        color: 'text-red-500',
        description: 'Tasks currently blocked'
      },
      {
        id: 'mood',
        label: 'Team Mood',
        value: 8.2,
        change: 3,
        changeType: 'increase',
        icon: <Users className="w-5 h-5" />,
        color: 'text-purple-500',
        description: 'Average team satisfaction score'
      }
    ]
  }, [tasks, currentSprint])

  return (
    <div className="space-y-6 p-6">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between"
      >
        <div>
          <h1 className="text-3xl font-bold text-gradient">
            Daily Pulse
          </h1>
          <p className="text-muted-foreground mt-1">
            Real-time insights into your team&apos;s progress and health
          </p>
        </div>
        
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 text-sm text-muted-foreground">
            <Clock className="w-4 h-4" />
            <span>Updated live</span>
          </div>
        </div>
      </motion.div>

      {/* Pulse Metrics */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
      >
        <PulseMetricsGrid metrics={pulseMetrics} />
      </motion.div>

      {/* Activity Feed */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <LiveActivityFeed events={timelineEvents} />
      </motion.div>
    </div>
  )
}