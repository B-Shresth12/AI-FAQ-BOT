"use client";

interface Answer {
  answer: string;
}

export const chat = async (
  conversation_id: string,
  message: string,
): Promise<Answer> => {
  const res = await fetch("http://192.168.1.161:8000/chat", {
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
