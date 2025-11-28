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
  companyName: 'Stranger Things',
  pageTitle: 'Stranger Things Game Master',
  pageDescription: 'A D&D-style voice adventure set in Hawkins, 1985',

  supportsChatInput: true,
  supportsVideoInput: false,
  supportsScreenShare: false,
  isPreConnectBufferEnabled: true,

  logo: '/Stranger_Things_logo.png',
  accent: '#cc0000',  // Stranger Things red
  logoDark: '/Stranger_Things_logo.png',
  accentDark: '#ff0000',  // Brighter red for dark mode
  startButtonText: 'Enter the Upside Down',

  // for LiveKit Cloud Sandbox
  sandboxId: undefined,
  agentName: undefined,
};
