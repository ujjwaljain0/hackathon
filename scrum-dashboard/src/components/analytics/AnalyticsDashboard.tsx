'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
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
  AlertTriangle,
  BarChart3,
  LineChart,
  PieChart,
  Download,
  Filter,
  RefreshCw,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react'

const velocityData = [
  { sprint: 'Sprint 19', planned: 45, completed: 42, efficiency: 93 },
  { sprint: 'Sprint 20', planned: 48, completed: 47, efficiency: 98 },
  { sprint: 'Sprint 21', planned: 50, completed: 45, efficiency: 90 },
  { sprint: 'Sprint 22', planned: 52, completed: 49, efficiency: 94 },
  { sprint: 'Sprint 23', planned: 55, completed: 0, efficiency: 0 }
]

const burndownData = [
  { day: 'Day 1', planned: 55, actual: 55 },
  { day: 'Day 2', planned: 50, actual: 52 },
  { day: 'Day 3', planned: 45, actual: 48 },
  { day: 'Day 4', planned: 40, actual: 42 },
  { day: 'Day 5', planned: 35, actual: 38 },
  { day: 'Day 6', planned: 30, actual: 32 },
  { day: 'Day 7', planned: 25, actual: 26 },
  { day: 'Day 8', planned: 20, actual: 21 },
  { day: 'Day 9', planned: 15, actual: 16 },
  { day: 'Day 10', planned: 10, actual: 12 },
  { day: 'Today', planned: 5, actual: 8 }
]

const teamMetrics = [
  {
    name: 'Sarah Chen',
    role: 'Frontend Dev',
    tasksCompleted: 12,
    tasksInProgress: 3,
    velocity: 15,
    efficiency: 94,
    trend: 'up'
  },
  {
    name: 'Mike Davis',
    role: 'Backend Dev', 
    tasksCompleted: 10,
    tasksInProgress: 4,
    velocity: 14,
    efficiency: 89,
    trend: 'up'
  },
  {
    name: 'Alex Johnson',
    role: 'Full Stack',
    tasksCompleted: 11,
    tasksInProgress: 2,
    velocity: 13,
    efficiency: 91,
    trend: 'down'
  },
  {
    name: 'Emma Wilson',
    role: 'UI/UX Designer',
    tasksCompleted: 8,
    tasksInProgress: 5,
    velocity: 13,
    efficiency: 87,
    trend: 'up'
  }
]

const kpiCards = [
  {
    title: 'Sprint Velocity',
    value: '42',
    unit: 'points',
    change: '+8.5%',
    trend: 'up',
    icon: Target,
    color: 'text-blue-600',
    bg: 'bg-blue-50 dark:bg-blue-950'
  },
  {
    title: 'Team Efficiency',
    value: '94%',
    unit: '',
    change: '+2.1%', 
    trend: 'up',
    icon: TrendingUp,
    color: 'text-green-600',
    bg: 'bg-green-50 dark:bg-green-950'
  },
  {
    title: 'Bug Resolution',
    value: '2.3',
    unit: 'days avg',
    change: '-15%',
    trend: 'up',
    icon: CheckCircle,
    color: 'text-purple-600',
    bg: 'bg-purple-50 dark:bg-purple-950'
  },
  {
    title: 'Code Quality',
    value: '98.2%',
    unit: 'coverage',
    change: '+0.8%',
    trend: 'up',
    icon: AlertTriangle,
    color: 'text-orange-600',
    bg: 'bg-orange-50 dark:bg-orange-950'
  }
]

export default function AnalyticsDashboard() {
  const { currentSprint } = useDashboardStore()

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
            Analytics Dashboard
          </motion.h1>
          <p className="text-muted-foreground mt-1">
            Insights and metrics for Sprint 23
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm" icon={<RefreshCw className="w-4 h-4" />}>
            Refresh
          </Button>
          <Button variant="outline" size="sm" icon={<Filter className="w-4 h-4" />}>
            Filter
          </Button>
          <Button size="sm" icon={<Download className="w-4 h-4" />}>
            Export
          </Button>
        </div>
      </div>

      {/* KPI Cards */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
      >
        {kpiCards.map((kpi, index) => (
          <motion.div
            key={kpi.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 + index * 0.05 }}
          >
            <Card className="hover:shadow-elevated transition-all duration-200">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div className={cn('p-2 rounded-lg', kpi.bg)}>
                    <kpi.icon className={cn('w-5 h-5', kpi.color)} />
                  </div>
                  <div className="flex items-center gap-1 text-xs">
                    {kpi.trend === 'up' ? (
                      <ArrowUpRight className="w-3 h-3 text-green-600" />
                    ) : (
                      <ArrowDownRight className="w-3 h-3 text-red-600" />
                    )}
                    <span className={cn(
                      kpi.trend === 'up' ? 'text-green-600' : 'text-red-600'
                    )}>
                      {kpi.change}
                    </span>
                  </div>
                </div>
                <div className="mt-4">
                  <div className="text-2xl font-bold text-foreground">
                    {kpi.value}
                    {kpi.unit && <span className="text-sm text-muted-foreground ml-1">{kpi.unit}</span>}
                  </div>
                  <div className="text-sm text-muted-foreground">{kpi.title}</div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </motion.div>

      {/* Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Velocity Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg font-semibold flex items-center gap-2">
                  <BarChart3 className="w-5 h-5 text-primary" />
                  Sprint Velocity
                </CardTitle>
                <Badge variant="outline">Last 5 Sprints</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="h-64 flex items-end justify-between gap-2 border-b border-border pb-4">
                {velocityData.map((sprint, index) => {
                  const maxHeight = Math.max(...velocityData.map(s => Math.max(s.planned, s.completed)))
                  const plannedHeight = (sprint.planned / maxHeight) * 200
                  const completedHeight = (sprint.completed / maxHeight) * 200
                  
                  return (
                    <div key={sprint.sprint} className="flex-1 flex flex-col items-center gap-2">
                      <div className="w-full flex justify-center gap-1">
                        <motion.div
                          initial={{ height: 0 }}
                          animate={{ height: plannedHeight }}
                          transition={{ delay: 0.3 + index * 0.1, duration: 0.5 }}
                          className="bg-muted rounded-sm flex-1 min-h-[4px]"
                        />
                        <motion.div
                          initial={{ height: 0 }}
                          animate={{ height: completedHeight }}
                          transition={{ delay: 0.4 + index * 0.1, duration: 0.5 }}
                          className="bg-primary rounded-sm flex-1 min-h-[4px]"
                        />
                      </div>
                      <div className="text-xs text-center">
                        <div className="font-medium text-foreground">{sprint.sprint.replace('Sprint ', 'S')}</div>
                        <div className="text-muted-foreground">{sprint.efficiency}%</div>
                      </div>
                    </div>
                  )
                })}
              </div>
              <div className="mt-4 flex items-center justify-center gap-4 text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-muted rounded-sm" />
                  <span className="text-muted-foreground">Planned</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-3 bg-primary rounded-sm" />
                  <span className="text-muted-foreground">Completed</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Burndown Chart */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
        >
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <CardTitle className="text-lg font-semibold flex items-center gap-2">
                  <LineChart className="w-5 h-5 text-primary" />
                  Sprint Burndown
                </CardTitle>
                <Badge variant="outline">Sprint 23</Badge>
              </div>
            </CardHeader>
            <CardContent>
              <div className="h-64 relative border-l border-b border-border">
                <svg className="absolute inset-0 w-full h-full">
                  {/* Planned line */}
                  <motion.polyline
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ delay: 0.5, duration: 1.5 }}
                    fill="none"
                    stroke="rgb(var(--color-muted-foreground))"
                    strokeWidth="2"
                    strokeDasharray="4,4"
                    points={burndownData.map((point, index) => 
                      `${(index / (burndownData.length - 1)) * 100}%,${100 - (point.planned / 55) * 80}%`
                    ).join(' ')}
                  />
                  
                  {/* Actual line */}
                  <motion.polyline
                    initial={{ pathLength: 0 }}
                    animate={{ pathLength: 1 }}
                    transition={{ delay: 0.7, duration: 1.5 }}
                    fill="none"
                    stroke="rgb(var(--color-primary))"
                    strokeWidth="3"
                    points={burndownData.map((point, index) => 
                      `${(index / (burndownData.length - 1)) * 100}%,${100 - (point.actual / 55) * 80}%`
                    ).join(' ')}
                  />
                </svg>
                
                {/* Data points */}
                {burndownData.map((point, index) => (
                  <motion.div
                    key={point.day}
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ delay: 0.8 + index * 0.05 }}
                    className="absolute w-2 h-2 bg-primary rounded-full -translate-x-1 -translate-y-1"
                    style={{
                      left: `${(index / (burndownData.length - 1)) * 100}%`,
                      top: `${100 - (point.actual / 55) * 80}%`
                    }}
                  />
                ))}
              </div>
              
              <div className="mt-4 flex items-center justify-center gap-4 text-xs">
                <div className="flex items-center gap-2">
                  <div className="w-3 h-0.5 bg-muted-foreground rounded-sm border-dashed border border-muted-foreground" />
                  <span className="text-muted-foreground">Ideal</span>
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-3 h-0.5 bg-primary rounded-sm" />
                  <span className="text-muted-foreground">Actual</span>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Team Performance */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <Card>
          <CardHeader>
            <CardTitle className="text-lg font-semibold flex items-center gap-2">
              <Users className="w-5 h-5 text-primary" />
              Team Performance
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {teamMetrics.map((member, index) => (
                <motion.div
                  key={member.name}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: 0.5 + index * 0.1 }}
                  className="flex items-center justify-between p-4 rounded-lg border border-border hover:bg-accent transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-full bg-gradient-primary flex items-center justify-center">
                      <span className="text-white font-medium text-sm">
                        {member.name.split(' ').map(n => n[0]).join('')}
                      </span>
                    </div>
                    <div>
                      <h4 className="font-medium text-foreground">{member.name}</h4>
                      <p className="text-sm text-muted-foreground">{member.role}</p>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-6">
                    <div className="text-center">
                      <div className="text-lg font-bold text-foreground">{member.tasksCompleted}</div>
                      <div className="text-xs text-muted-foreground">Completed</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-bold text-foreground">{member.tasksInProgress}</div>
                      <div className="text-xs text-muted-foreground">In Progress</div>
                    </div>
                    <div className="text-center">
                      <div className="text-lg font-bold text-foreground">{member.velocity}</div>
                      <div className="text-xs text-muted-foreground">Velocity</div>
                    </div>
                    <div className="text-center">
                      <div className="flex items-center gap-1">
                        <span className="text-lg font-bold text-foreground">{member.efficiency}%</span>
                        {member.trend === 'up' ? (
                          <TrendingUp className="w-4 h-4 text-green-600" />
                        ) : (
                          <TrendingDown className="w-4 h-4 text-red-600" />
                        )}
                      </div>
                      <div className="text-xs text-muted-foreground">Efficiency</div>
                    </div>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}