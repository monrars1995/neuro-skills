import {
  CopilotRuntime,
  GoogleGenerativeAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";

function buildServiceAdapter() {
  return new GoogleGenerativeAIAdapter({
    apiKey: process.env.GOOGLE_API_KEY,
    apiVersion: "v1",
    model: (process.env.GOOGLE_MODEL || "google/gemini-2.5-pro").replace("google/", ""),
  });
}

const runtime = new CopilotRuntime();
const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
  runtime,
  serviceAdapter: buildServiceAdapter(),
  endpoint: "/api/copilotkit",
});

export async function GET(request: Request) {
  return handleRequest(request);
}

export async function POST(request: Request) {
  return handleRequest(request);
}
