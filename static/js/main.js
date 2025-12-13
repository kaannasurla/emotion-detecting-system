// Variabile globale
let chart = null;
let autoUpdateInterval = null;
let currentEmotion = 'neutral';

// Inițializare la încărcarea paginii
document.addEventListener('DOMContentLoaded', function() {
    initializeChart();
    startAutoUpdate();
});

// Actualizează emoția detectată
async function updateEmotion() {
    try {
        const response = await fetch('/get_emotion');
        const data = await response.json();
        
        if (data.error) {
            showMessage('Eroare: ' + data.error, 'error');
            return;
        }
        
        currentEmotion = data.emotion;
        
        // Actualizează interfața
        document.getElementById('emojiDisplay').textContent = data.emoji;
        document.getElementById('emotionName').textContent = capitalizeFirst(data.emotion);
        
        // Actualizează bara de încredere
        const confidence = Math.round(data.confidence * 100);
        document.getElementById('confidenceFill').style.width = confidence + '%';
        document.getElementById('confidenceText').textContent = `Încredere: ${confidence}%`;
        
        // Schimbă culoarea în funcție de emoție
        updateEmotionColors(data.emotion);
        
        // Redă sunetul specific
        playEmotionSound(data.emotion);
        
        // Actualizează graficul
        updateChart();
        
    } catch (error) {
        console.error('Eroare la detectarea emoției:', error);
        showMessage('Eroare la conectarea cu serverul', 'error');
    }
}

// Actualizare automată periodică
function startAutoUpdate() {
    autoUpdateInterval = setInterval(() => {
        updateEmotion();
    }, 2000); // Actualizează la fiecare 2 secunde
}

function stopAutoUpdate() {
    if (autoUpdateInterval) {
        clearInterval(autoUpdateInterval);
        autoUpdateInterval = null;
    }
}

// Schimbă categoria de emoji
async function changeCategory(category) {
    try {
        const response = await fetch('/change_category', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category: category })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(`Categorie schimbată: ${capitalizeFirst(category)}`, 'success');
            
            // Actualizează emoji-ul curent
            const emojiResponse = await fetch(`/get_emoji/${category}`);
            const emojiData = await emojiResponse.json();
            document.getElementById('emojiDisplay').textContent = emojiData.emoji;
        }
    } catch (error) {
        console.error('Eroare la schimbarea categoriei:', error);
        showMessage('Eroare la schimbarea categoriei', 'error');
    }
}

// Salvează captură
async function saveCapture() {
    try {
        const response = await fetch('/save_capture', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage(`Captură salvată: ${data.filename}`, 'success');
        } else {
            showMessage('Eroare la salvarea capturii', 'error');
        }
    } catch (error) {
        console.error('Eroare la salvarea capturii:', error);
        showMessage('Eroare la salvarea capturii', 'error');
    }
}

// Toggle pentru afișarea istoricului
function toggleHistory() {
    const historySection = document.getElementById('historySection');
    if (historySection.style.display === 'none') {
        historySection.style.display = 'block';
        updateChart();
    } else {
        historySection.style.display = 'none';
    }
}

// Șterge istoricul
async function clearHistory() {
    if (!confirm('Sigur doriți să ștergeți istoricul?')) {
        return;
    }
    
    try {
        const response = await fetch('/clear_history', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showMessage('Istoric șters cu succes', 'success');
            if (chart) {
                chart.data.labels = [];
                chart.data.datasets[0].data = [];
                chart.update();
            }
        }
    } catch (error) {
        console.error('Eroare la ștergerea istoricului:', error);
        showMessage('Eroare la ștergerea istoricului', 'error');
    }
}

// Inițializează graficul
function initializeChart() {
    const ctx = document.getElementById('emotionChart');
    if (!ctx) return;
    
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [{
                label: 'Încredere (%)',
                data: [],
                borderColor: 'rgb(102, 126, 234)',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                tension: 0.4,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: true,
                    position: 'top'
                },
                title: {
                    display: true,
                    text: 'Evoluția Emoțiilor în Timp'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });
}

// Actualizează graficul cu date noi
async function updateChart() {
    if (!chart) return;
    
    try {
        const response = await fetch('/get_history');
        const data = await response.json();
        
        if (data.history && data.history.length > 0) {
            const labels = data.history.map((item, index) => `#${index + 1}`);
            const values = data.history.map(item => Math.round(item.confidence * 100));
            
            chart.data.labels = labels;
            chart.data.datasets[0].data = values;
            chart.update();
        }
    } catch (error) {
        console.error('Eroare la actualizarea graficului:', error);
    }
}

// Actualizează culorile în funcție de emoție
function updateEmotionColors(emotion) {
    const emotionCard = document.querySelector('.emotion-card');
    const gradients = {
        'happy': 'linear-gradient(135deg, #f6d365 0%, #fda085 100%)',
        'sad': 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
        'angry': 'linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%)',
        'surprise': 'linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 100%)',
        'neutral': 'linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%)'
    };
    
    emotionCard.style.background = gradients[emotion] || gradients['neutral'];
}

// Redă sunetul specific emoției
function playEmotionSound(emotion) {
    const audio = new Audio(`/static/sounds/${emotion}.mp3`);
    audio.volume = 0.3;
    audio.play().catch(error => {
        console.log('Nu s-a putut reda sunetul:', error);
    });
}

// Afișează mesaje de status
function showMessage(message, type) {
    const statusMessage = document.getElementById('statusMessage');
    statusMessage.textContent = message;
    statusMessage.className = `status-message show ${type}`;
    
    setTimeout(() => {
        statusMessage.classList.remove('show');
    }, 3000);
}

// Funcție helper pentru capitalizare
function capitalizeFirst(str) {
    const translations = {
        'happy': 'Fericit',
        'sad': 'Trist',
        'angry': 'Furios',
        'surprise': 'Surprins',
        'neutral': 'Neutru'
    };
    return translations[str] || str.charAt(0).toUpperCase() + str.slice(1);
}

// Cleanup la închiderea paginii
window.addEventListener('beforeunload', function() {
    stopAutoUpdate();
});