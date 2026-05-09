let editingId = null;
let activeFilter = "";

const $ = id => document.getElementById(id);

async function api(path, method = "GET", body = null) {
  const opts = { method, headers: { "Content-Type": "application/json" } };
  if (body) opts.body = JSON.stringify(body);
  const res = await fetch(path, opts);
  return res.json();
}

async function loadTasks() {
  const url = activeFilter ? `/api/tasks?status=${activeFilter}` : "/api/tasks";
  const tasks = await api(url);
  renderBoard(tasks);
  await loadStats();
}

async function loadStats() {
  const s = await api("/api/stats");
  $("statTotal").textContent = s.total;
  $("statTodo").textContent = s.todo;
  $("statProgress").textContent = s.in_progress;
  $("statDone").textContent = s.done;
}

function renderBoard(tasks) {
  ["todo", "in_progress", "done"].forEach(status => {
    $(`tasks-${status}`).innerHTML = "";
  });

  if (tasks.length === 0) {
    $("emptyState").style.display = "block";
    $("board").style.display = "none";
    return;
  }
  $("emptyState").style.display = "none";
  $("board").style.display = "grid";

  tasks.forEach(task => {
    const col = $(`tasks-${task.status}`);
    if (!col) return;
    col.appendChild(createCard(task));
  });
}

function createCard(task) {
  const card = document.createElement("div");
  card.className = `task-card ${task.status}`;
  card.dataset.id = task.id;

  const due = task.due_date ? formatDue(task.due_date) : "";
  const isOverdue = task.due_date && new Date(task.due_date) < new Date() && task.status !== "done";

  card.innerHTML = `
    <div class="task-top">
      <div class="task-title">${escHtml(task.title)}</div>
      <span class="priority-badge priority-${task.priority}">${task.priority}</span>
    </div>
    ${task.description ? `<div class="task-desc">${escHtml(task.description)}</div>` : ""}
    <div class="task-footer">
      <span class="task-due ${isOverdue ? "overdue" : ""}">${due}</span>
      <div class="task-actions">
        <button class="task-btn" onclick="openEdit(${task.id}, event)">Edit</button>
        <button class="task-btn delete" onclick="deleteTask(${task.id}, event)">Delete</button>
      </div>
    </div>
  `;
  return card;
}

function formatDue(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" });
}

function escHtml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

async function openEdit(id, e) {
  e && e.stopPropagation();
  const task = await api(`/api/tasks/${id}`);
  editingId = id;
  $("modalTitle").textContent = "Edit Task";
  $("taskTitle").value = task.title;
  $("taskDesc").value = task.description || "";
  $("taskPriority").value = task.priority;
  $("taskDue").value = task.due_date || "";
  $("taskStatus").value = task.status;
  $("statusGroup").style.display = "block";
  openModal();
}

async function deleteTask(id, e) {
  e && e.stopPropagation();
  if (!confirm("Delete this task?")) return;
  await api(`/api/tasks/${id}`, "DELETE");
  loadTasks();
}

function openModal() {
  $("modalOverlay").classList.add("open");
  $("taskTitle").focus();
}

function closeModal() {
  $("modalOverlay").classList.remove("open");
  resetForm();
}

function resetForm() {
  editingId = null;
  $("modalTitle").textContent = "New Task";
  $("taskTitle").value = "";
  $("taskDesc").value = "";
  $("taskPriority").value = "medium";
  $("taskDue").value = "";
  $("taskStatus").value = "todo";
  $("statusGroup").style.display = "none";
}

$("openModal").addEventListener("click", () => { resetForm(); openModal(); });
$("closeModal").addEventListener("click", closeModal);
$("modalOverlay").addEventListener("click", e => { if (e.target === $("modalOverlay")) closeModal(); });

$("saveTask").addEventListener("click", async () => {
  const title = $("taskTitle").value.trim();
  if (!title) { $("taskTitle").style.borderColor = "var(--high)"; return; }
  $("taskTitle").style.borderColor = "";

  const payload = {
    title,
    description: $("taskDesc").value.trim(),
    priority: $("taskPriority").value,
    due_date: $("taskDue").value,
    status: $("taskStatus").value,
  };

  if (editingId) {
    await api(`/api/tasks/${editingId}`, "PUT", payload);
  } else {
    await api("/api/tasks", "POST", payload);
  }
  closeModal();
  loadTasks();
});

document.querySelectorAll(".filter-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".filter-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    activeFilter = btn.dataset.status;
    loadTasks();
  });
});

document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeModal();
});

loadTasks();
