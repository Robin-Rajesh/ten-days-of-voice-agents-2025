export interface AppConfig {
  pageTitle: string;
  pageDescription: string;
  companyName: string;

  supportsChatInput: boolean;
  supportsVideoInput: boolean;
  supportsScreenShare: boolean;
  isPreConnectBufferEnabled: boolean;

  logo: string;
  startButtonText: string;
  accent?: string;
  logoDark?: string;
  accentDark?: string;

  // for LiveKit Cloud Sandbox
  sandboxId?: string;
  agentName?: string;
}

export const APP_CONFIG_DEFAULTS: AppConfig = {
  companyName: 'Improv Battle',
  pageTitle: 'Improv Battle - Voice Game Show',
  pageDescription: 'Test your improv skills in this high-energy voice game show!',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '',  // No logo
  accent: '#dc2626',  // Red for game show energy
  logoDark: '',
  accentDark: '#ef4444',  // Brighter red for dark mode
  startButtonText: 'Start Improv Battle',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
