'use client';

import { useEffect, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { tokenManager } from '@/utils/api';

function AuthContent() {
    const searchParams = useSearchParams();
    const router = useRouter();

    useEffect(() => {
        // Get token from URL
        const token = searchParams.get('token');
        const error = searchParams.get('error');

        if (error) {
            // Handle error
            console.error('Auth error:', error);
            router.push('/?error=' + error);
            return;
        }

        if (token) {
            // Save token to localStorage
            tokenManager.saveToken(token);

            // Redirect to dashboard
            router.push('/dashboard');
        } else {
            // No token, redirect to home
            router.push('/');
        }
    }, [searchParams, router]);

    return (
        <div className="min-h-screen bg-slate-950 flex items-center justify-center relative overflow-hidden">
            {/* Texture Overlay */}
            <div className="fixed inset-0 z-0 pointer-events-none opacity-20"
                style={{ backgroundImage: 'radial-gradient(circle at 1px 1px, rgba(168,85,247,0.15) 1px, transparent 0)', backgroundSize: '40px 40px' }}>
            </div>

            {/* Background Glow */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-purple-600/20 blur-[100px] rounded-full -z-10"></div>

            <div className="text-center z-10">
                <div className="animate-spin rounded-full h-16 w-16 border-4 border-purple-500/30 border-t-purple-500 mx-auto mb-6"></div>
                <h2 className="text-white text-3xl font-bold mb-3">Connecting to Spotify</h2>
                <p className="text-purple-300/60 text-xl animate-pulse">Analyzing your resonance...</p>
            </div>
        </div>
    );
}

export default function AuthCallback() {
    return (
        <Suspense fallback={
            <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
                Loading...
            </div>
        }>
            <AuthContent />
        </Suspense>
    );
}
