import { Button } from '@/components/livekit/button';

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
    <div ref={ref} className="relative min-h-svh">
      <section className="relative flex min-h-svh flex-col items-center justify-center overflow-hidden px-6 py-16 text-center">
        <div
          className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(66,233,245,0.25),_transparent_55%),_radial-gradient(circle_at_bottom,_rgba(244,69,156,0.15),_transparent_45%)] blur-3xl"
          aria-hidden
        />
        <div className="relative z-10 flex w-full max-w-3xl flex-col gap-6 rounded-3xl border border-white/10 bg-background/80 p-8 text-foreground shadow-2xl backdrop-blur">
          <div className="text-left">
            <p className="text-sm font-semibold uppercase tracking-wide text-white/70">Day 4 · Teach-the-Tutor</p>
            <h1 className="mt-2 text-3xl font-semibold leading-tight text-white sm:text-4xl">
              Active recall coach with three focused learning modes
            </h1>
            <p className="mt-3 text-base leading-7 text-white/80">
              This agent greets the learner, lets them pick a mode, and then uses a shared JSON syllabus
              to explain a concept, quiz them, or ask for a teach-back. Voices switch automatically:
              Matthew for learn, Alicia for quiz, and Ken for teach_back.
            </p>
          </div>

          <div className="grid w-full gap-3 text-left sm:grid-cols-3">
            {[
              {
                title: 'LEARN · Matthew',
                body: 'Pulls the concept summary from shared-data/day4_tutor_content.json and explains it clearly.',
              },
              {
                title: 'QUIZ · Alicia',
                body: 'Asks the sample_question for the chosen concept and gives lightweight feedback.',
              },
              {
                title: 'TEACH-BACK · Ken',
                body: 'Prompts the learner to explain the concept back and offers qualitative scoring.',
              },
            ].map((item) => (
              <div
                key={item.title}
                className="rounded-2xl border border-white/5 bg-white/5 p-4 text-white shadow-inner"
              >
                <p className="text-sm font-semibold uppercase tracking-wide text-white/80">{item.title}</p>
                <p className="mt-2 text-sm text-white/70">{item.body}</p>
              </div>
            ))}
          </div>

          <div className="w-full rounded-2xl border border-dashed border-white/10 bg-black/20 p-4 text-left text-white/80">
            <p className="text-sm font-semibold uppercase tracking-wide text-white/70">Content-driven</p>
            <p className="mt-2 text-sm">
              Concepts like <span className="font-semibold">variables</span> and <span className="font-semibold">loops</span> are
              defined in <code className="rounded bg-white/10 px-1">shared-data/day4_tutor_content.json</code>. Learn mode reads
              <code className="rounded bg-white/10 px-1">summary</code>, while quiz &amp; teach_back reuse
              <code className="rounded bg-white/10 px-1">sample_question</code>. Add more entries to expand the course.
            </p>
          </div>

          <Button
            variant="primary"
            size="lg"
            onClick={onStartCall}
            className="mt-2 w-full max-w-sm rounded-full bg-white/90 text-black hover:bg-white"
          >
            {startButtonText}
          </Button>
        </div>
      </section>

      <div className="pointer-events-none fixed bottom-5 left-0 flex w-full items-center justify-center">
        <p className="text-muted-foreground max-w-prose pt-1 text-xs leading-5 font-normal text-pretty md:text-sm">
          Need help getting set up? Check out the{' '}
          <a
            target="_blank"
            rel="noopener noreferrer"
            href="https://docs.livekit.io/agents/start/voice-ai/"
            className="underline"
          >
            Voice AI quickstart
          </a>
          .
        </p>
      </div>
    </div>
  );
};
