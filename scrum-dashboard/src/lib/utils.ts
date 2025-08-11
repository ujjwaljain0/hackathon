import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(date)
}

export function formatRelativeTime(date: Date): string {
  const now = new Date()
  const diffInSeconds = Math.floor((now.getTime() - date.getTime()) / 1000)
  
  if (diffInSeconds < 60) return 'just now'
  if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)}m ago`
  if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)}h ago`
  if (diffInSeconds < 604800) return `${Math.floor(diffInSeconds / 86400)}d ago`
  
  return formatDate(date)
}

export function generateId(): string {
  return Math.random().toString(36).substring(2) + Date.now().toString(36)
}

export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout | null = null
  
  return (...args: Parameters<T>) => {
    if (timeout) clearTimeout(timeout)
    timeout = setTimeout(() => func(...args), wait)
  }
}

export function throttle<T extends (...args: any[]) => any>(
  func: T,
  limit: number
): (...args: Parameters<T>) => void {
  let inThrottle: boolean
  
  return (...args: Parameters<T>) => {
    if (!inThrottle) {
      func(...args)
      inThrottle = true
      setTimeout(() => inThrottle = false, limit)
    }
  }
}

export function getStatusColor(status: string): string {
  const statusMap: Record<string, string> = {
    'todo': 'bg-gray-100 text-gray-800 border-gray-200',
    'in-progress': 'bg-blue-100 text-blue-800 border-blue-200',
    'review': 'bg-yellow-100 text-yellow-800 border-yellow-200',
    'done': 'bg-green-100 text-green-800 border-green-200',
    'blocked': 'bg-red-100 text-red-800 border-red-200',
    'low': 'bg-green-100 text-green-800 border-green-200',
    'medium': 'bg-yellow-100 text-yellow-800 border-yellow-200',
    'high': 'bg-orange-100 text-orange-800 border-orange-200',
    'critical': 'bg-red-100 text-red-800 border-red-200',
  }
  
  return statusMap[status.toLowerCase()] || 'bg-gray-100 text-gray-800 border-gray-200'
}

export function getPriorityIcon(priority: string): string {
  const priorityMap: Record<string, string> = {
    'low': '⬇',
    'medium': '➡',
    'high': '⬆',
    'critical': '🔥',
  }
  
  return priorityMap[priority.toLowerCase()] || '➡'
}

export function calculateVelocity(completedPoints: number[], sprintDays: number = 14): number {
  if (completedPoints.length === 0) return 0
  const totalPoints = completedPoints.reduce((sum, points) => sum + points, 0)
  return Math.round((totalPoints / completedPoints.length) * 10) / 10
}

export function predictDeliveryDate(remainingPoints: number, velocity: number): Date | null {
  if (velocity === 0) return null
  
  const sprintsNeeded = Math.ceil(remainingPoints / velocity)
  const daysNeeded = sprintsNeeded * 14 // Assuming 2-week sprints
  
  const deliveryDate = new Date()
  deliveryDate.setDate(deliveryDate.getDate() + daysNeeded)
  
  return deliveryDate
}