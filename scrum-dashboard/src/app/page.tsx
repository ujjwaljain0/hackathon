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
          <div className="p-8 text-muted-foreground">Team directory coming soon...</div>
        )
      default:
        return (
          <div className="p-8 text-muted-foreground">This section is under construction.</div>
        )
    }
  }, [currentView])

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
      <div className="flex-1 min-w-0 flex flex-col">
        {/* Top bar */}
        <TopBar />

        {/* Content */}
        <main className="flex-1 min-w-0">
          {isLoading ? (
            <div className="flex items-center justify-center h-[calc(100vh-4rem)]">
              <LoadingSpinner />
            </div>
          ) : (
            content
          )}
        </main>
      </div>
    </div>
  )
}