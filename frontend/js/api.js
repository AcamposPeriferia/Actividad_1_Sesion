// Cliente HTTP de la API de Mini Bank. Mismo origen: el backend sirve este front.

export class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

function errorMessage(body, status) {
  const detail = body?.detail;
  if (typeof detail === "string") return detail;
  // Errores de validación de FastAPI (422) llegan como lista.
  if (Array.isArray(detail)) return detail.map((item) => item.msg).join(" · ");
  return `Error inesperado (HTTP ${status})`;
}

async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const body = await response.json().catch(() => null);

  if (!response.ok) {
    throw new ApiError(errorMessage(body, response.status), response.status);
  }
  return body;
}

export const api = {
  health: () => request("/health"),
  listAccounts: () => request("/accounts"),
  listTransfers: () => request("/transfers"),
  listAuditEvents: () => request("/audit-events"),
  createTransfer: (payload) =>
    request("/transfers", { method: "POST", body: JSON.stringify(payload) }),
};
