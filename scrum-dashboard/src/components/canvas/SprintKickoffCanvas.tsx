'use client'

import React, { useState, useCallback, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
  DragEndEvent,
  DragStartEvent,
  DragOverlay,
  useDndMonitor
} from '@dnd-kit/core'
import {
  SortableContext,
  sortableKeyboardCoordinates,
  verticalListSortingStrategy,
  useSortable
} from '@dnd-kit/sortable'
import {
  CSS
} from '@dnd-kit/utilities'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { Button } from '@/components/ui/Button'
import { Task, AISuggestion, User } from '@/types'
import { useDashboardStore } from '@/stores/dashboard'
import { cn, getStatusColor, getPriorityIcon } from '@/lib/utils'
import { 
  Plus, 
  Sparkles, 
  Users, 
  Clock, 
  Target, 
  TrendingUp,
  Brain,
  Zap,
  AlertTriangle,
  CheckCircle,
  Circle,
  ArrowRight
} from 'lucide-react'

interface TaskCardProps {
  task: Task
  isDragging?: boolean
}

function TaskCard({ task, isDragging = false }: TaskCardProps) {
  const {
    attributes,
    listeners,
    setNodeRef,
    transform,
    transition,
    isDragging: isSortableDragging,
  } = useSortable({ id: task.id })

  const style = {
    transform: CSS.Transform.toString(transform),
    transition,
  }

  const cardContent = (
    <Card
      variant={isDragging || isSortableDragging ? "elevated" : "default"}
      interactive={!isDragging}
      className={cn(
        'w-full cursor-grab active:cursor-grabbing transition-all duration-200',
        isDragging && 'rotate-3 scale-105 shadow-2xl',
        isSortableDragging && 'opacity-50'
      )}
    >
      <CardHeader className="pb-2">
        <div className="flex items-start justify-between gap-2">
          <CardTitle className="text-sm font-medium leading-tight">
            {task.title}
          </CardTitle>
          <div className="flex items-center gap-1 flex-shrink-0">
            <span className="text-xs">{getPriorityIcon(task.priority)}</span>
            <span className="text-xs px-1.5 py-0.5 rounded-full bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300">
              {task.storyPoints}
            </span>
          </div>
        </div>
      </CardHeader>
      <CardContent className="pt-0">
        <div className="space-y-2">
          <p className="text-xs text-muted-foreground line-clamp-2">
            {task.description}
          </p>
          
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              {task.assignee && (
                <div className="flex items-center gap-1">
                  <div className="w-5 h-5 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center text-[8px] font-semibold text-white">
                    {task.assignee.name.split(' ').map(n => n[0]).join('')}
                  </div>
                </div>
              )}
              
              <div className={cn(
                'px-2 py-0.5 rounded-full text-xs font-medium border',
                getStatusColor(task.status)
              )}>
                {task.status.replace('-', ' ')}
              </div>
            </div>
          </div>
          
          {task.tags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {task.tags.slice(0, 3).map((tag) => (
                <span
                  key={tag}
                  className="px-1.5 py-0.5 text-xs rounded-md bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200"
                >
                  {tag}
                </span>
              ))}
              {task.tags.length > 3 && (
                <span className="px-1.5 py-0.5 text-xs rounded-md bg-gray-100 text-gray-600 dark:bg-gray-800 dark:text-gray-400">
                  +{task.tags.length - 3}
                </span>
              )}
            </div>
          )}
          
          {task.aiSuggestions && task.aiSuggestions.length > 0 && (
            <div className="flex items-center gap-1 text-xs text-purple-600 dark:text-purple-400">
              <Sparkles className="w-3 h-3" />
              <span>{task.aiSuggestions.length} AI suggestion{task.aiSuggestions.length !== 1 ? 's' : ''}</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  )

  if (isDragging) {
    return cardContent
  }

  return (
    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
      {cardContent}
    </div>
  )
}

interface AISuggestionPanelProps {
  suggestions: AISuggestion[]
  onAccept: (suggestionId: string) => void
  onDismiss: (suggestionId: string) => void
}

function AISuggestionPanel({ suggestions, onAccept, onDismiss }: AISuggestionPanelProps) {
  if (suggestions.length === 0) return null

  return (
    <motion.div
      initial={{ opacity: 0, x: 300 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 300 }}
      className="absolute right-4 top-4 w-80 z-50"
    >
      <Card variant="glass" className="border-2 border-purple-500/30">
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-sm">
            <Brain className="w-4 h-4 text-purple-500" />
            AI Suggestions ({suggestions.length})
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 max-h-60 overflow-y-auto scrollbar-thin">
            {suggestions.map((suggestion) => (
              <motion.div
                key={suggestion.id}
                layout
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="p-3 rounded-lg bg-purple-50/80 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800"
              >
                <div className="space-y-2">
                  <div className="flex items-start justify-between gap-2">
                    <h4 className="text-xs font-medium text-purple-800 dark:text-purple-200">
                      {suggestion.title}
                    </h4>
                    <div className="flex items-center gap-1">
                      <span className="text-xs px-1.5 py-0.5 rounded bg-purple-100 dark:bg-purple-800 text-purple-700 dark:text-purple-300">
                        {Math.round(suggestion.confidence * 100)}%
                      </span>
                    </div>
                  </div>
                  
                  <p className="text-xs text-purple-700 dark:text-purple-300">
                    {suggestion.description}
                  </p>
                  
                  <div className="flex items-center justify-between pt-2">
                    <span className={cn(
                      'text-xs px-2 py-1 rounded-full font-medium',
                      suggestion.impact === 'high' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                      suggestion.impact === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                      'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    )}>
                      {suggestion.impact} impact
                    </span>
                    
                    <div className="flex gap-2">
                      <Button
                        size="sm"
                        variant="ghost"
                        onClick={() => onDismiss(suggestion.id)}
                        className="h-6 px-2 text-xs"
                      >
                        Dismiss
                      </Button>
                      <Button
                        size="sm"
                        variant="gradient"
                        onClick={() => onAccept(suggestion.id)}
                        className="h-6 px-2 text-xs"
                      >
                        Accept
                      </Button>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

interface ResourceHeatmapProps {
  users: User[]
}

function ResourceHeatmap({ users }: ResourceHeatmapProps) {
  return (
    <Card variant="elevated" className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2 text-sm">
          <Users className="w-4 h-4" />
          Team Resource Heatmap
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {users.map((user) => (
            <motion.div
              key={user.id}
              whileHover={{ scale: 1.05 }}
              className="relative"
            >
              <div className={cn(
                'p-3 rounded-xl border-2 transition-all duration-200',
                user.workload === 'overloaded' ? 'bg-red-50 border-red-200 dark:bg-red-900/20 dark:border-red-800' :
                user.workload === 'heavy' ? 'bg-orange-50 border-orange-200 dark:bg-orange-900/20 dark:border-orange-800' :
                user.workload === 'medium' ? 'bg-yellow-50 border-yellow-200 dark:bg-yellow-900/20 dark:border-yellow-800' :
                'bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-800'
              )}>
                <div className="flex flex-col items-center gap-2">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-blue-400 to-purple-400 flex items-center justify-center text-xs font-semibold text-white">
                    {user.name.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div className="text-center">
                    <p className="text-xs font-medium truncate">{user.name}</p>
                    <p className="text-xs text-muted-foreground">{user.role}</p>
                  </div>
                  
                  <div className="flex items-center gap-1">
                    <span className="text-sm">
                      {user.mood === 'happy' ? '😊' :
                       user.mood === 'neutral' ? '😐' :
                       user.mood === 'stressed' ? '😰' : '🚫'}
                    </span>
                    <span className={cn(
                      'text-xs px-1.5 py-0.5 rounded-full font-medium',
                      user.workload === 'overloaded' ? 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200' :
                      user.workload === 'heavy' ? 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200' :
                      user.workload === 'medium' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200' :
                      'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    )}>
                      {user.workload}
                    </span>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}

export default function SprintKickoffCanvas() {
  const { 
    currentSprint, 
    tasks, 
    users, 
    aiSuggestions, 
    moveTask, 
    acceptAISuggestion, 
    dismissAISuggestion 
  } = useDashboardStore()
  
  const [activeId, setActiveId] = useState<string | null>(null)
  const [showAISuggestions, setShowAISuggestions] = useState(true)
  
  const sensors = useSensors(
    useSensor(PointerSensor, {
      activationConstraint: {
        distance: 8,
      },
    }),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  )

  const handleDragStart = useCallback((event: DragStartEvent) => {
    setActiveId(event.active.id as string)
  }, [])

  const handleDragEnd = useCallback((event: DragEndEvent) => {
    const { active, over } = event
    
    if (!over) {
      setActiveId(null)
      return
    }

    const activeTask = tasks.find(task => task.id === active.id)
    const overColumnId = over.id as string
    
    if (activeTask && ['todo', 'in-progress', 'review', 'done'].includes(overColumnId)) {
      moveTask(activeTask.id, overColumnId as Task['status'])
    }
    
    setActiveId(null)
  }, [tasks, moveTask])

  const activeTask = tasks.find(task => task.id === activeId)

  const columns = [
    { id: 'todo', title: '📋 To Do', tasks: tasks.filter(task => task.status === 'todo') },
    { id: 'in-progress', title: '⚡ In Progress', tasks: tasks.filter(task => task.status === 'in-progress') },
    { id: 'review', title: '👀 Review', tasks: tasks.filter(task => task.status === 'review') },
    { id: 'done', title: '✅ Done', tasks: tasks.filter(task => task.status === 'done') }
  ]

  return (
    <div className="relative h-full w-full overflow-hidden bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-purple-900/20">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-30">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(circle at 1px 1px, rgba(59, 130, 246, 0.15) 1px, transparent 0)`,
          backgroundSize: '20px 20px'
        }} />
      </div>

      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        className="relative z-10 p-6 border-b bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm"
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gradient">
              Sprint Kickoff Canvas
            </h1>
            {currentSprint && (
              <p className="text-sm text-muted-foreground mt-1">
                {currentSprint.name} • {currentSprint.goal}
              </p>
            )}
          </div>
          
          <div className="flex items-center gap-4">
            <Button
              variant="ai"
              size="sm"
              onClick={() => setShowAISuggestions(!showAISuggestions)}
              icon={<Brain className="w-4 h-4" />}
            >
              AI Assistant ({aiSuggestions.length})
            </Button>
            
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Target className="w-4 h-4" />
              <span>{tasks.reduce((sum, task) => sum + (task.storyPoints || 0), 0)} points</span>
            </div>
            
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Clock className="w-4 h-4" />
              <span>{Math.ceil((currentSprint?.endDate.getTime() || Date.now() - Date.now()) / (1000 * 60 * 60 * 24))} days left</span>
            </div>
          </div>
        </div>
      </motion.div>

      <div className="relative flex-1 p-6 overflow-auto">
        <div className="space-y-6">
          {/* Resource Heatmap */}
          <motion.div
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <ResourceHeatmap users={users} />
          </motion.div>

          {/* Kanban Board */}
          <DndContext
            sensors={sensors}
            collisionDetection={closestCenter}
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
          >
            <motion.div
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
            >
              {columns.map((column) => (
                <div key={column.id} className="space-y-4">
                  <div className="flex items-center justify-between">
                    <h3 className="font-semibold text-sm flex items-center gap-2">
                      {column.title}
                      <span className="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-800 rounded-full">
                        {column.tasks.length}
                      </span>
                    </h3>
                    <Button size="icon-sm" variant="ghost">
                      <Plus className="w-4 h-4" />
                    </Button>
                  </div>
                  
                  <SortableContext
                    items={column.tasks.map(task => task.id)}
                    strategy={verticalListSortingStrategy}
                  >
                    <div className="space-y-3 min-h-[200px] p-2 rounded-lg border-2 border-dashed border-gray-200 dark:border-gray-700">
                      {column.tasks.map((task) => (
                        <TaskCard key={task.id} task={task} />
                      ))}
                    </div>
                  </SortableContext>
                </div>
              ))}
            </motion.div>

            <DragOverlay>
              {activeTask ? <TaskCard task={activeTask} isDragging /> : null}
            </DragOverlay>
          </DndContext>
        </div>
      </div>

      {/* AI Suggestions Panel */}
      <AnimatePresence>
        {showAISuggestions && aiSuggestions.length > 0 && (
          <AISuggestionPanel
            suggestions={aiSuggestions}
            onAccept={acceptAISuggestion}
            onDismiss={dismissAISuggestion}
          />
        )}
      </AnimatePresence>
    </div>
  )
}