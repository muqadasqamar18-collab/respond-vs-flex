/**
 * Grant Proposal Classifier - TypeScript/Deno implementation
 *
 * Classifies grant proposal documents as either "Flex (Type 2)" or "Respond (Type 1)"
 * using heuristic rules and optional Gemini AI classification.
 */

import type { GeminiApiResponse, ProposalType } from "./types.ts";

/** Type guard that validates the shape of a Gemini API response. */
function isGeminiApiResponse(value: unknown): value is GeminiApiResponse {
  if (value === null || typeof value !== "object") return false;
  const obj = value as Record<string, unknown>;
  if (!Array.isArray(obj["candidates"])) return false;
  for (const candidate of obj["candidates"] as unknown[]) {
    if (candidate === null || typeof candidate !== "object") return false;
    const c = candidate as Record<string, unknown>;
    if (c["content"] === null || typeof c["content"] !== "object") return false;
    const content = c["content"] as Record<string, unknown>;
    if (!Array.isArray(content["parts"])) return false;
    for (const part of content["parts"] as unknown[]) {
      if (part === null || typeof part !== "object") return false;
      if (typeof (part as Record<string, unknown>)["text"] !== "string") {
        return false;
      }
    }
  }
  return true;
}

/**
 * Classify text using the Gemini AI API.
 * Returns null if the API key is not set or if an error occurs.
 */
export async function classifyWithGemini(
  text: string,
): Promise<ProposalType | null> {
  const apiKey = Deno.env.get("GEMINI_API_KEY");
  if (!apiKey) {
    return null;
  }

  const prompt =
    "You are an expert grant proposal classifier. " +
    "Classify the following document text as either 'Flex (Type 2)' or 'Respond (Type 1)'. " +
    "If the document contains 'Request for Proposal', 'RFP', 'Questions', 'Guidelines', or 'Narrative', it is likely 'Flex (Type 2)'. " +
    "If the document is a 'Form', 'Template', 'Checklist', or 'Application Form' to be filled out, it is likely 'Respond (Type 1)'. " +
    "Return ONLY the classification string: 'Flex (Type 2)' or 'Respond (Type 1)'." +
    "\n\nDocument Text:\n" +
    text.slice(0, 10000);

  try {
    const url =
      `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`;
    const response = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }],
      }),
    });

    if (!response.ok) {
      return null;
    }

    const data: unknown = await response.json();
    if (!isGeminiApiResponse(data) || data.candidates.length === 0) {
      return null;
    }

    const parts = data.candidates[0].content.parts;
    if (parts.length === 0) {
      return null;
    }

    const result = parts[0].text.trim();
    if (result === "Flex (Type 2)" || result === "Respond (Type 1)") {
      return result;
    }
    return null;
  } catch (error: unknown) {
    if (error instanceof Error) {
      console.error("Gemini API error:", error.message);
    }
    return null;
  }
}

/**
 * Classify a proposal document by its filename and text content using heuristic rules.
 */
export function classifyByHeuristics(
  filename: string,
  text: string,
): ProposalType {
  const nameLower = filename.toLowerCase();
  const textLower = text.toLowerCase();

  let scoreRespond = 0;
  let scoreFlex = 0;

  // 1. Filename Analysis
  if (nameLower.includes("template")) scoreRespond += 3;
  if (nameLower.includes("form")) scoreRespond += 2;
  if (nameLower.includes("checklist")) scoreRespond += 2;
  if (nameLower.includes("chapter")) scoreRespond += 2;
  if (nameLower.includes("appendix")) scoreRespond += 2;

  if (nameLower.includes("rfp")) scoreFlex += 3;
  if (nameLower.includes("question")) scoreFlex += 3;
  if (nameLower.includes("guidelines")) scoreFlex += 2;
  if (nameLower.includes("narrative")) scoreFlex += 2;

  // 2. Content Analysis

  // FLEX Indicators
  if (textLower.includes("character limit")) scoreFlex += 3;
  if (textLower.includes("request for proposal")) scoreFlex += 2;
  if (
    textLower.includes("project overview") &&
    textLower.includes("project name*")
  ) {
    scoreFlex += 3;
  }
  if (textLower.includes("collaborate feature")) scoreFlex += 2;

  // RESPOND Indicators
  if (textLower.includes("application form")) scoreRespond += 1;
  if (textLower.includes("please note that a session will time out")) {
    scoreRespond += 2;
  }
  if (textLower.includes("application template")) scoreRespond += 3;
  if (textLower.includes("chapter 3:") || textLower.includes("chapter 2:")) {
    scoreRespond += 2;
  }

  if (
    textLower.includes("grant guidelines") &&
    !nameLower.includes("guidelines")
  ) {
    scoreFlex += 1;
  }

  // Length/Structure Heuristics
  const underscoreMatches = textLower.match(/___/g);
  if (underscoreMatches && underscoreMatches.length > 10) scoreRespond += 1;

  // Conflict Resolution
  if (scoreFlex > scoreRespond) {
    return "Flex (Type 2)";
  } else if (scoreRespond > scoreFlex) {
    return "Respond (Type 1)";
  } else {
    if (
      nameLower.includes("question") ||
      nameLower.includes("rfp")
    ) {
      return "Flex (Type 2)";
    }
    return "Respond (Type 1)";
  }
}

/**
 * Classify a proposal given its filename and text content.
 * Tries Gemini AI first, then falls back to heuristic rules.
 */
export async function classifyProposal(
  filename: string,
  text: string,
): Promise<ProposalType> {
  const geminiResult = await classifyWithGemini(text);
  if (geminiResult !== null) {
    return geminiResult;
  }

  return classifyByHeuristics(filename, text);
}
