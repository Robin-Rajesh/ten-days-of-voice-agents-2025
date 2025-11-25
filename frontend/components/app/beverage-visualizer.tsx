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

  return null;
}

