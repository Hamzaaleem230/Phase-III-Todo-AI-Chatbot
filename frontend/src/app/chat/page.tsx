"use client";

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getToken } from '@/lib/auth';
import ChatComponent from '@/components/ChatComponent';

export default function ChatPage() {
  const router = useRouter();
  const [authorized, setAuthorized] = useState<boolean>(false);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      router.push('/login');
    } else {
      setAuthorized(true);
    }
  }, [router]);

  if (!authorized) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  return (
    <div className="flex flex-col items-center min-h-screen py-2 px-4">
      <h1 className="text-4xl font-bold mb-8">AI Chatbot</h1>
      <div className="w-full max-w-4xl">
        <ChatComponent />
      </div>
    </div>
  );
}