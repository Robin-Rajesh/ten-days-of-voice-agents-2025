import { Button } from '@/components/livekit/button';
import Image from 'next/image';

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  return (
    <div ref={ref}>
      <section className="bg-background flex flex-col items-center justify-center text-center">
        {/* Stranger Things Logo */}
        <div className="mb-8">
          <Image
            src="/Stranger_Things_logo.png"
            alt="Stranger Things"
            width={400}
            height={200}
            priority
            className="max-w-md w-full h-auto"
          />
        </div>

        <p className="text-foreground max-w-prose pt-1 leading-6 font-medium text-lg">
          A D&D-style voice adventure set in Hawkins, 1985
        </p>

        <Button variant="primary" size="lg" onClick={onStartCall} className="mt-8 w-72 font-mono text-lg">
          {startButtonText}
        </Button>
      </section>

      <div className="fixed bottom-5 left-0 flex w-full items-center justify-center">
        <p className="text-muted-foreground max-w-prose pt-1 text-xs leading-5 font-normal text-pretty md:text-sm">
          Powered by{' '}
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://livekit.io"
            className="underline"
          >
            LiveKit Agents
          </a>
        </p>
      </div>
    </div>
  );
};
