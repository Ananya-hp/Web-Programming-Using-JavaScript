
document.getElementById("viewWorkBtn").addEventListener("click", function (e) {
    e.preventDefault();
    document.getElementById("projects").scrollIntoView({ behavior: "smooth" });
});


function highlightService(card) {
    const cards = document.querySelectorAll(".service-card");
    cards.forEach(c => c.classList.remove("active-service"));
    card.classList.add("active-service");
}
