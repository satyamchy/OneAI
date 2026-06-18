// Converts an interaction mode into the display icon used across the UI.
export function modeIcon(mode) {
  return { chat: '💬', web_search: '🌐', tools: '🔧' }[mode] || '💬';
}
