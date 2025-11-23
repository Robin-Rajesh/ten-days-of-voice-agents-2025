'use client';

import { useEffect, useState } from 'react';
import { useRoomContext } from '@livekit/components-react';
import { RoomEvent, type DataPacket_Kind, type RemoteParticipant } from 'livekit-client';

interface OrderData {
  drinkType?: string;
  size?: string;
  milk?: string;
  extras?: string[] | string;
  name?: string;
}

export function BeverageVisualizer() {
  const room = useRoomContext();
  const [orderData, setOrderData] = useState<OrderData>({});

  useEffect(() => {
    if (!room) return;

    const handleDataReceived = (
      payload: Uint8Array,
      participant?: RemoteParticipant,
      kind?: DataPacket_Kind,
      topic?: string
    ) => {
      try {
        const decoder = new TextDecoder();
        const strData = decoder.decode(payload);
        const json = JSON.parse(strData);

        if (json.type === 'order_update' && json.data) {
          setOrderData(json.data);
        }
      } catch (e) {
        console.error('Error parsing order data:', e);
      }
    };

    room.on(RoomEvent.DataReceived, handleDataReceived);

    return () => {
      room.off(RoomEvent.DataReceived, handleDataReceived);
    };
  }, [room]);

  // Determine size class
  const getSizeClass = () => {
    if (!orderData.size) return 'medium';
    const size = orderData.size.toLowerCase();
    if (size.includes('small') || size.includes('tall')) return 'small';
    if (size.includes('large') || size.includes('venti')) return 'large';
    return 'medium';
  };

  // Check if has whipped cream
  const hasWhip = () => {
    if (!orderData.extras) return false;
    const extras = Array.isArray(orderData.extras)
      ? orderData.extras.join(' ')
      : String(orderData.extras);
    return extras.toLowerCase().includes('whip') || extras.toLowerCase().includes('whipped');
  };

  // Check if has milk
  const hasMilk = () => {
    return orderData.milk && orderData.milk.toLowerCase() !== 'none';
  };

  const sizeClass = getSizeClass();
  const showWhip = hasWhip();
  const showMilk = hasMilk();

  return (
    <div className="fixed right-4 top-4 z-50 flex flex-col gap-4">
      {/* Receipt */}
      <div className="bg-white p-4 rounded-lg shadow-lg border-t-4 border-gray-800 w-48">
        <h3 className="text-center font-bold border-b border-dashed border-gray-300 pb-2 mb-2 text-gray-900">
          MURF COFFEE
        </h3>
        <div className="text-sm space-y-1 text-gray-900">
          <div>Cust: {orderData.name || 'Pending...'}</div>
          <div>Drink: {orderData.drinkType || '...'}</div>
          <div>Size: {orderData.size || '...'}</div>
          <div>Extras: {orderData.extras ? (Array.isArray(orderData.extras) ? orderData.extras.join(', ') : orderData.extras) : '-'}</div>
        </div>
        <div className="border-t border-dashed border-gray-300 pt-2 mt-2 text-right font-bold text-xs text-gray-900">
          STATUS: PREPARING
        </div>
      </div>

      {/* Visual Cup */}
      <div className="relative flex flex-col items-center justify-end h-64 w-48">
        {/* Steam */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 flex gap-2">
          <div className="w-2 h-8 bg-gray-400 rounded-full blur-sm opacity-60 animate-pulse" />
          <div className="w-2 h-8 bg-gray-400 rounded-full blur-sm opacity-60 animate-pulse" style={{ animationDelay: '0.5s' }} />
        </div>

        {/* Cup */}
        <div
          className={`relative bg-amber-900 rounded-b-3xl border-4 border-amber-950 flex items-center justify-center text-white font-bold transition-all duration-500 ${
            sizeClass === 'small' ? 'w-20 h-20' : sizeClass === 'large' ? 'w-32 h-40' : 'w-24 h-28'
          } ${showMilk ? 'bg-amber-200' : ''}`}
        >
          {/* Cup Handle */}
          <div className="absolute -right-4 top-4 w-6 h-10 border-4 border-amber-950 border-l-0 rounded-r-full" />

          {/* Size Label */}
          <span className="text-lg">{sizeClass.charAt(0).toUpperCase()}</span>

          {/* Whipped Cream */}
          {showWhip && (
            <div className="absolute -top-6 left-0 right-0 h-10 bg-white rounded-full shadow-md transition-all duration-500">
              <div className="absolute top-0 left-4 w-8 h-8 bg-white rounded-full" />
              <div className="absolute top-0 right-4 w-6 h-6 bg-white rounded-full" />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

