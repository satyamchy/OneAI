import api from './axios.js';

// Lists all messages for a conversation.
export function listMessages(conversationId) {
  return api.get(`/conversations/${conversationId}/messages`).then((response) => response.data);
}

// Parses buffered Server-Sent Events and forwards them to the caller.
function parseBufferedEvents(buffer, onEvent) {
  const events = buffer.split('\n\n');
  const pending = events.pop() || '';
  events.forEach((raw) => {
    const event = raw.split('\n').find((line) => line.startsWith('event:'))?.replace('event:', '').trim();
    const dataLine = raw.split('\n').find((line) => line.startsWith('data:'));
    if (event && dataLine) {
      onEvent(event, JSON.parse(dataLine.replace('data:', '').trim()));
    }
  });
  return pending;
}

// Streams a message through Axios progress events so all API calls use Axios.
export async function streamMessage(conversationId, payload, onEvent) {
  let parsedLength = 0;
  let pending = '';

  await api.post(`/conversations/${conversationId}/messages/stream`, payload, {
    responseType: 'text',
    onDownloadProgress: (progressEvent) => {
      const responseText = progressEvent.event?.target?.responseText || progressEvent.currentTarget?.responseText || '';
      const chunk = responseText.slice(parsedLength);
      parsedLength = responseText.length;
      pending = parseBufferedEvents(pending + chunk, onEvent);
    },
  });

  if (pending.trim()) {
    parseBufferedEvents(`${pending}\n\n`, onEvent);
  }
}
