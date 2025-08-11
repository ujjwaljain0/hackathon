'use client'

import { useEffect, useRef } from 'react'
import { useQueryClient } from '@tanstack/react-query'
import { useDashboardStore } from '@/stores/dashboard'
import { apiClient, queryKeys } from '@/lib/api'

export function useRealtimeUpdates() {
  const queryClient = useQueryClient()
  const addRealtimeUpdate = useDashboardStore(state => state.addRealtimeUpdate)
  const unsubscribeRef = useRef<(() => void) | null>(null)

  useEffect(() => {
    // Subscribe to real-time updates
    const unsubscribe = apiClient.subscribeToUpdates((update) => {
      console.log('Real-time update received:', update)

      // Update Zustand store
      addRealtimeUpdate(update.data)

      // Invalidate relevant React Query caches
      switch (update.type) {
        case 'task_updated':
          queryClient.invalidateQueries({ queryKey: queryKeys.tasks() })
          queryClient.invalidateQueries({ queryKey: queryKeys.currentSprint() })
          break

        case 'new_ai_suggestion':
          queryClient.invalidateQueries({ queryKey: queryKeys.aiSuggestions() })
          break

        case 'new_notification':
          queryClient.invalidateQueries({ queryKey: queryKeys.notifications() })
          break

        case 'sprint_updated':
          queryClient.invalidateQueries({ queryKey: queryKeys.currentSprint() })
          queryClient.invalidateQueries({ queryKey: queryKeys.sprints() })
          break

        case 'team_metrics_updated':
          queryClient.invalidateQueries({ queryKey: queryKeys.teamMetrics() })
          break

        default:
          // Invalidate all queries for unknown update types
          queryClient.invalidateQueries()
      }
    })

    unsubscribeRef.current = unsubscribe

    return () => {
      if (unsubscribeRef.current) {
        unsubscribeRef.current()
      }
    }
  }, [queryClient, addRealtimeUpdate])

  // Return the unsubscribe function in case components need manual control
  return {
    disconnect: () => {
      if (unsubscribeRef.current) {
        unsubscribeRef.current()
        unsubscribeRef.current = null
      }
    }
  }
}