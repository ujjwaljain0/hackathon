'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Avatar } from '@/components/ui/Avatar'
import { Badge } from '@/components/ui/Badge'
import { useDashboardStore } from '@/stores/dashboard'
import { cn } from '@/lib/utils'
import {
  TrendingUp,
  TrendingDown,
  Activity,
  Users,
  Calendar,
  Clock,
  Target,
  CheckCircle,
  AlertCircle,
  Zap,
  BarChart3,
  ArrowRight,
  Plus,
  Filter,
  MoreHorizontal
} from 'lucide-react'

const statsCards = [
  {
    title: 'Sprint Progress',
    value: '68%',
    change: '+12%',
    trend: 'up',
    icon: Target,
    color: 'text-blue-600',
    bg: 'bg-blue-50 dark:bg-blue-950'
  },
  {
    title: 'Team Velocity',
    value: '42',
    change: '-3%',
    trend: 'down',
    icon: TrendingUp,
    color: 'text-green-600',
    bg: 'bg-green-50 dark:bg-green-950'
  },
  {
    title: 'Active Tasks',
    value: '24',
    change: '+6%',
    trend: 'up',
    icon: Activity,
    color: 'text-purple-600',
    bg: 'bg-purple-50 dark:bg-purple-950'
  },
  {
    title: 'Team Members',
    value: '12',
    change: '0%',
    trend: 'neutral',
    icon: Users,
    color: 'text-orange-600',
    bg: 'bg-orange-50 dark:bg-orange-950'
  }
]

const recentTasks = [
  {
    id: 1,
    title: 'Implement user authentication',
    status: 'in-progress',
    assignee: { name: 'Alex Johnson', avatar: 'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face' },
    priority: 'high',
    dueDate: '2024-01-15'
  },
  {
    id: 2,
    title: 'Design system components',
    status: 'review',
    assignee: { name: 'Sarah Chen', avatar: 'https://images.unsplash.com/photo-1494790108755-2616b1e10d44?w=150&h=150&fit=crop&crop=face' },
    priority: 'medium',
    dueDate: '2024-01-18'
  },
  {
    id: 3,
    title: 'API performance optimization',
    status: 'todo',
    assignee: { name: 'Mike Davis', avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&h=150&fit=crop&crop=face' },
    priority: 'critical',
    dueDate: '2024-01-20'
  }
]

const upcomingEvents = [
  { id: 1, title: 'Daily Standup', time: '9:00 AM', type: 'meeting' },
  { id: 2, title: 'Sprint Review', time: '2:00 PM', type: 'review' },
  { id: 3, title: 'Client Demo', time: '4:00 PM', type: 'demo' }
]

export default function OverviewDashboard() {
  const { currentSprint, tasks, users } = useDashboardStore()

  return (
    <div className="p-6 space-y-6 h-full overflow-y-auto scrollbar-thin">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <motion.h1 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="text-3xl font-bold text-foreground"
          >
            Good morning, Alex 👋
          </motion.h1>
          <p className="text-muted-foreground mt-1">
            Here&apos;s what&apos;s happening with your team today
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" icon={<Filter className="w-4 h-4" />}>
            Filter
          </Button>
          <Button size="sm" icon={<Plus className="w-4 h-4" />}>
            New Task
          </Button>
        </div>
      </div>

      {/* Stats Grid */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {statsCards.map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + index * 0.05 }}
          >
            <Card className="hover:shadow-elevated transition-all duration-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className={cn('p-2 rounded-lg', stat.bg)}>
                    <stat.icon className={cn('w-5 h-5', stat.color)} />
                  </div>
                  <div className="flex items-center gap-1 text-xs">
                    {stat.trend === 'up' ? (
                      <TrendingUp className="w-3 h-3 text-green-600" />
                    ) : stat.trend === 'down' ? (
                      <TrendingDown className="w-3 h-3 text-red-600" />
                    ) : null}
                    <span className={cn(
                      stat.trend === 'up' ? 'text-green-600' :
                      stat.trend === 'down' ? 'text-red-600' :
                      'text-muted-foreground'
                    )}>
                      {stat.change}
                    </span>
                  </div>
                </div>
                <div className="mt-4">
                  <div className="text-2xl font-bold text-foreground">{stat.value}</div>
                  <div className="text-sm text-muted-foreground">{stat.title}</div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {/* Main Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Recent Tasks */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="lg:col-span-2"
        >
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg font-semibold">Recent Tasks</CardTitle>
                <Button variant="ghost" size="sm">
                  View All <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {recentTasks.map((task, index) => (
                  <motion.div
                    key={task.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + index * 0.1 }}
                    className="flex items-center justify-between p-4 rounded-lg border border-border hover:bg-accent transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <div className={cn(
                        'w-2 h-2 rounded-full',
                        task.status === 'in-progress' ? 'bg-blue-500' :
                        task.status === 'review' ? 'bg-yellow-500' :
                        task.status === 'todo' ? 'bg-gray-400' : 'bg-green-500'
                      )} />
                      <div className="flex-1">
                        <h4 className="font-medium text-foreground">{task.title}</h4>
                        <div className="flex items-center gap-2 mt-1">
                          <Badge 
                            variant={
                              task.priority === 'critical' ? 'destructive' :
                              task.priority === 'high' ? 'secondary' : 'outline'
                            }
                            className="text-xs"
                          >
                            {task.priority}
                          </Badge>
                          <span className="text-xs text-muted-foreground">Due {task.dueDate}</span>
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-3">
                      <Avatar size="sm" src={task.assignee.avatar} alt={task.assignee.name} />
                      <Button variant="ghost" size="icon-sm">
                        <MoreHorizontal className="w-4 h-4" />
                      </Button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Today&apos;s Schedule */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="text-lg font-semibold flex items-center gap-2">
                  <Calendar className="w-5 h-5 text-primary" />
                  Today&apos;s Schedule
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {upcomingEvents.map((event, index) => (
                    <motion.div
                      key={event.id}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.4 + index * 0.1 }}
                      className="flex items-center gap-3 p-3 rounded-lg bg-accent"
                    >
                      <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center">
                        <Clock className="w-4 h-4 text-primary-foreground" />
                      </div>
                      <div className="flex-1">
                        <h4 className="font-medium text-sm text-foreground">{event.title}</h4>
                        <p className="text-xs text-muted-foreground">{event.time}</p>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Team Status */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="text-lg font-semibold flex items-center gap-2">
                  <Users className="w-5 h-5 text-primary" />
                  Team Status
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {users.slice(0, 4).map((user, index) => (
                    <motion.div
                      key={user.id}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.5 + index * 0.1 }}
                      className="flex items-center justify-between"
                    >
                      <div className="flex items-center gap-3">
                        <Avatar size="sm" src={user.avatar} alt={user.name} online={true} />
                        <div>
                          <h4 className="font-medium text-sm text-foreground">{user.name}</h4>
                          <p className="text-xs text-muted-foreground capitalize">{user.role.replace('-', ' ')}</p>
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm">
                          {user.mood === 'happy' ? '😊' :
                           user.mood === 'neutral' ? '😐' :
                           user.mood === 'stressed' ? '😰' : '🚫'}
                        </span>
                        <Badge 
                          variant={
                            user.workload === 'overloaded' ? 'destructive' :
                            user.workload === 'heavy' ? 'secondary' : 'outline'
                          }
                          className="text-xs"
                        >
                          {user.workload}
                        </Badge>
                      </div>
                    </motion.div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </motion.div>

          {/* Quick Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card>
              <CardHeader>
                <CardTitle className="text-lg font-semibold flex items-center gap-2">
                  <Zap className="w-5 h-5 text-primary" />
                  Quick Actions
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-3">
                  <Button variant="outline" size="sm" className="h-auto p-3 flex-col gap-2">
                    <Plus className="w-4 h-4" />
                    <span className="text-xs">New Task</span>
                  </Button>
                  <Button variant="outline" size="sm" className="h-auto p-3 flex-col gap-2">
                    <Calendar className="w-4 h-4" />
                    <span className="text-xs">Schedule</span>
                  </Button>
                  <Button variant="outline" size="sm" className="h-auto p-3 flex-col gap-2">
                    <BarChart3 className="w-4 h-4" />
                    <span className="text-xs">Analytics</span>
                  </Button>
                  <Button variant="outline" size="sm" className="h-auto p-3 flex-col gap-2">
                    <Users className="w-4 h-4" />
                    <span className="text-xs">Team</span>
                  </Button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  )
}