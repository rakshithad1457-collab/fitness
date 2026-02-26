// middleware.js  (place this in your project ROOT, next to package.json)
// Protects /admin/* routes — checks for a signed admin cookie.
// Works on Vercel Edge Runtime with zero extra dependencies.

import { NextResponse } from 'next/server';

export function middleware(request) {
  const { pathname } = request.nextUrl;

  // Only guard /admin routes (not /admin/login)
  if (pathname.startsWith('/admin') && pathname !== '/admin/login') {
    const adminToken = request.cookies.get('admin_token')?.value;

    if (!adminToken || adminToken !== process.env.ADMIN_SECRET) {
      const loginUrl = new URL('/admin/login', request.url);
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/admin/:path*'],
};