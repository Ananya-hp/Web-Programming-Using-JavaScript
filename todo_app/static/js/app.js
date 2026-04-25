// Student Name:
// Roll No:
// Assignment 4 - Flask Powered Dynamic To-Do List Application
// Date:

let taskStore = [];
let currentFilter = "all";

document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("add-task-btn").addEventListener("click", addTask);
    document.getElementById("clear-all-btn").addEventListener("click", clearAllTasks);

    document.querySelectorAll(".filter-btn").forEach(btn => {
        btn.addEventListener("click", () => filterTasks(btn.dataset.filter));
    });

    loadFromLocalStorage();
});

async function loadTasks(status = "all") {
    try {
        let url = "/api/tasks";
        if (status !== "all") url += `?status=${status}`;

        const response = await fetch(url);
        if (!response.ok) throw new Error("Failed to fetch tasks");

        taskStore = await response.json();
        renderTasks(taskStore);
        updateCounter();
        saveToLocalStorage();
    } catch (error) {
        showError(error.message);
    }
}

function loadFromLocalStorage() {
    const saved = localStorage.getItem("tasks");
    if (saved) {
        taskStore = JSON.parse(saved);
        renderTasks(taskStore);
        updateCounter();
    } else {
        loadTasks();
    }
}

function saveToLocalStorage() {
    localStorage.setItem("tasks", JSON.stringify(taskStore));
}

function renderTasks(tasks) {
    const taskList = document.getElementById("task-list");
    taskList.innerHTML = "";

    if (!tasks.length) {
        taskList.innerHTML = `<p class="empty-state">No tasks yet! Add your first task above.</p>`;
        return;
    }

    tasks.forEach(task => {
        const card = document.createElement("div");
        card.className = `task-card priority-${task.priority} ${task.completed ? "completed" : ""}`;
        card.dataset.id = task.id;
        card.draggable = true;

        card.innerHTML = `
            <div class="task-top">
                <input type="checkbox" ${task.completed ? "checked" : ""} onchange="toggleTask(${task.id})">
                <div class="task-content">
                    <h3>${task.title}</h3>
                    <p>${task.description}</p>
                    <small>${task.created_at}</small>
                </div>
                <span class="badge priority-badge priority-${task.priority}">${task.priority}</span>
            </div>
            <div class="task-actions">
                <button onclick="editTask(${task.id})">Edit</button>
                <button onclick="deleteTask(${task.id})" class="delete-btn">Delete</button>
            </div>
        `;

        addDragEvents(card);
        taskList.appendChild(card);
    });
}

async function addTask() {
    const title = document.getElementById("task-title").value.trim();
    const description = document.getElementById("task-desc").value.trim();
    const priority = document.getElementById("task-priority").value;
    const error = document.getElementById("error-message");

    if (!title) {
        error.textContent = "Title is required.";
        return;
    }

    error.textContent = "";

    try {
        const response = await fetch("/api/tasks", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ title, description, priority })
        });

        if (!response.ok) throw new Error("Failed to add task");

        document.getElementById("task-title").value = "";
        document.getElementById("task-desc").value = "";
        document.getElementById("task-priority").value = "medium";

        await loadTasks(currentFilter);
    } catch (error) {
        showError(error.message);
    }
}

async function deleteTask(id) {
    try {
        const response = await fetch(`/api/tasks/${id}`, { method: "DELETE" });
        if (!response.ok) throw new Error("Failed to delete task");

        taskStore = taskStore.filter(task => task.id !== id);
        renderTasks(taskStore);
        updateCounter();
        saveToLocalStorage();
    } catch (error) {
        showError(error.message);
    }
}

async function toggleTask(id) {
    try {
        const response = await fetch(`/api/tasks/${id}/toggle`, { method: "PATCH" });
        if (!response.ok) throw new Error("Failed to toggle task");

        await loadTasks(currentFilter);
    } catch (error) {
        showError(error.message);
    }
}

function editTask(id) {
    const card = document.querySelector(`[data-id='${id}']`);
    const task = taskStore.find(t => t.id === id);

    card.innerHTML = `
        <div class="edit-mode">
            <input type="text" id="edit-title-${id}" value="${task.title}">
            <textarea id="edit-desc-${id}">${task.description}</textarea>
            <select id="edit-priority-${id}">
                <option value="low" ${task.priority === "low" ? "selected" : ""}>Low</option>
                <option value="medium" ${task.priority === "medium" ? "selected" : ""}>Medium</option>
                <option value="high" ${task.priority === "high" ? "selected" : ""}>High</option>
            </select>
            <div class="task-actions">
                <button onclick="saveTask(${id})">Save</button>
                <button onclick="renderTasks(taskStore)">Cancel</button>
            </div>
        </div>
    `;
}

async function saveTask(id) {
    const title = document.getElementById(`edit-title-${id}`).value.trim();
    const description = document.getElementById(`edit-desc-${id}`).value.trim();
    const priority = document.getElementById(`edit-priority-${id}`).value;

    try {
        const response = await fetch(`/api/tasks/${id}`, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ title, description, priority })
        });

        if (!response.ok) throw new Error("Failed to update task");

        await loadTasks(currentFilter);
    } catch (error) {
        showError(error.message);
    }
}

function filterTasks(status) {
    currentFilter = status;

    document.querySelectorAll(".filter-btn").forEach(btn => btn.classList.remove("active"));
    document.querySelector(`[data-filter='${status}']`).classList.add("active");

    loadTasks(status);
}

function updateCounter() {
    const total = taskStore.length;
    const completed = taskStore.filter(task => task.completed).length;
    const active = total - completed;

    document.getElementById("total-count").textContent = total;
    document.getElementById("active-count").textContent = active;
    document.getElementById("completed-count").textContent = completed;
    document.getElementById("nav-task-count").textContent = total;
}

function showError(message) {
    document.getElementById("error-message").textContent = message;
}

async function clearAllTasks() {
    if (!confirm("Are you sure you want to clear all tasks?")) return;

    try {
        await fetch("/api/tasks", { method: "DELETE" });
        taskStore = [];
        renderTasks(taskStore);
        updateCounter();
        saveToLocalStorage();
    } catch (error) {
        showError(error.message);
    }
}

function addDragEvents(card) {
    card.addEventListener("dragstart", () => card.classList.add("dragging"));
    card.addEventListener("dragend", () => {
        card.classList.remove("dragging");
        saveToLocalStorage();
    });

    card.addEventListener("dragover", e => e.preventDefault());

    card.addEventListener("drop", e => {
        e.preventDefault();
        const dragging = document.querySelector(".dragging");
        if (dragging && dragging !== card) {
            card.parentNode.insertBefore(dragging, card);
        }
    });
}