const form = document.getElementById("form");
const box = document.getElementById("result");
const predictBtn = document.getElementById("predictBtn");

const FIELDS = [
    "ph", "hardness", "solids", "chloramines", "sulfate",
    "conductivity", "organic_carbon", "trihalomethanes", "turbidity",
];

document.getElementById("clearBtn").addEventListener("click", () => {
    form.reset();
    box.className = "result hidden";
    box.innerHTML = "";
});

function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
}

function showResult(data) {
    const isGood = data.result === "Potable";
    box.innerHTML = "";
    box.className = "result " + (isGood ? "good" : "bad");

    const head = el("div", "result-head");
    head.appendChild(el("div", "result-icon", isGood ? "✅" : "❌"));

    const titles = el("div");
    titles.appendChild(el("div", "result-title", data.result));
    titles.appendChild(el(
        "div", "result-sub",
        isGood ? "Values look acceptable for drinking."
            : "This water may not be suitable for drinking."
    ));
    head.appendChild(titles);
    box.appendChild(head);

    const meta = el("div", "meta");
    if (data.confidence !== null && data.confidence !== undefined) {
        meta.appendChild(el("span", "pill", "Confidence: " + data.confidence + "%"));
    }
    meta.appendChild(el("span", "pill", "Decided by: " + data.method));
    box.appendChild(meta);

    if (data.reasons && data.reasons.length > 0) {
        const list = el("ul", "reasons");
        data.reasons.forEach((r) => list.appendChild(el("li", "", r)));
        box.appendChild(list);
    }

    box.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function showError(message) {
    box.innerHTML = "";
    box.className = "result bad";
    box.appendChild(el("div", "result-title", "Something went wrong"));
    box.appendChild(el("div", "result-sub", message));
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const body = {};
    FIELDS.forEach((id) => {
        body[id] = parseFloat(document.getElementById(id).value);
    });

    box.className = "result loading";
    box.textContent = "Analyzing your water values...";
    predictBtn.disabled = true;
    predictBtn.textContent = "Checking...";

    try {
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
        });

        if (!res.ok) throw new Error("Please check your values and try again.");

        showResult(await res.json());
    } catch (err) {
        showError(err.message);
    } finally {
        predictBtn.disabled = false;
        predictBtn.textContent = "Check water";
    }
});