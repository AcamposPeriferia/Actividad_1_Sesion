import { api } from "./api.js";

const currency = new Intl.NumberFormat("es-CO", {
  style: "currency",
  currency: "COP",
  maximumFractionDigits: 2,
});
const dateTime = new Intl.DateTimeFormat("es-CO", {
  dateStyle: "short",
  timeStyle: "medium",
});

const ACCOUNT_TYPE_LABELS = { PERSONAL: "Personal", CORPORATIVA: "Corporativa" };
const EVENT_LABELS = {
  TRANSFER_COMPLETED: "Completada",
  TRANSFER_REJECTED: "Rechazada",
};

const $ = (selector) => document.querySelector(selector);

function el(tag, { className, text } = {}, children = []) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  node.append(...children);
  return node;
}

function row(cells) {
  return el("tr", {}, cells.map(({ text, className }) => el("td", { text, className })));
}

function emptyRow(columns, message) {
  const cell = el("td", { className: "empty", text: message });
  cell.colSpan = columns;
  return el("tr", {}, [cell]);
}

// ---------- Render ----------

function renderAccounts(accounts) {
  $("#accounts").replaceChildren(
    ...accounts.map((account) =>
      el("article", { className: "account-card" }, [
        el("div", { className: "account-top" }, [
          el("span", { className: "account-id", text: account.account_id }),
          el("span", {
            className: `badge badge-${account.account_type.toLowerCase()}`,
            text: ACCOUNT_TYPE_LABELS[account.account_type] ?? account.account_type,
          }),
        ]),
        el("p", { className: "account-owner", text: account.owner }),
        el("p", { className: "account-balance", text: currency.format(account.balance) }),
      ]),
    ),
  );

  for (const select of [$("#from-account"), $("#to-account")]) {
    const previous = select.value;
    select.replaceChildren(
      ...accounts.map((account) => {
        const option = el("option", { text: `${account.account_id} · ${account.owner}` });
        option.value = account.account_id;
        return option;
      }),
    );
    if (previous) select.value = previous;
  }
  if (!$("#to-account").dataset.touched && accounts.length > 1) {
    $("#to-account").selectedIndex = 1;
  }
}

function renderTransfers(transfers) {
  const body = $("#transfers-body");
  if (transfers.length === 0) {
    body.replaceChildren(emptyRow(5, "Aún no hay transferencias."));
    return;
  }
  body.replaceChildren(
    ...transfers.map((t) =>
      row([
        { text: t.transfer_id, className: "mono" },
        { text: dateTime.format(new Date(t.created_at)) },
        { text: t.from_account },
        { text: t.to_account },
        { text: currency.format(t.amount), className: "num" },
      ]),
    ),
  );
}

function describeEvent(details) {
  const route = `${details.from_account} → ${details.to_account}`;
  const amount = typeof details.amount === "number" ? currency.format(details.amount) : details.amount;
  return details.reason ? `${route} · ${amount} · ${details.reason}` : `${route} · ${amount}`;
}

function renderAudit(events) {
  const body = $("#audit-body");
  if (events.length === 0) {
    body.replaceChildren(emptyRow(4, "Sin eventos registrados."));
    return;
  }
  body.replaceChildren(
    ...events.map((event) => {
      const tr = row([
        { text: event.event_id, className: "mono" },
        { text: dateTime.format(new Date(event.occurred_at)) },
        { text: "" },
        { text: describeEvent(event.details) },
      ]);
      const kind = event.event_type === "TRANSFER_REJECTED" ? "rejected" : "completed";
      tr.children[2].append(
        el("span", {
          className: `badge badge-${kind}`,
          text: EVENT_LABELS[event.event_type] ?? event.event_type,
        }),
      );
      return tr;
    }),
  );
}

function showFeedback(kind, message) {
  const box = $("#transfer-feedback");
  box.dataset.kind = kind;
  box.textContent = message;
  box.hidden = false;
}

function setApiStatus(online) {
  const pill = $("#api-status");
  pill.dataset.state = online ? "online" : "offline";
  pill.textContent = online ? "API conectada" : "API sin conexión";
}

// ---------- Data ----------

async function refresh() {
  try {
    const [accounts, transfers, events] = await Promise.all([
      api.listAccounts(),
      api.listTransfers(),
      api.listAuditEvents(),
    ]);
    renderAccounts(accounts);
    renderTransfers(transfers);
    renderAudit(events);
    setApiStatus(true);
  } catch (error) {
    setApiStatus(false);
    showFeedback("error", `No se pudo cargar la información: ${error.message}`);
  }
}

async function handleSubmit(event) {
  event.preventDefault();
  const amountValue = $("#amount").value.trim();
  if (amountValue === "") {
    showFeedback("error", "Ingresa el monto a transferir.");
    return;
  }

  const payload = {
    from_account: $("#from-account").value,
    to_account: $("#to-account").value,
    amount: Number(amountValue),
  };

  const button = $("#submit-button");
  button.disabled = true;
  button.textContent = "Procesando…";
  try {
    const result = await api.createTransfer(payload);
    showFeedback(
      "success",
      `Transferencia exitosa: ${currency.format(result.amount)} de ${result.from_account} a ${result.to_account}.`,
    );
    $("#amount").value = "";
  } catch (error) {
    showFeedback("error", error.message);
  } finally {
    button.disabled = false;
    button.textContent = "Transferir";
    await refresh();
  }
}

// ---------- Init ----------

$("#transfer-form").addEventListener("submit", handleSubmit);
$("#refresh-button").addEventListener("click", refresh);
$("#to-account").addEventListener("change", (e) => (e.target.dataset.touched = "true"));

api.health().then(() => setApiStatus(true), () => setApiStatus(false));
refresh();
