let selectedDistance = null;
let measurementActive = false;
let startTime = null;
let velocity = 0;

function selectDistance(meters) {
    selectedDistance = meters;
    document.getElementById('selected-distance').textContent = meters + ' metros';
    document.getElementById('distance-info').textContent = meters + ' metros';
    showToast('Sucesso', `distancia settada para ${meters} metros`, 'sucesso');
}

function postMessage() {
    if (!selectedDistance) {
        showToast('Erro', 'Por favor, selecione uma distância para o teste!', 'erro');
        return;
    }

    // Hide the Post button and show the Stop button
    document.getElementById('start-btn').classList.add('hidden');
    document.getElementById('stop-btn').classList.remove('hidden');

    measurementActive = true;
    startTime = new Date();
    document.getElementById('status-info').textContent = 'em teste...';
    showToast('Sucesso', `Teste iniciado para ${selectedDistance}m`, 'sucesso');

    // Simulate velocity calculation (in a real app, this would come from actual measurements)
    calculateVelocity();
}

function stopMeasurement() {
    // Hide the Stop button and show the Post button
    document.getElementById('stop-btn').classList.add('hidden');
    document.getElementById('start-btn').classList.remove('hidden');

    measurementActive = false;
    document.getElementById('status-info').textContent = 'Fora de teste';
    showToast('Parou', 'Teste interrompido', 'info');
}

function calculateVelocity() {
    if (!measurementActive) return;

    // In a real app, this would calculate based on actual measurements
    // Here we simulate a random velocity between 2 and 5 m/s
    velocity = (Math.random() * 3 + 2).toFixed(2);
    document.getElementById('velocity-info').textContent = velocity + ' m/s';

    // Update every second
    setTimeout(calculateVelocity, 1000);
}

function showToast(title, message, type) {
    const toast = document.getElementById('toast');
    const toastIcon = document.getElementById('toast-icon');
    const toastTitle = document.getElementById('toast-title');
    const toastMessage = document.getElementById('toast-message');

    // Set content
    toastTitle.textContent = title;
    toastMessage.textContent = message;

    // Set icon and color based on type
    switch (type) {
        case 'success':
            toastIcon.className = 'fas fa-check-circle text-green-400 text-xl';
            break;
        case 'error':
            toastIcon.className = 'fas fa-exclamation-circle text-red-400 text-xl';
            break;
        case 'info':
            toastIcon.className = 'fas fa-info-circle text-blue-400 text-xl';
            break;
        default:
            toastIcon.className = 'fas fa-info-circle text-blue-400 text-xl';
    }

    // Show toast
    toast.classList.add('show');

    // Hide after 3 seconds
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}