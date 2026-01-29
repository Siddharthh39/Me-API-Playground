const API_BASE_URL = "http://127.0.0.1:8000"; 

async function loadProfile() {
  const res = await fetch(`${API_BASE_URL}/profile`);
  const data = await res.json();

  document.getElementById("profile").innerText =
    `${data.name} | ${data.education}`;
}

async function loadProjects(skill = "") {
  let url = `${API_BASE_URL}/projects`;
  if (skill) url += `?skill=${skill}`;

  const res = await fetch(url);
  const projects = await res.json();

  const list = document.getElementById("projects");
  list.innerHTML = "";

  projects.forEach(p => {
    const li = document.createElement("li");
    li.className = "list-group-item";
    li.innerHTML = `<strong>${p.title}</strong><br>${p.description}`;
    list.appendChild(li);
  });
}

function search() {
  const skill = document.getElementById("searchInput").value;
  loadProjects(skill);
}

loadProfile();
loadProjects();
