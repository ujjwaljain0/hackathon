import React from 'react'
import type { Meta, StoryObj } from '@storybook/react'
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../src/components/ui/Card'
import { Button } from '../src/components/ui/Button'
import { Badge } from '../src/components/ui/Badge'

const meta = {
  title: 'UI/Card',
  component: Card,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A flexible card component with various visual variants. Perfect for displaying content in organized, elevated containers with consistent spacing and styling.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'elevated', 'glass', 'gradient', 'neo'],
      description: 'Visual variant of the card',
    },
    size: {
      control: 'select',
      options: ['sm', 'default', 'lg', 'xl'],
      description: 'Padding size of the card',
    },
    interactive: {
      control: 'boolean',
      description: 'Adds hover effects when true',
    },
    loading: {
      control: 'boolean',
      description: 'Shows loading skeleton when true',
    },
  },
} satisfies Meta<typeof Card>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    children: (
      <>
        <CardHeader>
          <CardTitle>Card Title</CardTitle>
          <CardDescription>Card description goes here</CardDescription>
        </CardHeader>
        <CardContent>
          <p>This is the main content of the card. You can put any content here.</p>
        </CardContent>
      </>
    ),
  },
}

export const Elevated: Story = {
  args: {
    variant: 'elevated',
    children: (
      <>
        <CardHeader>
          <CardTitle>Elevated Card</CardTitle>
          <CardDescription>This card has enhanced shadow effects</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Perfect for highlighting important content or creating visual hierarchy.</p>
        </CardContent>
      </>
    ),
  },
}

export const Glass: Story = {
  args: {
    variant: 'glass',
    children: (
      <>
        <CardHeader>
          <CardTitle>Glass Card</CardTitle>
          <CardDescription>Glassmorphism design with backdrop blur</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Modern translucent effect that works great on gradient backgrounds.</p>
        </CardContent>
      </>
    ),
  },
  parameters: {
    backgrounds: { default: 'gradient' },
  },
}

export const Gradient: Story = {
  args: {
    variant: 'gradient',
    children: (
      <>
        <CardHeader>
          <CardTitle>Gradient Card</CardTitle>
          <CardDescription>Subtle gradient background</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Elegant gradient background that adapts to light and dark themes.</p>
        </CardContent>
      </>
    ),
  },
}

export const Neo: Story = {
  args: {
    variant: 'neo',
    children: (
      <>
        <CardHeader>
          <CardTitle>Neumorphic Card</CardTitle>
          <CardDescription>Modern neumorphic design</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Soft, tactile appearance with subtle shadows and highlights.</p>
        </CardContent>
      </>
    ),
  },
}

export const Interactive: Story = {
  args: {
    variant: 'elevated',
    interactive: true,
    children: (
      <>
        <CardHeader>
          <CardTitle>Interactive Card</CardTitle>
          <CardDescription>Hover over this card to see the effect</CardDescription>
        </CardHeader>
        <CardContent>
          <p>This card responds to hover with smooth animations and transform effects.</p>
        </CardContent>
      </>
    ),
  },
}

export const WithFooter: Story = {
  args: {
    children: (
      <>
        <CardHeader>
          <CardTitle>Task Card</CardTitle>
          <CardDescription>Implement user authentication</CardDescription>
        </CardHeader>
        <CardContent>
          <p>Create secure login/logout functionality with JWT tokens and password reset capability.</p>
          <div className="flex gap-2 mt-4">
            <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">Backend</span>
            <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">Security</span>
          </div>
        </CardContent>
        <CardFooter>
          <Button variant="outline" size="sm">Edit</Button>
          <Button size="sm">Complete</Button>
        </CardFooter>
      </>
    ),
  },
}

export const SmallSize: Story = {
  args: {
    size: 'sm',
    children: (
      <>
        <CardHeader>
          <CardTitle>Small Card</CardTitle>
        </CardHeader>
        <CardContent>
          <p>Compact card with reduced padding.</p>
        </CardContent>
      </>
    ),
  },
}

export const LargeSize: Story = {
  args: {
    size: 'lg',
    children: (
      <>
        <CardHeader>
          <CardTitle>Large Card</CardTitle>
          <CardDescription>More spacious layout</CardDescription>
        </CardHeader>
        <CardContent>
          <p>This card has generous padding for better readability and visual comfort.</p>
        </CardContent>
      </>
    ),
  },
}

export const Loading: Story = {
  args: {
    loading: true,
  },
}