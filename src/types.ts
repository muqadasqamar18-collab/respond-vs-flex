/**
 * Types for the Grant Proposal Classifier
 */

export type ProposalType = "Flex (Type 2)" | "Respond (Type 1)";

export interface ClassificationResult {
  filename: string;
  classification: string;
  type: "flex" | "respond" | "error";
  ai_powered: boolean;
}

export interface ClassifyResponse {
  results: ClassificationResult[];
}

export interface GeminiContentPart {
  text: string;
}

export interface GeminiCandidate {
  content: {
    parts: GeminiContentPart[];
  };
}

export interface GeminiApiResponse {
  candidates: GeminiCandidate[];
}
