'use client'

import React, { useEffect, useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Button } from '@/components/ui/Button'
import { cn } from '@/lib/utils'
import { 
  Volume2, 
  VolumeX, 
  Eye, 
  EyeOff,
  Type,
  Zap,
  Settings,
  X
} from 'lucide-react'

interface AccessibilityState {
  announcements: boolean
  reducedMotion: boolean
  highContrast: boolean
  largeText: boolean
  keyboardNavigation: boolean
}

const AccessibilityPanel = ({ 
  isOpen, 
  onClose 
}: { 
  isOpen: boolean
  onClose: () => void 
}) => {
  const [settings, setSettings] = useState<AccessibilityState>({
    announcements: true,
    reducedMotion: false,
    highContrast: false,
    largeText: false,
    keyboardNavigation: true
  })

  const updateSetting = (key: keyof AccessibilityState, value: boolean) => {
    setSettings(prev => ({ ...prev, [key]: value }))
    
    // Apply changes to document
    const root = document.documentElement
    
    switch (key) {
      case 'reducedMotion':
        root.style.setProperty('--motion-duration', value ? '0s' : '0.3s')
        if (value) {
          root.classList.add('reduce-motion')
        } else {
          root.classList.remove('reduce-motion')
        }
        break
        
      case 'highContrast':
        if (value) {
          root.classList.add('high-contrast')
        } else {
          root.classList.remove('high-contrast')
        }
        break
        
      case 'largeText':
        if (value) {
          root.classList.add('large-text')
        } else {
          root.classList.remove('large-text')
        }
        break
    }
    
    // Store in localStorage
    localStorage.setItem('accessibility-settings', JSON.stringify({ ...settings, [key]: value }))
  }

  useEffect(() => {
    // Load settings from localStorage
    const saved = localStorage.getItem('accessibility-settings')
    if (saved) {
      try {
        const parsed = JSON.parse(saved)
        setSettings(parsed)
        
        // Apply saved settings
        Object.entries(parsed).forEach(([key, value]) => {
          if (typeof value === 'boolean') {
            updateSetting(key as keyof AccessibilityState, value)
          }
        })
      } catch (e) {
        console.error('Failed to parse accessibility settings:', e)
      }
    }
  }, [])

  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4"
          onClick={onClose}
        >
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            className="bg-white dark:bg-gray-900 rounded-2xl p-6 max-w-md w-full shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-semibold flex items-center gap-2">
                <Settings className="w-5 h-5" />
                Accessibility Settings
              </h2>
              <Button
                variant="ghost"
                size="icon-sm"
                onClick={onClose}
                aria-label="Close accessibility settings"
              >
                <X className="w-4 h-4" />
              </Button>
            </div>

            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {settings.announcements ? <Volume2 className="w-4 h-4" /> : <VolumeX className="w-4 h-4" />}
                  <div>
                    <h3 className="font-medium">Screen Reader Announcements</h3>
                    <p className="text-sm text-muted-foreground">Enable status announcements</p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => updateSetting('announcements', !settings.announcements)}
                  className={cn(
                    'w-12 h-6 rounded-full relative transition-colors',
                    settings.announcements ? 'bg-primary-500' : 'bg-gray-300 dark:bg-gray-600'
                  )}
                >
                  <div
                    className={cn(
                      'w-4 h-4 bg-white rounded-full absolute transition-transform',
                      settings.announcements ? 'transform translate-x-6' : 'transform translate-x-1'
                    )}
                  />
                </Button>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Zap className="w-4 h-4" />
                  <div>
                    <h3 className="font-medium">Reduced Motion</h3>
                    <p className="text-sm text-muted-foreground">Minimize animations and transitions</p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => updateSetting('reducedMotion', !settings.reducedMotion)}
                  className={cn(
                    'w-12 h-6 rounded-full relative transition-colors',
                    settings.reducedMotion ? 'bg-primary-500' : 'bg-gray-300 dark:bg-gray-600'
                  )}
                >
                  <div
                    className={cn(
                      'w-4 h-4 bg-white rounded-full absolute transition-transform',
                      settings.reducedMotion ? 'transform translate-x-6' : 'transform translate-x-1'
                    )}
                  />
                </Button>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  {settings.highContrast ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                  <div>
                    <h3 className="font-medium">High Contrast</h3>
                    <p className="text-sm text-muted-foreground">Increase color contrast for better visibility</p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => updateSetting('highContrast', !settings.highContrast)}
                  className={cn(
                    'w-12 h-6 rounded-full relative transition-colors',
                    settings.highContrast ? 'bg-primary-500' : 'bg-gray-300 dark:bg-gray-600'
                  )}
                >
                  <div
                    className={cn(
                      'w-4 h-4 bg-white rounded-full absolute transition-transform',
                      settings.highContrast ? 'transform translate-x-6' : 'transform translate-x-1'
                    )}
                  />
                </Button>
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <Type className="w-4 h-4" />
                  <div>
                    <h3 className="font-medium">Large Text</h3>
                    <p className="text-sm text-muted-foreground">Increase text size throughout the app</p>
                  </div>
                </div>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => updateSetting('largeText', !settings.largeText)}
                  className={cn(
                    'w-12 h-6 rounded-full relative transition-colors',
                    settings.largeText ? 'bg-primary-500' : 'bg-gray-300 dark:bg-gray-600'
                  )}
                >
                  <div
                    className={cn(
                      'w-4 h-4 bg-white rounded-full absolute transition-transform',
                      settings.largeText ? 'transform translate-x-6' : 'transform translate-x-1'
                    )}
                  />
                </Button>
              </div>
            </div>

            <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
              <p className="text-sm text-blue-800 dark:text-blue-200">
                <strong>Tip:</strong> Use Tab to navigate, Space/Enter to activate buttons, and arrow keys to move between options.
              </p>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

// Screen reader announcements component
export const ScreenReaderAnnouncements = () => {
  const [announcement, setAnnouncement] = useState('')

  useEffect(() => {
    // Listen for custom announcement events
    const handleAnnouncement = (event: CustomEvent) => {
      setAnnouncement(event.detail.message)
      
      // Clear after reading
      setTimeout(() => setAnnouncement(''), 100)
    }

    window.addEventListener('announce' as any, handleAnnouncement)
    
    return () => {
      window.removeEventListener('announce' as any, handleAnnouncement)
    }
  }, [])

  return (
    <div
      aria-live="polite"
      aria-atomic="true"
      className="sr-only"
    >
      {announcement}
    </div>
  )
}

// Hook for making announcements
export const useAnnouncement = () => {
  return (message: string) => {
    const settings = JSON.parse(localStorage.getItem('accessibility-settings') || '{}')
    if (settings.announcements !== false) {
      window.dispatchEvent(new CustomEvent('announce', { 
        detail: { message } 
      }))
    }
  }
}

// Focus management hook
export const useFocusManagement = () => {
  const [focusVisible, setFocusVisible] = useState(false)

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Tab') {
        setFocusVisible(true)
      }
    }

    const handleClick = () => {
      setFocusVisible(false)
    }

    document.addEventListener('keydown', handleKeyDown)
    document.addEventListener('click', handleClick)

    return () => {
      document.removeEventListener('keydown', handleKeyDown)
      document.removeEventListener('click', handleClick)
    }
  }, [])

  return focusVisible
}

// Keyboard navigation hook
export const useKeyboardNavigation = (
  items: HTMLElement[],
  isOpen: boolean
) => {
  const [activeIndex, setActiveIndex] = useState(-1)

  useEffect(() => {
    if (!isOpen) return

    const handleKeyDown = (e: KeyboardEvent) => {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault()
          setActiveIndex(prev => 
            prev < items.length - 1 ? prev + 1 : 0
          )
          break
          
        case 'ArrowUp':
          e.preventDefault()
          setActiveIndex(prev => 
            prev > 0 ? prev - 1 : items.length - 1
          )
          break
          
        case 'Home':
          e.preventDefault()
          setActiveIndex(0)
          break
          
        case 'End':
          e.preventDefault()
          setActiveIndex(items.length - 1)
          break
          
        case 'Enter':
        case ' ':
          if (activeIndex >= 0 && items[activeIndex]) {
            e.preventDefault()
            items[activeIndex].click()
          }
          break
      }
    }

    document.addEventListener('keydown', handleKeyDown)
    
    return () => {
      document.removeEventListener('keydown', handleKeyDown)
    }
  }, [items, isOpen, activeIndex])

  // Focus the active item
  useEffect(() => {
    if (activeIndex >= 0 && items[activeIndex]) {
      items[activeIndex].focus()
    }
  }, [activeIndex, items])

  return activeIndex
}

export default AccessibilityPanel