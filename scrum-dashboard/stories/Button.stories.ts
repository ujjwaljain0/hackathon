import React from 'react'
import type { Meta, StoryObj } from '@storybook/react'
import { fn } from '@storybook/test'
import { Button } from '../src/components/ui/Button'
import { Heart, Download, Sparkles } from 'lucide-react'

const meta = {
  title: 'UI/Button',
  component: Button,
  parameters: {
    layout: 'centered',
    docs: {
      description: {
        component: 'A versatile button component with multiple variants, sizes, and states. Built with accessibility in mind and supports icons, loading states, and modern animations.',
      },
    },
  },
  tags: ['autodocs'],
  argTypes: {
    variant: {
      control: 'select',
      options: ['default', 'destructive', 'outline', 'secondary', 'ghost', 'link', 'gradient', 'glass', 'ai'],
      description: 'Visual variant of the button',
    },
    size: {
      control: 'select',
      options: ['default', 'sm', 'lg', 'xl', 'icon', 'icon-sm', 'icon-lg'],
      description: 'Size of the button',
    },
    loading: {
      control: 'boolean',
      description: 'Shows loading spinner when true',
    },
    disabled: {
      control: 'boolean',
      description: 'Disables the button when true',
    },
    asChild: {
      control: 'boolean',
      description: 'Render as a child component (useful for links)',
    },
  },
  args: { onClick: fn() },
} satisfies Meta<typeof Button>

export default meta
type Story = StoryObj<typeof meta>

export const Default: Story = {
  args: {
    children: 'Button',
  },
}

export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary',
  },
}

export const Destructive: Story = {
  args: {
    variant: 'destructive',
    children: 'Delete',
  },
}

export const Outline: Story = {
  args: {
    variant: 'outline',
    children: 'Outline',
  },
}

export const Ghost: Story = {
  args: {
    variant: 'ghost',
    children: 'Ghost',
  },
}

export const Link: Story = {
  args: {
    variant: 'link',
    children: 'Link',
  },
}

export const Gradient: Story = {
  args: {
    variant: 'gradient',
    children: 'Gradient',
  },
}

export const Glass: Story = {
  args: {
    variant: 'glass',
    children: 'Glass',
  },
  parameters: {
    backgrounds: { default: 'gradient' },
  },
}

export const AI: Story = {
  args: {
    variant: 'ai',
    children: 'AI Powered',
    icon: React.createElement(Sparkles, { className: 'w-4 h-4' }),
  },
}

export const Small: Story = {
  args: {
    size: 'sm',
    children: 'Small',
  },
}

export const Large: Story = {
  args: {
    size: 'lg',
    children: 'Large',
  },
}

export const ExtraLarge: Story = {
  args: {
    size: 'xl',
    children: 'Extra Large',
  },
}

export const WithIcon: Story = {
  args: {
    children: 'Download',
    icon: React.createElement(Download, { className: 'w-4 h-4' }),
  },
}

export const Loading: Story = {
  args: {
    children: 'Please wait',
    loading: true,
  },
}

export const Disabled: Story = {
  args: {
    children: 'Disabled',
    disabled: true,
  },
}

export const IconOnly: Story = {
  args: {
    size: 'icon',
    children: React.createElement(Heart, { className: 'w-4 h-4' }),
  },
}

export const IconSmall: Story = {
  args: {
    size: 'icon-sm',
    variant: 'outline',
    children: React.createElement(Heart, { className: 'w-4 h-4' }),
  },
}

export const IconLarge: Story = {
  args: {
    size: 'icon-lg',
    variant: 'gradient',
    children: React.createElement(Sparkles, { className: 'w-4 h-4' }),
  },
}