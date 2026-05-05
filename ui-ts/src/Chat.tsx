import { useEffect, useRef, useState } from 'react'
import { sendMessage } from './api'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function Chat({ athleteId }: { athleteId: number }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [thinking, setThinking] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, thinking])

  async function send() {
    const text = input.trim()
    if (!text || thinking) return
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: text }])
    setThinking(true)
    try {
      const reply = await sendMessage(athleteId, text)
      setMessages(prev => [...prev, { role: 'assistant', content: reply }])
    } catch (e) {
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: `Error: ${e instanceof Error ? e.message : 'unknown error'}`,
      }])
    } finally {
      setThinking(false)
    }
  }

  return (
    <div className="chat">
      <h3>Ask your coach</h3>
      <div className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.role}`}>
            <span className="role">{m.role === 'user' ? 'You' : 'Coach'}</span>
            <p>{m.content}</p>
          </div>
        ))}
        {thinking && (
          <div className="message assistant">
            <span className="role">Coach</span>
            <p className="muted thinking">Thinking...</p>
          </div>
        )}
        <div ref={bottomRef} />
      </div>
      <div className="input-row">
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => { if (e.key === 'Enter') void send() }}
          placeholder="Ask about your training..."
          disabled={thinking}
          autoFocus
        />
        <button
          className="btn btn-primary"
          onClick={() => void send()}
          disabled={thinking || !input.trim()}
        >
          Send
        </button>
      </div>
    </div>
  )
}
