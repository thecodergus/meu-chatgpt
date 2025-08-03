import React from 'react'
import { Link } from 'react-router-dom'

interface SidebarProps {
  conversations: { id: string; title: string }[]
}

const Sidebar: React.FC<SidebarProps> = ({ conversations }) => {
  return (
    <div className="flex flex-col h-full w-64 bg-gray-100 border-r">
      <nav className="flex-0 p-4">
        <ul className="space-y-2">
          <li>
            <Link to="/conversations/new" className="block p-2 hover:bg-gray-200 rounded">
              Criar nova conversa
            </Link>
          </li>
          <li>
            <Link to="/agents" className="block p-2 hover:bg-gray-200 rounded">
              Criar/Editar Agentes
            </Link>
          </li>
          <li>
            <Link to="/knowledge-bases" className="block p-2 hover:bg-gray-200 rounded">
              Criar/Editar bases de conhecimento
            </Link>
          </li>
          <li>
            <Link to="/conversations/manage" className="block p-2 hover:bg-gray-200 rounded">
              Gerenciar conversas
            </Link>
          </li>
        </ul>
      </nav>
      <div className="border-t mt-4" />
      <div className="flex-1 overflow-y-auto p-4">
        <h3 className="text-sm font-semibold mb-2">Histórico</h3>
        <ul className="space-y-2">
          {conversations.map((conv) => (
            <li key={conv.id}>
              <Link to={`/conversations/${conv.id}`} className="block p-2 hover:bg-gray-200 rounded">
                {conv.title}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default Sidebar