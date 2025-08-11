'use client'

import React, { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from '@/components/ui/Button'
import { Avatar } from '@/components/ui/Avatar'
import { Badge } from '@/components/ui/Badge'
import { cn } from '@/lib/utils'
import {
  LayoutDashboard,
  Calendar,
  Users,
  BarChart3,
  Settings,
  Bell,
  Search,
  Menu,
  X,
  ChevronDown,
  Sparkles,
  Target,
  Activity,
  Clock,
  Plus,
  Home,
  FolderKanban,
  MessageSquare,
  FileText
} from 'lucide-react'

interface SidebarProps {
  collapsed?: boolean
  onCollapsedChange?: (collapsed: boolean) => void
  currentView: string
  onViewChange: (view: string) => void
}

const navigationItems = [
  {
    id: 'overview',
    label: 'Overview',
    icon: Home,
    badge: null,
    submenu: []
  },
  {
    id: 'canvas',
    label: 'Sprint Canvas',
    icon: FolderKanban,
    badge: 'AI',
    submenu: []
  },
  {
    id: 'pulse',
    label: 'Daily Pulse',
    icon: Activity,
    badge: 'Live',
    submenu: []
  },
  {
    id: 'analytics',
    label: 'Analytics',
    icon: BarChart3,
    badge: null,
    submenu: [
      { id: 'velocity', label: 'Velocity', icon: Target },
      { id: 'burndown', label: 'Burndown', icon: Clock },
      { id: 'reports', label: 'Reports', icon: FileText }
    ]
  },
  {
    id: 'team',
    label: 'Team',
    icon: Users,
    badge: '12',
    submenu: []
  },
  {
    id: 'calendar',
    label: 'Calendar',
    icon: Calendar,
    badge: null,
    submenu: []
  },
  {
    id: 'messages',
    label: 'Messages',
    icon: MessageSquare,
    badge: '3',
    submenu: []
  }
]

const quickActions = [
  { id: 'new-sprint', label: 'New Sprint', icon: Plus },
  { id: 'add-task', label: 'Add Task', icon: Target },
  { id: 'schedule-meeting', label: 'Schedule Meeting', icon: Calendar }
]

export default function Sidebar({ collapsed = false, onCollapsedChange, currentView, onViewChange }: SidebarProps) {
  const [expandedItems, setExpandedItems] = useState<string[]>(['analytics'])

  const toggleExpanded = (itemId: string) => {
    setExpandedItems(prev => 
      prev.includes(itemId) 
        ? prev.filter(id => id !== itemId)
        : [...prev, itemId]
    )
  }

  return (
    <motion.div
      initial={false}
      animate={{ width: collapsed ? 80 : 280 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="relative flex flex-col h-full bg-card border-r border-border shadow-elegant flex-shrink-0"
    >
      {/* Header */}
      <div className="flex items-center justify-between p-6 border-b border-border">
        <AnimatePresence mode="wait">
          {!collapsed && (
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="flex items-center gap-3"
            >
              <div className="w-8 h-8 rounded-lg gradient-primary flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <div>
                <h2 className="text-sm font-semibold text-foreground">AI Scrum</h2>
                <p className="text-xs text-muted-foreground">Dashboard</p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        
        <Button
          variant="ghost"
          size="icon-sm"
          onClick={() => onCollapsedChange?.(!collapsed)}
          className="ml-auto"
        >
          {collapsed ? <Menu className="w-4 h-4" /> : <X className="w-4 h-4" />}
        </Button>
      </div>

      {/* Search */}
      {!collapsed && (
        <div className="p-4 border-b border-border">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search..."
              className="w-full pl-10 pr-4 py-2 text-sm bg-muted rounded-lg border border-border focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>
        </div>
      )}

      {/* Navigation */}
      <div className="flex-1 p-4 space-y-2 overflow-y-auto scrollbar-thin">
        <div>
          {!collapsed && (
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
              Navigation
            </p>
          )}
          
          <nav className="space-y-1">
            {navigationItems.map((item) => (
              <div key={item.id}>
                <Button
                  variant={currentView === item.id ? 'secondary' : 'ghost'}
                  size="sm"
                  onClick={() => {
                    onViewChange(item.id)
                    if (item.submenu.length > 0) {
                      toggleExpanded(item.id)
                    }
                  }}
                  className={cn(
                    'w-full justify-start gap-3 text-left font-normal',
                    currentView === item.id && 'bg-primary text-primary-foreground hover:bg-primary hover:text-primary-foreground',
                    collapsed && 'justify-center px-0'
                  )}
                >
                  <item.icon className="w-4 h-4 flex-shrink-0" />
                  {!collapsed && (
                    <>
                      <span className="flex-1">{item.label}</span>
                      {item.badge && (
                        <Badge variant="secondary" className="text-xs">
                          {item.badge}
                        </Badge>
                      )}
                      {item.submenu.length > 0 && (
                        <ChevronDown 
                          className={cn(
                            'w-4 h-4 transition-transform',
                            expandedItems.includes(item.id) && 'rotate-180'
                          )} 
                        />
                      )}
                    </>
                  )}
                </Button>

                {/* Submenu */}
                <AnimatePresence>
                  {!collapsed && item.submenu.length > 0 && expandedItems.includes(item.id) && (
                    <motion.div
                      initial={{ opacity: 0, height: 0 }}
                      animate={{ opacity: 1, height: 'auto' }}
                      exit={{ opacity: 0, height: 0 }}
                      className="ml-4 mt-1 space-y-1 overflow-hidden"
                    >
                      {item.submenu.map((subitem) => (
                        <Button
                          key={subitem.id}
                          variant="ghost"
                          size="sm"
                          onClick={() => onViewChange(subitem.id)}
                          className={cn(
                            'w-full justify-start gap-3 text-left font-normal text-muted-foreground',
                            currentView === subitem.id && 'bg-accent text-accent-foreground'
                          )}
                        >
                          <subitem.icon className="w-3 h-3" />
                          <span>{subitem.label}</span>
                        </Button>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
          </nav>
        </div>

        {/* Quick Actions */}
        {!collapsed && (
          <div className="pt-6">
            <p className="text-xs font-medium text-muted-foreground uppercase tracking-wide mb-2">
              Quick Actions
            </p>
            <div className="space-y-1">
              {quickActions.map((action) => (
                <Button
                  key={action.id}
                  variant="ghost"
                  size="sm"
                  className="w-full justify-start gap-3 text-left font-normal text-muted-foreground hover:text-foreground"
                >
                  <action.icon className="w-4 h-4" />
                  <span>{action.label}</span>
                </Button>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* User Profile */}
      <div className="p-4 border-t border-border">
        {collapsed ? (
          <div className="flex justify-center">
            <Avatar size="sm" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face" alt="User" />
          </div>
        ) : (
          <div className="flex items-center gap-3">
            <Avatar size="sm" src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=150&h=150&fit=crop&crop=face" alt="User" />
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-foreground truncate">Alex Johnson</p>
              <p className="text-xs text-muted-foreground truncate">Scrum Master</p>
            </div>
            <Button variant="ghost" size="icon-sm">
              <Settings className="w-4 h-4" />
            </Button>
          </div>
        )}
      </div>
    </motion.div>
  )
}