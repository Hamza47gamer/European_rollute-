let isSpinning = false;
const canvas = document.getElementById("roulette-wheel");
const ctx = canvas.getContext("2d");
canvas.width = 400;
canvas.height = 400;

const numbers = [...Array(37).keys()]; // 0 to 36
const colors = ["green", "red", "black"];
const ball = document.getElementById("ball");

function drawWheel() {
    const arc = (2 * Math.PI) / 37;
    for (let i = 0; i < 37; i++) {
        ctx.beginPath();
        ctx.fillStyle = colors[i % colors.length];
        ctx.moveTo(200, 200);
        ctx.arc(200, 200, 200, i * arc, (i + 1) * arc);
        ctx.fill();
        ctx.closePath();
    }
}

function spinWheel() {
    if (isSpinning) return;
    isSpinning = true;
    ball.style.animation = "spin 5s linear";
    setTimeout(() => {
        fetch("/spin", { method: "POST" })
            .then((res) => res.json())
            .then((data) => {
                ball.style.animation = "none";
                updateHistory(data.history);
                alert(`Result: ${data.result}`);
                isSpinning = false;
            });
    }, 5000);
}

function updateHistory(history) {
    const historyEl = document.getElementById("previous-results");
    historyEl.innerHTML = "";
    history.forEach((num) => {
        const li = document.createElement("li");
        li.textContent = num;
        historyEl.appendChild(li);
    });
}

document.getElementById("spin-button").addEventListener("click", spinWheel);

drawWheel();
