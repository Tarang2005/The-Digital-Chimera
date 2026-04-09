"use client"
import React, { useEffect, useRef, useState } from 'react';
import { submitSegment } from '@/lib/api';

interface FabricCanvasProps {
  corpseId: number;
  sessionId: string;
  targetSegment: string;
  sliverUrl?: string | null;
  onSuccess: () => void;
}

export default function FabricCanvas({ corpseId, sessionId, targetSegment, sliverUrl, onSuccess }: FabricCanvasProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [fabricCanvas, setFabricCanvas] = useState<any | null>(null);
  const [color, setColor] = useState('#ffffff');
  const [brushSize, setBrushSize] = useState(5);

  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [toastMsg, setToastMsg] = useState<string | null>(null);

  useEffect(() => {
    if (!canvasRef.current) return;

    let canvas: any;

    const initCanvas = async () => {
      const { fabric } = await import('fabric');

      canvas = new fabric.Canvas(canvasRef.current!, {
        isDrawingMode: true,
        width: 500,
        height: 500,
        backgroundColor: '#1e293b',
      });

      setFabricCanvas(canvas);

      if (sliverUrl) {
        fabric.Image.fromURL(sliverUrl, (img: any) => {
          img.set({ left: 0, top: 0, selectable: false, evented: false, opacity: 0.5 });
          canvas.add(img);
        });
      }
    };

    initCanvas();

    return () => {
      canvas?.dispose();
    };
  }, [sliverUrl]);

  useEffect(() => {
    if (fabricCanvas && fabricCanvas.freeDrawingBrush) {
      fabricCanvas.freeDrawingBrush.color = color;
      fabricCanvas.freeDrawingBrush.width = brushSize;
    }
  }, [fabricCanvas, color, brushSize]);

  const handleClear = async () => {
    if (!fabricCanvas) return;
    const { fabric } = await import('fabric');
    fabricCanvas.clear();
    fabricCanvas.backgroundColor = '#1e293b';
    if (sliverUrl) {
      fabric.Image.fromURL(sliverUrl, (img: any) => {
        img.set({ left: 0, top: 0, selectable: false, evented: false, opacity: 0.5 });
        fabricCanvas.add(img);
        fabricCanvas.renderAll();
      });
    }
  };

  const handleSubmit = async () => {
    if (!fabricCanvas) return;

    setIsSubmitting(true);
    setError(null);
    setToastMsg(null);

    try {
      const dataUrl = fabricCanvas.toDataURL({ format: 'png', quality: 1 });

      await submitSegment(corpseId, sessionId, targetSegment, dataUrl);

      setToastMsg("Masterpiece submitted successfully!");
      setTimeout(() => {
        handleClear();
        onSuccess();
      }, 1500);
    } catch (err: any) {
      setError(err.message || "An unknown error occurred.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="flex flex-col items-center gap-4 glass-panel p-6 rounded-xl relative">

      {/* Toast Notification */}
      {(error || toastMsg) && (
        <div className={`absolute -top-16 px-4 py-2 rounded shadow-lg text-white font-bold transition-all ${error ? 'bg-red-500' : 'bg-green-500'}`}>
          {error || toastMsg}
        </div>
      )}

      {/* Loading Overlay */}
      {isSubmitting && (
        <div className="absolute inset-0 z-50 flex items-center justify-center bg-slate-900/80 rounded-xl backdrop-blur-sm">
          <div className="flex flex-col items-center gap-4 text-white">
            <svg className="animate-spin h-10 w-10 text-pink-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span className="text-lg font-semibold animate-pulse">Uploading masterpiece...</span>
          </div>
        </div>
      )}

      <div className="flex gap-4 items-center bg-slate-800/50 p-3 rounded-lg border border-slate-700 w-full justify-between z-10">
        <div className="flex gap-4 items-center">
          <input
            type="color"
            value={color}
            onChange={(e) => setColor(e.target.value)}
            className="w-8 h-8 rounded cursor-pointer bg-transparent border-0"
            disabled={isSubmitting}
          />
          <input
            type="range"
            min="1" max="50"
            value={brushSize}
            onChange={(e) => setBrushSize(parseInt(e.target.value))}
            className="cursor-pointer"
            disabled={isSubmitting}
          />
        </div>
        <div className="flex gap-2">
          <button onClick={handleClear} disabled={isSubmitting} className="px-4 py-2 bg-slate-700 hover:bg-slate-600 border border-slate-600 disabled:opacity-50 rounded transition text-sm font-semibold">Clear</button>
          <button onClick={handleSubmit} disabled={isSubmitting} className="px-4 py-2 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-400 hover:to-pink-400 disabled:opacity-50 rounded text-sm font-semibold transition">Submit Turn</button>
        </div>
      </div>

      <div className="border border-slate-600 rounded-lg overflow-hidden shadow-2xl relative z-10">
        <canvas ref={canvasRef} />
      </div>
      <p className="text-slate-400 text-sm">{sliverUrl ? "Use the top guide to align your drawing!" : "You're drawing the head! Start anywhere."}</p>
    </div>
  );
}