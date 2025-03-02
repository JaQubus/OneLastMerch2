document.addEventListener('DOMContentLoaded', function () {
    const wheel = document.getElementById('wheel');
    const spinButton = document.getElementById('spin-btn');
    const resultMessage = document.getElementById('result-message');
    let isSpinning = false;

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
                    const totalSegments = document.querySelectorAll('.wheel-segment').length;
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
            .catch(error => console.error('Error:', error));
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