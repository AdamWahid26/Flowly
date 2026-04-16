let members = [];
let courseworks = [];

// Add Member
function addMember() {
  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;
  let role = document.getElementById("role").value;

  members.push({ name, email, role });

  alert("Member added!");
}

// Add Coursework
function addCoursework() {
  let title = document.getElementById("coursework").value;
  let deadline = document.getElementById("deadline").value;

  courseworks.push({
    title,
    deadline,
    members: [...members] // link all members for now
  });

  displayDashboard();
}

// Display Dashboard
function displayDashboard() {
  let dashboard = document.getElementById("dashboard");
  dashboard.innerHTML = "";

  let today = new Date();

  courseworks.forEach(cw => {
    let dueDate = new Date(cw.deadline);
    let diffDays = (dueDate - today) / (1000 * 60 * 60 * 24);

    let div = document.createElement("div");

    // Highlight near deadline (3 days)
    if (diffDays <= 3) {
      div.classList.add("urgent");
    } else {
      div.classList.add("normal");
    }

    div.innerHTML = `
      <h3>${cw.title}</h3>
      <p>Deadline: ${cw.deadline}</p>
      <p>Members:</p>
      <ul>
        ${cw.members.map(m => `<li>${m.name} (${m.role})</li>`).join("")}
      </ul>
    `;

    dashboard.appendChild(div);
  });
}