'use client';

import React, { useState, FormEvent, useEffect, useRef, useCallback } from 'react';
import { getToken } from '@/lib/auth';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
  isError?: boolean;
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

  const scrollToBottom = useCallback(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, []);

  useEffect(scrollToBottom, [messages, loading]);

  // ✅ Load Chat History
  const fetchHistory = useCallback(async () => {
    if (!token) return;
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/chat/history`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) {
        console.error('Failed to load chat history.');
        return;
      }
      const history = await response.json();
      const formattedMessages: Message[] = [];
      history.forEach((h: any, index: number) => {
        formattedMessages.push({ id: index * 2, text: h.message_content, sender: 'user' });
        formattedMessages.push({ id: index * 2 + 1, text: h.response_content, sender: 'ai' });
      });
      setMessages(formattedMessages);
    } catch (err) {
      console.error('Network error while loading chat history', err);
    }
  }, [token]);

  useEffect(() => {
    fetchHistory();
  }, [fetchHistory]);

  const handleSubmit = async (e: FormEvent | string, messageText?: string) => {
    if (e && typeof e !== 'string') e.preventDefault();
    const textToSubmit = typeof e === 'string' ? e : input;
    if (!textToSubmit.trim() || !token) return;

    const userMessage: Message = { id: Date.now(), text: textToSubmit, sender: 'user' };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const controller = new AbortController();
      const response = await fetch(`${process.env.NEXT_PUBLIC_BACKEND_URL}/api/v1/chat/send-message`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` },
        body: JSON.stringify({ message: textToSubmit }),
        signal: controller.signal
      });

      if (!response.ok) throw new Error('API Error');
      const data = await response.json();
      setMessages((prev) => [...prev, { id: Date.now() + 1, text: data.response, sender: 'ai' }]);
    } catch (err: any) {
      setMessages((prev) => [
        ...prev,
        { id: Date.now() + 1, text: `Error: ${err.message}`, sender: 'ai', isError: true },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-[70vh] max-h-[800px] bg-gray-900 text-gray-100 border border-gray-700 rounded-xl overflow-hidden shadow-2xl">
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div key={msg.id} className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[85%] px-4 py-2 rounded-2xl text-sm ${msg.sender === 'user' ? 'bg-blue-600 text-white' : 'bg-gray-700 text-gray-100'}`}>
              {msg.text}
              {msg.isError && (
                <button onClick={() => handleSubmit(msg.text)} className="block mt-2 text-xs text-red-300 underline font-semibold">Retry</button>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-700 px-4 py-2 rounded-2xl text-sm animate-pulse">AI is typing...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSubmit} className="p-3 border-t border-gray-700 bg-gray-800 flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your tasks..."
          className="flex-1 bg-gray-900 p-2 rounded-lg outline-none border border-gray-600 focus:border-blue-500 text-sm"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-lg text-sm font-semibold transition"
        >
          {loading ? '...' : 'Send'}
        </button>
      </form>
    </div>
  );
}
