'use client'

import React from 'react'
import { cn } from '@/lib/utils'

interface SkipLinkProps {
  href?: string
  className?: string
  children?: React.ReactNode
}

export const SkipLink: React.FC<SkipLinkProps> = ({ 
  href = '#main-content',
  className,
  children = 'Skip to main content'
}) => {
  return (
    <a
      href={href}
      className={cn(
        'sr-only focus:not-sr-only focus:absolute focus:top-4 focus:left-4 focus:z-50',
        'bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium',
        'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:ring-offset-2',
        'transition-all duration-200',
        className
      )}
      onFocus={(e) => {
        // Smooth scroll to target when focused
        setTimeout(() => {
          const target = document.querySelector(href)
          if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' })
          }
        }, 100)
      }}
    >
      {children}
    </a>
  )
}

// Multiple skip links for complex layouts
export const SkipLinks: React.FC<{ 
  links?: Array<{ href: string; label: string }> 
}> = ({ 
  links = [
    { href: '#main-content', label: 'Skip to main content' },
    { href: '#navigation', label: 'Skip to navigation' },
    { href: '#sidebar', label: 'Skip to sidebar' }
  ]
}) => {
  return (
    <nav aria-label="Skip links" className="sr-only focus-within:not-sr-only">
      <ul className="fixed top-4 left-4 z-50 space-y-2">
        {links.map((link) => (
          <li key={link.href}>
            <SkipLink href={link.href}>
              {link.label}
            </SkipLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}