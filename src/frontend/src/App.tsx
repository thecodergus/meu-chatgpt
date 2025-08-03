import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import ChatPage from './pages/ChatPage'
import ConversationHistory from './components/ConversationHistory'

function App() {
  const conversations = [
    { id: '1', title: 'Conversa 1' },
    { id: '2', title: 'Conversa 2' },
  ]
  const events = conversations.map((conv) => ({
    id: conv.id,
    title: conv.title,
    date: new Date().toISOString().split('T')[0],
  }))

  return (
    <BrowserRouter>
      <div className="flex h-screen">
        <Sidebar conversations={conversations} />
        <div className="flex-1 flex flex-col">
          <Routes>
            <Route path="/" element={<ConversationHistory events={events} />} />
            <Route path="/conversations/new" element={<ChatPage />} />
            <Route path="/conversations/:id" element={<ChatPage />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App
