'use client';

import React, { useState, FormEvent, useEffect, useRef } from 'react';
import { getToken } from '@/lib/auth';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
}

export default function ChatComponent() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // ✅ get token CLIENT SIDE only
  useEffect(() => {
    setToken(getToken());
  }, []);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(scrollToBottom, [messages]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !token) return;

    const userMessage: Message = {
      id: messages.length + 1,
      text: input,
      sender: 'user',
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/chat/send-message`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ message: input }),
        }
      );

      if (!response.ok) {
        const text = await response.text();
        throw new Error(text || 'Chat API error');
      }

      const data = await response.json();

      const aiMessage: Message = {
        id: messages.length + 2,
        text: data.response,
        sender: 'ai',
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        {
          id: messages.length + 2,
          text: `Error: ${err.message}`,
          sender: 'ai',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[600px] bg-gray-900 text-gray-100 border border-gray-700 rounded-xl">
      <div className="flex-1 p-4 overflow-y-auto">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`mb-3 max-w-[75%] px-4 py-2 rounded-xl ${
              msg.sender === 'user'
                ? 'ml-auto bg-blue-600'
                : 'mr-auto bg-gray-700'
            }`}
          >
            {msg.text}
          </div>
        ))}
        {loading && (
          <div className="mr-auto bg-gray-700 px-4 py-2 rounded-xl animate-pulse">
            AI is thinking…
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="flex border-t border-gray-700">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          className="flex-1 p-3 bg-gray-800 outline-none"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  );
}