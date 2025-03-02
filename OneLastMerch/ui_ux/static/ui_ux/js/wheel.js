document.addEventListener("DOMContentLoaded", function () {
    const wheel = document.getElementById("wheel");
    const spinButton = document.getElementById("spin-btn");
    const resultMessage = document.getElementById("result-message");

    let prizes = [];

    // Fetch prize data from backend
    fetch("/spin-wheel/", { headers: { "X-Requested-With": "XMLHttpRequest" } })
        .then(response => {
            if (!response.ok) throw new Error("Network response was not ok");
            return response.json();
        })
        .then(data => {
            prizes = data.total_prizes;
            createWheel(prizes);
        })
        .catch(error => {
            console.error("Error fetching prizes:", error);
            resultMessage.innerHTML = "Failed to load prizes. Please try again.";
        });

    function createWheel(numPrizes) {
        const angle = 360 / numPrizes;
        wheel.innerHTML = ""; // Clear existing slices

        for (let i = 0; i < numPrizes; i++) {
            let slice = document.createElement("div");
            slice.classList.add("wheel-slice");
            slice.style.transform = `rotate(${i * angle}deg)`;
            wheel.appendChild(slice);
        }
    }

    function spinWheel() {
        if (prizes.length === 0) {
            resultMessage.innerHTML = "No prizes available. Please try again later.";
            return;
        }

        let randomDegree = Math.floor(Math.random() * 360) + 1800; // Random spin with extra rotations
        wheel.style.transition = "transform 4s ease-out";
        wheel.style.transform = `rotate(${randomDegree}deg)`;

        // Fetch random prize from backend
        fetch("/spin-wheel/", { headers: { "X-Requested-With": "XMLHttpRequest" } })
            .then(response => {
                if (!response.ok) throw new Error("Network response was not ok");
                return response.json();
            })
            .then(data => {
                setTimeout(() => {
                    resultMessage.innerHTML = `🎉 You won: <strong>${data.reward.text}</strong>`;
                }, 4000); // Delay until spin completes
            })
            .catch(error => {
                console.error("Error fetching reward:", error);
                resultMessage.innerHTML = "Failed to spin the wheel. Please try again.";
            });
    }

    spinButton.addEventListener("click", spinWheel);
});