// ===== NAVIGATION =====

function toggleMenu() {

    let menu = document.getElementById("menu");

    menu.style.display =
        menu.style.display === "block" ? "none" : "block";
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
}


// ===== GENERATE NOTES =====

function generateDummyNotes() {

    const notesArea = document.getElementById("notesArea");

    notesArea.value = `Software Security - Secure Coding

1. Overview
Secure coding is the practice of developing software while reducing vulnerabilities and security risks.

2. Key Concepts
- Validate user input properly
- Prevent SQL Injection attacks
- Use secure authentication methods
- Encrypt sensitive information
- Avoid exposing system errors

3. Example
If user input is not validated, attackers may inject malicious SQL commands into the database.

4. Summary
Secure coding improves system security and helps developers reduce risks before deployment.`;

}


// ===== SAVE NOTES =====

function saveNotes() {

    alert("Notes saved successfully.");

}


// ===== COPY NOTES =====

function copyNotes() {

    const notesArea = document.getElementById("notesArea");

    notesArea.select();

    document.execCommand("copy");

    alert("Notes copied.");

}


// ===== CLEAR NOTES =====

function clearNotes() {

    document.getElementById("notesArea").value = "";

}


// ===== PROGRESS TRACKING =====

const checkboxes = document.querySelectorAll(".topic-check");

checkboxes.forEach(box => {

    box.addEventListener("change", updateProgress);

});

function updateProgress() {

    const total = checkboxes.length;

    const checked =
        document.querySelectorAll(".topic-check:checked").length;

    const percentage =
        Math.round((checked / total) * 100);

    const percentText =
        document.getElementById("software-percent");

    const progressBar =
        document.getElementById("software-bar");

    const currentProgress =
        document.getElementById("currentProgress");

    if (percentText) {
        percentText.textContent = percentage + "%";
    }

    if (progressBar) {
        progressBar.style.width = percentage + "%";
    }

    if (currentProgress) {
        currentProgress.textContent = percentage + "%";
    }
}


// ===== INITIALIZE =====

updateProgress();