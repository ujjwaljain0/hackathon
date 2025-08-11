'use client'

import React, { useEffect, useMemo, useState } from 'react'
import { LoadingSpinner } from '@/components/ui/LoadingSpinner'
import Sidebar from '@/components/layout/Sidebar'
import TopBar from '@/components/layout/TopBar'
import OverviewDashboard from '@/components/dashboard/OverviewDashboard'
import SprintKickoffCanvas from '@/components/canvas/SprintKickoffCanvas'
import DailyPulseView from '@/components/pulse/DailyPulseView'
import AnalyticsDashboard from '@/components/analytics/AnalyticsDashboard'
import { useDashboardStore } from '@/stores/dashboard'
import { useRealtimeUpdates } from '@/hooks/useRealtimeUpdates'

export default function Dashboard() {
  const { loadInitialData, isLoading } = useDashboardStore()

  // Local UI state
  const [isSidebarCollapsed, setIsSidebarCollapsed] = useState(false)
  const [currentView, setCurrentView] = useState<string>('overview')

  // Set up real-time updates
  useRealtimeUpdates()

  useEffect(() => {
    loadInitialData()
  }, [loadInitialData])

  const content = useMemo(() => {
    if (isLoading) {
      return (
        <div className="flex items-center justify-center h-[calc(100vh-8rem)]">
          <LoadingSpinner />
        </div>
      )
    }

    switch (currentView) {
      case 'overview':
        return <OverviewDashboard />
      case 'canvas':
        return <SprintKickoffCanvas />
      case 'pulse':
        return <DailyPulseView />
      case 'analytics':
      case 'velocity':
      case 'burndown':
      case 'reports':
        return <AnalyticsDashboard />
      case 'team':
        return (
          <div className="p-8">
            <h1 className="text-2xl font-bold mb-4">Team Directory</h1>
            <p className="text-muted-foreground">Team management features coming soon...</p>
          </div>
        )
      case 'calendar':
        return (
          <div className="p-8">
            <h1 className="text-2xl font-bold mb-4">Calendar</h1>
            <p className="text-muted-foreground">Calendar view coming soon...</p>
          </div>
        )
      case 'messages':
        return (
          <div className="p-8">
            <h1 className="text-2xl font-bold mb-4">Messages</h1>
            <p className="text-muted-foreground">Team messaging coming soon...</p>
          </div>
        )
      default:
        return (
          <div className="p-8">
            <h1 className="text-2xl font-bold mb-4">Under Construction</h1>
            <p className="text-muted-foreground">This section is being built...</p>
          </div>
        )
    }
  }, [currentView, isLoading])

  return (
    <div className="min-h-screen bg-background text-foreground flex">
      {/* Sidebar */}
      <Sidebar
        collapsed={isSidebarCollapsed}
        onCollapsedChange={setIsSidebarCollapsed}
        currentView={currentView}
        onViewChange={setCurrentView}
      />

      {/* Main area */}
      <div className="flex-1 flex flex-col min-w-0 w-full">
        {/* Top bar */}
        <TopBar />

        {/* Content */}
        <main className="flex-1 overflow-auto bg-background">
          {content}
        </main>
      </div>
    </div>
  )
}