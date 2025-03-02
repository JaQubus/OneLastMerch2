document.addEventListener('DOMContentLoaded', function () {
    const wheel = document.getElementById('wheel');
    const spinButton = document.getElementById('spin-btn');
    const resultMessage = document.getElementById('result-message');
    let isSpinning = false;

    // Retrieve all prize labels (optional if you need them in JS)
    const labels = document.querySelectorAll('.wheel-label');
    const segmentCount = labels.length;

    // If you want to create a dynamic conic gradient based on prize colors,
    // you might have an array of colors from the backend. For example:
    const colors = [
        '#ff9f43', '#feca57', '#ff6b6b', '#ee5253', '#54a0ff',
        '#2e86de', '#1dd1a1', '#10ac84', '#5f27cd', '#341f97'
    ];
    if (segmentCount > 0) {
        const gradientStops = [];
        const angleIncrement = 360 / segmentCount;
        for (let i = 0; i < segmentCount; i++) {
            const startAngle = angleIncrement * i;
            const endAngle = angleIncrement * (i + 1);
            const color = colors[i % colors.length];
            gradientStops.push(`${color} ${startAngle}deg ${endAngle}deg`);
        }
        wheel.style.background = `conic-gradient(${gradientStops.join(', ')})`;
    }

    // Handle spin button click via AJAX
    spinButton.addEventListener('click', function () {
        if (isSpinning) return;
        isSpinning = true;
        spinButton.disabled = true;
        resultMessage.textContent = '';

        fetch(spinWheelApiUrl, {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                resultMessage.textContent = data.error;
                spinButton.disabled = false;
                isSpinning = false;
            } else {
                const prizeIndex = data.prize_index;
                const totalRotation = 360 * 5;  // Five full spins for effect
                const rotationPerSegment = 360 / segmentCount;
                const targetRotation = rotationPerSegment * prizeIndex + rotationPerSegment / 2;
                const finalRotation = totalRotation + (360 - targetRotation);                

                wheel.style.transform = `rotate(${finalRotation}deg)`;
                wheel.style.transition = 'transform 3s ease-out';

                setTimeout(() => {
                    resultMessage.textContent = `You won: ${data.prize_name}`;
                    spinButton.disabled = false;
                    isSpinning = false;
                }, 3000);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            resultMessage.textContent = 'An error occurred. Please try again.';
            spinButton.disabled = false;
            isSpinning = false;
        });
    });

    // Utility function to retrieve CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
