import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

function Home(){
  return (<div className="p-6"> <h1 className="text-2xl font-bold">Retail Sales & Inventory Analytics Dashboard (Frontend Scaffold)</h1>
  <p className="mt-4">Connect to backend at <code>http://localhost:8000</code></p></div>)
}

function App(){
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home/>} />
      </Routes>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(<App />)
