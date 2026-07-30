import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // Sirf console check ke liye
  return NextResponse.next();
}

export const config = {
  matcher: ['/tasks/:path*', '/login', '/signup', '/chat'],
};