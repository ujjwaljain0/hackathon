import type { Meta, StoryObj } from '@storybook/react'
import DailyPulseView from '../src/components/pulse/DailyPulseView'
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
      <div className="min-h-screen w-full bg-background">
        <StoryWithData />
      </div>
    </QueryClientProvider>
  )
}

const meta = {
  title: 'Components/DailyPulseView',
  component: DailyPulseView,
  parameters: {
    layout: 'fullscreen',
    docs: {
      description: {
        component: 'A real-time dashboard showing team pulse metrics, live activity feed, and key performance indicators. Features animated metrics cards and a timeline of recent events.',
      },
    },
  },
  tags: ['autodocs'],
  decorators: [withProviders],
} satisfies Meta<typeof DailyPulseView>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {}

export const WithHighActivity: Story = {
  parameters: {
    docs: {
      description: {
        story: 'Shows the pulse view with high team activity, multiple timeline events, and dynamic metrics updates.',
      },
    },
  },
}

export const DarkMode: Story = {
  parameters: {
    backgrounds: { default: 'dark' },
    docs: {
      description: {
        story: 'The pulse view in dark mode, highlighting the elegant contrast and readability.',
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
        story: 'Responsive design optimized for mobile devices with stacked metrics and touch-friendly timeline.',
      },
    },
  },
}

export const TabletView: Story = {
  parameters: {
    viewport: {
      defaultViewport: 'tablet',
    },
    docs: {
      description: {
        story: 'Tablet-optimized layout with balanced spacing and readable metrics grid.',
      },
    },
  },
}