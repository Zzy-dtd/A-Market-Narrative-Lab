const warning =
  "Note: This system is designed for educational analysis only and should not be interpreted as investment advice.";

const directRecommendationPatterns = [
  /\byou should buy\b/i,
  /\byou should sell\b/i,
  /\bstrong buy\b/i,
  /\bprice target\b/i,
  /\bguaranteed\b/i,
  /\brisk-free\b/i,
];

export function detectDirectRecommendation(response: string) {
  return directRecommendationPatterns.some((pattern) => pattern.test(response));
}

export function softenRecommendationLanguage(response: string) {
  if (detectDirectRecommendation(response) && !response.includes(warning)) {
    return `${response.trim()}\n\n${warning}`;
  }
  return response;
}
