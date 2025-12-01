import { Button } from '@/components/livekit/button';
import { useState } from 'react';

interface WelcomeViewProps {
  startButtonText: string;
  onStartCall: () => void;
}

export const WelcomeView = ({
  startButtonText,
  onStartCall,
  ref,
}: React.ComponentProps<'div'> & WelcomeViewProps) => {
  const [contestantName, setContestantName] = useState('');

  const handleStartClick = () => {
    // Store the name in session storage so the agent can access it if needed
    if (contestantName.trim()) {
      sessionStorage.setItem('contestantName', contestantName.trim());
    }
    onStartCall();
  };

  return (
    <div ref={ref}>
      <section className="bg-background flex flex-col items-center justify-center text-center">
        {/* Improv Battle Icon - Theater Masks */}
        <div className="mb-8">
          <svg
            className="w-32 h-32 text-primary"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            {/* Comedy/Tragedy Masks */}
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
        </div>

        <h1 className="text-foreground text-5xl font-bold mb-4 tracking-tight">
          🎭 IMPROV BATTLE 🎭
        </h1>

        <p className="text-foreground max-w-prose pt-1 leading-7 font-medium text-xl mb-8">
          Test your improvisation skills in this high-energy voice game show!
        </p>

        <div className="w-full max-w-md space-y-6">
          {/* Name Input Field */}
          <div className="space-y-2">
            <label
              htmlFor="contestant-name"
              className="text-foreground text-sm font-semibold block text-left"
            >
              Contestant Name
            </label>
            <input
              id="contestant-name"
              type="text"
              value={contestantName}
              onChange={(e) => setContestantName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && contestantName.trim()) {
                  handleStartClick();
                }
              }}
              placeholder="Enter your name..."
              className="w-full px-4 py-3 text-lg rounded-lg border-2 border-primary/30 bg-background text-foreground placeholder:text-muted-foreground focus:outline-none focus:border-primary focus:ring-2 focus:ring-primary/20 transition-all"
              autoFocus
            />
          </div>

          {/* Start Button */}
          <Button
            variant="primary"
            size="lg"
            onClick={handleStartClick}
            disabled={!contestantName.trim()}
            className="w-full font-mono text-lg py-6 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {startButtonText}
          </Button>
        </div>

        {/* Game Info */}
        <div className="mt-12 max-w-md text-left space-y-3">
          <h3 className="text-foreground font-bold text-lg mb-4">How It Works:</h3>
          <div className="space-y-2 text-muted-foreground">
            <p className="flex items-start gap-2">
              <span className="text-primary font-bold">1.</span>
              <span>You'll get 3 improv scenarios</span>
            </p>
            <p className="flex items-start gap-2">
              <span className="text-primary font-bold">2.</span>
              <span>Act out each scenario in character</span>
            </p>
            <p className="flex items-start gap-2">
              <span className="text-primary font-bold">3.</span>
              <span>The host will react to your performance</span>
            </p>
            <p className="flex items-start gap-2">
              <span className="text-primary font-bold">4.</span>
              <span>Get honest feedback - not always supportive!</span>
            </p>
          </div>
        </div>
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
