import type { Meta, StoryObj } from '@storybook/react'
import SprintKickoffCanvas from '../src/components/canvas/SprintKickoffCanvas'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useDashboardStore } from '../src/stores/dashboard'
import { useEffect } from 'react'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false, staleTime: Infinity },
    mutations: { retry: false },
  },
})

// Story decorator to provide necessary context
const withProviders = (Story: any) => {
  const StoryWithData = () => {
    const loadInitialData = useDashboardStore(state => state.loadInitialData)
    
    useEffect(() => {
      loadInitialData()
    }, [loadInitialData])

    return <Story />
  }

  return (
    <QueryClientProvider client={queryClient}>
      <div className="h-screen w-full">
        <StoryWithData />
      </div>
    </QueryClientProvider>
  )
}

const meta = {
  title: 'Components/SprintKickoffCanvas',
  component: SprintKickoffCanvas,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'An interactive Sprint Kickoff Canvas with drag-and-drop functionality, AI suggestions, and team resource heatmap. Features a beautiful gradient background with animated elements.',
      },
    },
  },
  tags: ['autodocs'],
  decorators: [withProviders],
} satisfies Meta<typeof SprintKickoffCanvas>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}

export const WithAISuggestions: Story = {
  parameters: {
    docs: {
      description: {
        story: 'Shows the canvas with AI suggestions panel open, demonstrating smart recommendations for task creation, priority adjustments, and resource allocation.',
      },
    },
  },
}

export const DarkMode: Story = {
  parameters: {
    backgrounds: { default: 'dark' },
    docs: {
      description: {
        story: 'The canvas in dark mode, showcasing the adaptive design and glassmorphism effects.',
      },
    },
  },
}

export const MobileView: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
    docs: {
      description: {
        story: 'Responsive design for mobile devices with stacked columns and touch-friendly interactions.',
      },
    },
  },
}