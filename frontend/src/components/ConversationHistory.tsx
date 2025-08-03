import React from 'react'
import FullCalendar, { EventInput } from '@fullcalendar/react'
import dayGridPlugin from '@fullcalendar/daygrid'

// Eventos de conversa com data
interface ConversationEvent {
  id: string
  title: string
  date: string // ISO date string
}

interface ConversationHistoryProps {
  events: ConversationEvent[]
}

const ConversationHistory: React.FC<ConversationHistoryProps> = ({ events }) => {
  // Converte ConversationEvent para EventInput do FullCalendar
  const calendarEvents: EventInput[] = events.map((e) => ({
    id: e.id,
    title: e.title,
    date: e.date,
  }))

  return (
    <div className="h-full overflow-auto p-4">
      <FullCalendar
        plugins={[dayGridPlugin]}
        initialView="dayGridMonth"
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: '',
        }}
        events={calendarEvents}
        height="auto"
      />
    </div>
  )
}

export default ConversationHistory