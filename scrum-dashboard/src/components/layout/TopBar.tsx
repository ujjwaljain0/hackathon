'use client'

import React from 'react'
import { motion } from 'framer-motion'
import { Button } from '@/components/ui/Button'
import { Avatar } from '@/components/ui/Avatar'
import { Badge } from '@/components/ui/Badge'
import { cn } from '@/lib/utils'
import {
  Bell,
  Search,
  Sun,
  Moon,
  Settings,
  HelpCircle,
  ChevronDown,
  Command,
  Zap,
  Calendar,
  Clock
} from 'lucide-react'
import { useTheme } from 'next-themes'

interface TopBarProps {
  className?: string
}

const notifications = [
  { id: '1', type: 'task', message: 'Task "API Integration" completed', time: '2m ago', unread: true },
  { id: '2', type: 'mention', message: 'You were mentioned in "Sprint Review"', time: '5m ago', unread: true },
  { id: '3', type: 'system', message: 'Sprint 23 starts in 2 hours', time: '1h ago', unread: false }
]

export default function TopBar({ className }: TopBarProps) {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = React.useState(false)

  React.useEffect(() => {
    setMounted(true)
  }, [])

  const unreadCount = notifications.filter(n => n.unread).length

  if (!mounted) {
    return null
  }

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className={cn(
        'sticky top-0 z-40 w-full border-b border-border bg-background/80 backdrop-blur-sm',
        className
      )}
    >
      <div className="flex h-16 items-center justify-between px-6">
        {/* Left Section - Breadcrumb & Search */}
        <div className="flex items-center gap-4 flex-1">
          {/* Breadcrumb */}
          <div className="hidden md:flex items-center gap-2 text-sm">
            <span className="text-muted-foreground">Dashboard</span>
            <span className="text-muted-foreground">/</span>
            <span className="text-foreground font-medium">Sprint Canvas</span>
          </div>

          {/* Global Search */}
          <div className="relative w-full max-w-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-muted-foreground" />
            </div>
            <input
              type="search"
              placeholder="Search tasks, people, or sprints..."
              className="block w-full pl-10 pr-3 py-2 border border-border rounded-lg bg-background placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-sm"
            />
            <div className="absolute inset-y-0 right-0 pr-3 flex items-center">
              <kbd className="hidden sm:inline-flex h-5 select-none items-center gap-1 rounded border border-border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100">
                <Command className="h-2.5 w-2.5" />K
              </kbd>
            </div>
          </div>
        </div>

        {/* Right Section - Actions & Profile */}
        <div className="flex items-center gap-2">
          {/* Current Sprint Info */}
          <div className="hidden lg:flex items-center gap-3 px-3 py-1.5 rounded-lg bg-muted">
            <Calendar className="w-4 h-4 text-primary" />
            <div className="text-sm">
              <span className="font-medium text-foreground">Sprint 23</span>
              <div className="flex items-center gap-2 text-xs text-muted-foreground">
                <Clock className="w-3 h-3" />
                <span>5 days left</span>
              </div>
            </div>
          </div>

          {/* AI Assistant */}
          <Button variant="ghost" size="sm" className="gap-2">
            <Zap className="w-4 h-4 text-primary" />
            <span className="hidden sm:inline">AI Assistant</span>
          </Button>

          {/* Notifications */}
          <div className="relative">
            <Button variant="ghost" size="icon">
              <Bell className="w-4 h-4" />
              {unreadCount > 0 && (
                <Badge variant="destructive" className="absolute -top-1 -right-1 w-5 h-5 text-xs flex items-center justify-center p-0">
                  {unreadCount}
                </Badge>
              )}
            </Button>
          </div>

          {/* Theme Toggle */}
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          >
            {theme === 'dark' ? (
              <Sun className="w-4 h-4" />
            ) : (
              <Moon className="w-4 h-4" />
            )}
          </Button>

          {/* Help */}
          <Button variant="ghost" size="icon">
            <HelpCircle className="w-4 h-4" />
          </Button>

          {/* Settings */}
          <Button variant="ghost" size="icon">
            <Settings className="w-4 h-4" />
          </Button>

          {/* User Menu */}
          <div className="flex items-center gap-2 pl-2">
            <div className="hidden sm:block text-right">
              <p className="text-sm font-medium text-foreground">Alex Johnson</p>
              <p className="text-xs text-muted-foreground">Scrum Master</p>
            </div>
            <Button variant="ghost" className="gap-2 px-2">
              <Avatar size="sm" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face" alt="User" />
              <ChevronDown className="w-3 h-3" />
            </Button>
          </div>
        </div>
      </div>

      {/* Quick Stats Bar */}
      <div className="border-t border-border bg-muted/50 px-6 py-2">
        <div className="flex items-center justify-between text-xs">
          <div className="flex items-center gap-6">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-500"></div>
              <span className="text-muted-foreground">32 Tasks Completed</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-blue-500"></div>
              <span className="text-muted-foreground">18 In Progress</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-yellow-500"></div>
              <span className="text-muted-foreground">5 Blocked</span>
            </div>
          </div>
          <div className="text-muted-foreground">
            Team Velocity: <span className="font-medium text-foreground">42 pts/sprint</span>
          </div>
        </div>
      </div>
    </motion.header>
  )
}