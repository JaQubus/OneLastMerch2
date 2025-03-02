document.addEventListener('DOMContentLoaded', function () {
    const wheel = document.getElementById('wheel');
    const spinButton = document.getElementById('spin-btn');
    const resultMessage = document.getElementById('result-message');
    let isSpinning = false;

    // Get all the segments and calculate the angle for each segment
    const segments = document.querySelectorAll('.wheel-segment');
    const segmentCount = segments.length;

    if (segmentCount > 0) {
        const colors = [
            '#ff9f43', '#feca57', '#ff6b6b', '#ee5253', '#54a0ff', '#2e86de', '#1dd1a1', '#10ac84', '#5f27cd', '#341f97'
        ]; // Color array for segments
        const gradientStops = [];
        const angleIncrement = 360 / segmentCount;

        // Create a dynamic conic gradient for the wheel segments
        for (let i = 0; i < segmentCount; i++) {
            const startAngle = angleIncrement * i;
            const endAngle = angleIncrement * (i + 1);
            const color = colors[i % colors.length]; // Cycle through colors if there are more segments than colors
            gradientStops.push(`${color} ${startAngle}deg ${endAngle}deg`);
        }

        wheel.style.background = `conic-gradient(${gradientStops.join(', ')})`;
    }

    // Rotate the segment content and position it correctly
    const segmentAngle = 360 / segmentCount;
    segments.forEach((segment, index) => {
        const content = segment.querySelector('.segment-content');
        if (content) {
            const rotation = (index * segmentAngle) + (segmentAngle / 2);  // Adjust rotation for proper alignment
            content.style.transform = `translate(-50%, -50%) rotate(${rotation}deg)`; // Rotate the content to keep the text upright
        }
    });

    // Handle spin button click
    spinButton.addEventListener('click', function () {
        if (isSpinning) return;
        isSpinning = true;
        spinButton.disabled = true;

        // Fetch the spin result from the backend
        fetch('/spin-wheel-api/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),  // Include CSRF token
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultMessage.textContent = data.error;
                    spinButton.disabled = false;
                    isSpinning = false;
                } else {
                    // Calculate the spin animation degrees
                    const prizeIndex = data.prize_index;
                    const totalSegments = segments.length;
                    const degrees = 360 * 5 + (360 / totalSegments) * prizeIndex;  // Spin animation

                    // Apply the spin animation
                    wheel.style.transform = `rotate(${degrees}deg)`;
                    wheel.style.transition = 'transform 3s ease-out';

                    // Display the result after the spin animation ends
                    setTimeout(() => {
                        resultMessage.textContent = `You won: ${data.prize_name}`;
                        spinButton.disabled = true;  // Disable button after spin
                        isSpinning = false;
                    }, 3000);  // Match animation duration
                }
            })
            .catch(error => {
                console.error('Error:', error);
                resultMessage.textContent = 'An error occurred. Please try again.';
                spinButton.disabled = false;
                isSpinning = false;
            });
    });

    // Function to get CSRF token from cookies
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
