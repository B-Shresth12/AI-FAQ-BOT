"use client";
const host: string = "http://192.168.1.161:8000";

interface Answer {
  answer: string;
}

export const chat = async (
  conversation_id: string,
  message: string,
): Promise<Answer> => {
  const res = await fetch(`${host}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      conversation_id,
      message,
    }),
  });

  if (!res.ok) {
    throw new Error(`Chat request failed: ${res.status} ${res.statusText}`);
  }

  const data: Answer = await res.json();
  return data;
};

// Get Message Action
interface Message {
  role: "user" | "assistant" | "system"; // or whatever your Role enum maps to
  content: string;
}

interface Messages {
  messages: Message[];
}

export const getMessagesofConversation = async (
  conversationId: string,
): Promise<Messages> => {
  const url = new URL(`${host}/get-message`);
  url.searchParams.set("conversation_id", conversationId);

  const res = await fetch(url);

  if (!res.ok) {
    throw new Error(`Failed to get Messages: ${res.status} ${res.statusText}`);
  }

  const data: Messages = await res.json();
  return data;
};

//Get Conversations
export interface ConversationSummary {
  id: string;
  created_at: string;
  updated_at: string;
}

interface ConversationsResponse {
  conversations: ConversationSummary[];
}

export const getConversations = async (): Promise<ConversationsResponse> => {
  const url = new URL(`${host}/get-conversations`);
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error(`Failed to get Conversations`);
  }

  const data: ConversationsResponse = await res.json();
  return data;
};
