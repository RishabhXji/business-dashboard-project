import React from 'react'

export default function PlaceholderCard({title, children}){
  return (
    <div className="bg-white dark:bg-gray-800 shadow rounded p-4">
      <h3 className="font-semibold text-gray-700 dark:text-gray-200">{title}</h3>
      <div className="mt-2">{children}</div>
    </div>
  )
}
