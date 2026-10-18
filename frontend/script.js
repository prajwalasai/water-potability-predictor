const form = document.getElementById("form");
const box = document.getElementById("result");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const body = {
        ph: parseFloat(document.getElementById("ph").value),
        hardness: parseFloat(document.getElementById("hardness").value),
        solids: parseFloat(document.getElementById("solids").value),
        turbidity: parseFloat(document.getElementById("turbidity").value),
    };

    box.className = "";
    box.textContent = "Analyzing...";

    try {
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        if (!res.ok) throw new Error("Please check your values and try again.");

        const data = await res.json();

        box.className = data.result === "Potable" ? "good" : "bad";
        box.innerHTML =
            "<strong>" + data.result + "</strong>" +
            "<span>Model confidence: " + data.confidence + "%</span>" +
            "<small>" + data.disclaimer + "</small>";
    } catch (err) {
        box.className = "bad";
        box.textContent = err.message;
    }
});