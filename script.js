// ==============================
// ADD GROUP MEMBER
// ==============================
function addMember() {

  // Get values from input fields
  let name = document.getElementById("name").value;
  let email = document.getElementById("email").value;
  let role = document.getElementById("role").value;

  // Send data to Flask backend
  fetch("http://127.0.0.1:5000/add_member", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },

    body: JSON.stringify({
      name: name,
      email: email,
      role: role,
      coursework_id: 1  // default link
    })
  })

  .then(res => res.json())
  .then(data => {
    alert(data.message); // show success message
  });
}


// ==============================
// ADD COURSEWORK
// ==============================
function addCoursework() {

  let title = document.getElementById("coursework").value;
  let deadline = document.getElementById("deadline").value;

  // Send to backend
  fetch("http://127.0.0.1:5000/add_coursework", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },

    body: JSON.stringify({
      title: title,
      due_date: deadline
    })
  })

  .then(res => res.json())
  .then(data => {
    alert(data.message);
    loadDashboard(); // refresh dashboard after adding
  });
}


// ==============================
// LOAD DASHBOARD FROM BACKEND
// ==============================
function loadDashboard() {

  fetch("http://127.0.0.1:5000/upcoming")
    .then(res => res.json())
    .then(data => {

      let dashboard = document.getElementById("dashboard");
      dashboard.innerHTML = ""; // clear old content

      // Loop through tasks
      data.forEach(cw => {

        let div = document.createElement("div");

        // highlight urgent tasks
        div.className = cw.days_left <= 3 ? "urgent" : "normal";

        // display content
        div.innerHTML = `
          <h3>${cw.title}</h3>
          <p>Deadline: ${cw.due_date}</p>
          <p>Days left: ${cw.days_left}</p>
        `;

        dashboard.appendChild(div);
      });
    });
}


// ==============================
// AUTO LOAD WHEN PAGE OPENS
// ==============================
window.onload = loadDashboard;