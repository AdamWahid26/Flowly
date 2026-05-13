// SUBJECT SWITCHING

const subjectCards = document.querySelectorAll(".subject-card");

subjectCards.forEach(card => {

    card.addEventListener("click", () => {

        subjectCards.forEach(c => {
            c.classList.remove("active-subject");
        });

        card.classList.add("active-subject");

    });

});


// GENERATE NOTES BUTTON

function generateDummyNotes() {

    const notesArea = document.getElementById("notesArea");

    notesArea.value = `Generated AI Notes

1. Overview
These notes are generated from uploaded study material.

2. Key Points
- Important concepts summarized
- Cleaner explanation
- Easier revision

3. Summary
This system helps students revise faster using AI-generated notes.`;

}


// SAVE BUTTON

function saveNotes() {

    alert("Notes saved successfully.");

}


// COPY BUTTON

function copyNotes() {

    const notesArea = document.getElementById("notesArea");

    notesArea.select();

    document.execCommand("copy");

    alert("Notes copied.");

}


// CLEAR BUTTON

function clearNotes() {

    document.getElementById("notesArea").value = "";

}


// PROGRESS TRACKING

const checkboxes = document.querySelectorAll(".topic-check");

checkboxes.forEach(box => {

    box.addEventListener("change", updateProgress);

});

function updateProgress() {

    const total = checkboxes.length;

    const checked = document.querySelectorAll(".topic-check:checked").length;

    const percentage = Math.round((checked / total) * 100);

    document.getElementById("software-percent").textContent = percentage + "%";

    document.getElementById("software-bar").style.width = percentage + "%";

    document.getElementById("currentProgress").textContent = percentage + "%";

}

updateProgress();
function toggleMenu() {
  let menu = document.getElementById("menu");
  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

function goHome() {
  window.location.href = "dashboard.html";
}

function goWork() {
  window.location.href = "work.html";
}

function goGenerateQuiz() {
  window.location.href = "generatequiz.html";
}

function goProfile() {
  window.location.href = "profile.html";
}

function goSettings() {
  window.location.href = "settings.html";
}

function logout() {
  window.location.href = "login1.html";