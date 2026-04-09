"use client"
import React, { useEffect, useState } from 'react';
import dynamic from 'next/dynamic';
import { getAvailableTurn, TurnData } from '@/lib/api';

const FabricCanvas = dynamic(() => import('@/components/canvas/FabricCanvas'), {
  ssr: false,
});

export default function Home() {
    const [turnData, setTurnData] = useState<TurnData | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    const fetchTurn = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await getAvailableTurn();
            setTurnData(data);
        } catch (err: any) {
            setError(err.message || 'Failed to fetch turn.');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchTurn();
    }, []);

    const handleSuccess = () => {
        // Fetch the next available turn
        fetchTurn();
    };

    if (loading) {
        return (
            <div className="flex flex-col items-center gap-8 w-full max-w-4xl pt-20">
                <svg className="animate-spin h-10 w-10 text-pink-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <p className="text-slate-300 font-semibold text-lg animate-pulse">Finding an available canvas...</p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex flex-col items-center gap-8 w-full max-w-4xl pt-20">
                <div className="bg-red-500/20 text-red-100 px-6 py-4 rounded border border-red-500/50 text-center">
                    <h2 className="text-2xl font-bold mb-2">Connection Error</h2>
                    <p>{error}</p>
                    <button onClick={fetchTurn} className="mt-4 px-4 py-2 bg-red-500 hover:bg-red-400 font-semibold rounded">Try Again</button>
                </div>
            </div>
        );
    }

    if (!turnData) return null;

    // Remove 'Needs_' from target segment string for cleaner UI
    const friendlyName = turnData.target_segment.replace('Needs_', '');

    return (
        <div className="flex flex-col items-center gap-8 w-full max-w-4xl animate-in fade-in duration-500">
            <div className="text-center space-y-4">
                <h2 className="text-4xl font-black tracking-tight flex items-center justify-center gap-3">
                    Your Turn: <span className="text-pink-400 bg-pink-500/10 px-3 py-1 rounded-md">{friendlyName}</span>
                </h2>
                <p className="text-slate-400 text-lg">Continue the masterpiece before your lock expires.</p>
            </div>
            
            <FabricCanvas 
                corpseId={turnData.corpse_id}
                sessionId={turnData.session_id}
                targetSegment={turnData.target_segment}
                sliverUrl={turnData.sliver_url}
                onSuccess={handleSuccess} 
            />
        </div>
    );
}
