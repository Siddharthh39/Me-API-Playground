// Use the actual API Gateway base URL (no {proxy+} placeholder or trailing slash).
// Example for a default stage HTTP API: https://zra3rtnbte.execute-api.ap-south-1.amazonaws.com
// If you have a named stage (e.g., "prod"), append it: https://...amazonaws.com/prod
const API_BASE_URL = "https://ktycpctozh.execute-api.ap-south-1.amazonaws.com";

let currentProfileName = "";
let skillChart;

function setStatus(message, isError = false) {
  const status = document.getElementById("status");
  status.textContent = message || "";
  status.className = isError ? "text-danger" : "text-muted";
}

function renderList(listEl, items, renderer) {
  listEl.innerHTML = "";
  items.forEach(item => {
    const li = document.createElement("li");
    li.className = "list-group-item";
    li.innerHTML = renderer(item);
    listEl.appendChild(li);
  });
}

async function loadProfile() {
  try {
    const nameInput = document.getElementById("profileNameInput").value.trim();
    currentProfileName = nameInput;

    let url = `${API_BASE_URL}/profile`;
    if (nameInput) url += `?name=${encodeURIComponent(nameInput)}`;

    setStatus("Loading profile...");
    const res = await fetch(url);
    if (!res.ok) {
      const detail = await res.text();
      setStatus(`Error ${res.status}: ${detail || "Profile not found"}`, true);
      return;
    }

    const data = await res.json();
    setStatus("");

    document.getElementById("profileName").textContent = `${data.name}`;
    document.getElementById("profileEmail").textContent = data.email ? `Email: ${data.email}` : "";
    document.getElementById("profileEducation").textContent = data.education ? `Education: ${data.education}` : "";
    document.getElementById("profileTag").textContent = data.name ? "Active" : "";

    const skillsWrap = document.getElementById("skills");
    skillsWrap.innerHTML = "";
    const skills = data.skills || [];
    document.getElementById("skillCount").textContent = skills.length;
    skills.forEach(s => {
      const pill = document.createElement("span");
      pill.className = "badge text-bg-light text-dark px-3 py-2";
      pill.textContent = s.name;
      skillsWrap.appendChild(pill);
    });
    renderSkillChart(skills);

    renderProjects(data.projects || []);

    renderWork(data.work || []);

    const links = [];
    if (data.links?.github) links.push({ label: "GitHub", url: data.links.github });
    if (data.links?.linkedin) links.push({ label: "LinkedIn", url: data.links.linkedin });
    if (data.links?.portfolio) links.push({ label: "Portfolio", url: data.links.portfolio });
    renderList(
      document.getElementById("links"),
      links,
      l => `<a href="${l.url}" target="_blank" rel="noopener">${l.label}</a>`
    );
  } catch (err) {
    setStatus(`Unexpected error: ${err.message}`, true);
  }
}

async function loadProjects(skill = "") {
  try {
    let url = `${API_BASE_URL}/projects`;
    const params = new URLSearchParams();
    if (currentProfileName) params.set("name", currentProfileName);
    if (skill) params.set("skill", skill);
    const qs = params.toString();
    if (qs) url += `?${qs}`;

    const res = await fetch(url);
    if (!res.ok) return;
    const projects = await res.json();

    renderProjects(projects || []);
  } catch (err) {
    setStatus(`Unexpected error: ${err.message}`, true);
  }
}

function search() {
  const skill = document.getElementById("searchInput").value.trim();
  loadProjects(skill);
}

function renderProjects(projects) {
  const container = document.getElementById("projects");
  container.innerHTML = "";
  projects.forEach(p => {
    const col = document.createElement("div");
    col.className = "col-12";
    col.innerHTML = `
      <div class="p-3 border rounded-3 bg-light h-100">
        <div class="d-flex justify-content-between align-items-center mb-1">
          <strong>${p.title}</strong>
          <span class="badge text-bg-secondary">Project</span>
        </div>
        <div class="text-muted small">${p.description || ""}</div>
      </div>
    `;
    container.appendChild(col);
  });
}

function renderWork(work) {
  const container = document.getElementById("work");
  container.innerHTML = "";
  if (!work.length) {
    container.innerHTML = '<div class="text-muted">No work experience listed.</div>';
    return;
  }
  work.forEach(w => {
    const item = document.createElement("div");
    item.className = "mb-3 ps-3 border-start border-2";
    item.innerHTML = `
      <div class="fw-semibold">${w.role} @ ${w.company}</div>
      <div class="text-muted small">${w.duration || ""}</div>
      <div class="small">${w.description || ""}</div>
    `;
    container.appendChild(item);
  });
}

function renderSkillChart(skills) {
  const labels = skills.map(s => s.name);
  const values = skills.map((_, idx) => Math.max(30, 100 - idx * 10));

  const ctx = document.getElementById("skillChart");
  if (!ctx) return;
  if (skillChart) {
    skillChart.destroy();
  }
  skillChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [
        {
          label: "Strength",
          data: values,
          backgroundColor: "rgba(255, 193, 7, 0.6)",
          borderColor: "rgba(255, 193, 7, 1)",
          borderWidth: 1,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: {
          beginAtZero: true,
          max: 110,
          ticks: { stepSize: 20 },
          grid: { color: "rgba(0,0,0,0.05)" },
        },
        x: {
          grid: { display: false },
        },
      },
      plugins: {
        legend: { display: false },
      },
    },
  });
}

// Initial load uses first profile
loadProfile();
