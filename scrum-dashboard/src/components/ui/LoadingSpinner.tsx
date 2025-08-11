'use client'

import React from 'react'
import { motion } from 'framer-motion'

export function LoadingSpinner() {
  return (
    <div className="min-h-screen bg-background flex items-center justify-center">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="text-center space-y-4"
      >
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-12 h-12 mx-auto"
        >
          <div className="w-12 h-12 rounded-full border-4 border-primary border-t-transparent animate-spin" />
        </motion.div>
        <div>
          <h2 className="text-xl font-semibold text-foreground">Loading Dashboard</h2>
          <p className="text-muted-foreground">Preparing your workspace...</p>
        </div>
      </motion.div>
    </div>
  )
}
