import React, { useState } from 'react'
import ReactMarkdown from 'react-markdown'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

const ChatPage: React.FC = () => {
  // const { id } = useParams<{ id: string }>() // ID não utilizado
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState<string>('')
  const [showSettings, setShowSettings] = useState<boolean>(false)
  const [temperature, setTemperature] = useState<number>(0.7)
  const [topP, setTopP] = useState<number>(1.0)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0]
      const url = URL.createObjectURL(file)
      const newUserMessage: Message = {
        role: 'user',
        content: `![${file.name}](${url})`,
      }
      setMessages((prev) => [...prev, newUserMessage])
      e.target.value = ''
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return
    const newUserMessage: Message = { role: 'user', content: input }
    setMessages((prev) => [...prev, newUserMessage])
    setInput('')
    const assistantResponse: Message = { role: 'assistant', content: 'Resposta do agente!' }
    setMessages((prev) => [...prev, assistantResponse])
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 overflow-auto p-4 space-y-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`prose ${msg.role === 'assistant' ? 'bg-gray-100 p-2 rounded' : ''}`}
          >
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
        ))}
      </div>
      <div className="p-4 border-t">
        <button
          type="button"
          onClick={() => setShowSettings((s) => !s)}
          className="text-sm text-gray-600 hover:text-gray-800"
        >
          {showSettings ? 'Ocultar Configurações' : 'Mostrar Configurações'}
        </button>
        {showSettings && (
          <div className="mt-2 space-y-2">
            <div>
              <label className="text-sm">Temperatura: {temperature}</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={temperature}
                onChange={(e) => setTemperature(parseFloat(e.target.value))}
                className="w-full"
              />
            </div>
            <div>
              <label className="text-sm">Top-p: {topP}</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={topP}
                onChange={(e) => setTopP(parseFloat(e.target.value))}
                className="w-full"
              />
            </div>
          </div>
        )}
      </div>
      <form onSubmit={handleSubmit} className="p-4 border-t flex items-center space-x-2">
        <input type="file" onChange={handleFileChange} className="mr-2" />
        <input
          type="text"
          className="flex-1 border rounded px-3 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Digite sua mensagem..."
        />
        <button type="submit" className="bg-blue-500 text-white rounded px-4 py-2">
          Enviar
        </button>
      </form>
    </div>
)

}

export default ChatPage