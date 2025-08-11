'use client'

import React from 'react'
import { cn } from '@/lib/utils'

export interface AvatarProps extends React.HTMLAttributes<HTMLDivElement> {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  src?: string
  alt?: string
  fallback?: string
  online?: boolean
}

const sizeMap = {
  xs: 'w-6 h-6 text-xs',
  sm: 'w-8 h-8 text-sm',
  md: 'w-10 h-10 text-base',
  lg: 'w-12 h-12 text-lg',
  xl: 'w-16 h-16 text-xl'
}

const Avatar = React.forwardRef<HTMLDivElement, AvatarProps>(
  ({ className, size = 'md', src, alt, fallback, online, children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(
          'relative inline-flex items-center justify-center rounded-full bg-gradient-to-r from-blue-400 to-purple-400 font-semibold text-white',
          sizeMap[size],
          className
        )}
        {...props}
      >
        {src ? (
          <img
            src={src}
            alt={alt || 'Avatar'}
            className="w-full h-full rounded-full object-cover"
          />
        ) : (
          <span className="font-semibold text-white">
            {fallback || (children && typeof children === 'string' ? children.charAt(0).toUpperCase() : '?')}
          </span>
        )}
        
        {online !== undefined && (
          <span
            className={cn(
              'absolute -bottom-0.5 -right-0.5 block rounded-full border-2 border-white dark:border-gray-800',
              online 
                ? 'bg-green-400' 
                : 'bg-gray-400',
              size === 'xs' && 'w-2 h-2',
              size === 'sm' && 'w-2.5 h-2.5',
              size === 'md' && 'w-3 h-3',
              size === 'lg' && 'w-3.5 h-3.5',
              size === 'xl' && 'w-4 h-4'
            )}
          />
        )}
      </div>
    )
  }
)

Avatar.displayName = 'Avatar'

export { Avatar }