// app/api/admin/login/route.js
import { NextResponse } from 'next/server';

export async function POST(request) {
  const { password } = await request.json();

  if (password !== process.env.ADMIN_SECRET) {
    return NextResponse.json({ error: 'Wrong password' }, { status: 401 });
  }

  const response = NextResponse.json({ success: true });

  response.cookies.set('admin_token', process.env.ADMIN_SECRET, {
    httpOnly: true,
    secure:   true,
    sameSite: 'strict',
    maxAge:   60 * 60 * 8, // 8 hours
    path:     '/',
  });

  return response;
}