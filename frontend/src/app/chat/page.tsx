import React from 'react';
import ChatComponent from '@/components/ChatComponent';

export default function ChatPage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="text-4xl font-bold mb-8">AI Chatbot</h1>
      <div className="w-full max-w-md">
        <ChatComponent />
      </div>
    </div>
  );
}