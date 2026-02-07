// ===============================
// Configuration
// ===============================
const API_BASE_URL = 'http://localhost:8000/api';

// ===============================
// State Management
// ===============================
let currentStep = 1;
let profileData = {};
let loanData = {};
let predictionChart = null;

// ===============================
// Step Navigation
// ===============================
function nextStep(step) {
    if (step === 1) {
        const form = document.getElementById('profileForm');

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        profileData = {
            name: document.getElementById('name').value,
            age: parseInt(document.getElementById('age').value),
            gender: document.getElementById('gender').value,
            employment_type: document.getElementById('employmentType').value
        };

        currentStep = 2;
        updateFormSteps();
    }
}

function prevStep(step) {
    if (step === 2) {
        currentStep = 1;
        updateFormSteps();
    }
}

function updateFormSteps() {
    const progressSteps = document.querySelectorAll('.progress-step');
    progressSteps.forEach((step, index) => {
        const stepNumber = index + 1;
        step.classList.remove('active', 'completed');

        if (stepNumber < currentStep) {
            step.classList.add('completed');
        } else if (stepNumber === currentStep) {
            step.classList.add('active');
        }
    });

    document.querySelectorAll('.application-form')
        .forEach(form => form.classList.remove('active'));

    if (currentStep === 1) {
        document.getElementById('profileForm').classList.add('active');
    } else if (currentStep === 2) {
        document.getElementById('loanForm').classList.add('active');
    }
}

// ===============================
// Submit Loan Application
// ===============================
async function submitApplication() {
    const form = document.getElementById('loanForm');

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    loanData = {
        applicant_income: parseFloat(document.getElementById('applicantIncome').value),
        coapplicant_income: parseFloat(document.getElementById('coapplicantIncome').value) || 0,
        loan_amount: parseFloat(document.getElementById('loanAmount').value),
        loan_term: parseInt(document.getElementById('loanTerm').value),
        credit_history: parseInt(document.getElementById('creditHistory').value),
        dependents: document.getElementById('dependents').value,
        property_area: document.getElementById('propertyArea').value,
        married: document.getElementById('married').value,
        education: document.getElementById('education').value
    };

    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                profile: profileData,
                loan_details: loanData
            })
        });

        if (!response.ok) throw new Error('Prediction failed');

        const result = await response.json();
        hideLoading();
        displayResults(result);

    } catch (error) {
        console.error(error);
        hideLoading();
        alert('Error: Make sure backend is running at http://localhost:8000');
    }
}

// ===============================
// Display Results
// ===============================
function displayResults(result) {

    currentStep = 3;

    document.querySelectorAll('.progress-step')
        .forEach(step => step.classList.remove('active'));

    document.querySelectorAll('.application-form')
        .forEach(form => form.classList.remove('active'));

    document.getElementById('resultsSection').classList.add('active');

    const isApproved = result.prediction === 'Y';
    const icon = isApproved ? '✓' : '✗';
    const statusClass = isApproved ? 'approved' : 'rejected';

    document.getElementById('resultsCard').innerHTML = `
        <div class="result-header">
            <div class="result-icon ${statusClass}">${icon}</div>
            <h2 class="${statusClass}">
                Loan ${result.prediction_label}
            </h2>
            <p>Application for ${result.applicant_name}</p>
        </div>

        <div class="result-stats">
            <div>
                <h4>Approval Probability</h4>
                <p>${result.probability_approved.toFixed(2)}%</p>
            </div>
            <div>
                <h4>Rejection Probability</h4>
                <p>${result.probability_rejected.toFixed(2)}%</p>
            </div>
        </div>

        <canvas id="predictionChart"></canvas>

        <div class="result-actions">
            <button onclick="resetApplication()">New Application</button>
            <button onclick="window.print()">Print</button>
        </div>
    `;

    createPredictionChart(result);
}

// ===============================
// Chart.js Graph
// ===============================
function createPredictionChart(result) {

    const ctx = document.getElementById('predictionChart');

    if (predictionChart) {
        predictionChart.destroy();
    }

    predictionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Approved', 'Rejected'],
            datasets: [{
                label: 'Probability (%)',
                data: [
                    result.probability_approved,
                    result.probability_rejected
                ],
                backgroundColor: [
                    'rgba(34,197,94,0.7)',
                    'rgba(239,68,68,0.7)'
                ],
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });
}

// ===============================
// Reset Application
// ===============================
function resetApplication() {
    currentStep = 1;
    profileData = {};
    loanData = {};

    document.getElementById('profileForm').reset();
    document.getElementById('loanForm').reset();

    document.getElementById('resultsSection').classList.remove('active');
    document.getElementById('profileForm').classList.add('active');

    updateFormSteps();
    document.getElementById('apply').scrollIntoView({ behavior: 'smooth' });
}

// ===============================
// Contact Form
// ===============================
async function handleContactSubmit(e) {
    e.preventDefault();

    const formData = {
        name: document.getElementById('contactName').value,
        email: document.getElementById('contactEmail').value,
        subject: document.getElementById('contactSubject').value,
        message: document.getElementById('contactMessage').value
    };

    showLoading();

    try {
        const response = await fetch(`${API_BASE_URL}/contact`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) throw new Error('Contact failed');

        const result = await response.json();
        hideLoading();
        alert(result.message);

        document.getElementById('contactForm').reset();

    } catch (error) {
        console.error(error);
        hideLoading();
        alert('Failed to send message.');
    }
}

// ===============================
// Loading Overlay
// ===============================
function showLoading() {
    document.getElementById('loadingOverlay')?.classList.add('active');
}

function hideLoading() {
    document.getElementById('loadingOverlay')?.classList.remove('active');
}

// ===============================
// Navigation + Initialization
// ===============================
document.addEventListener('DOMContentLoaded', () => {

    document.getElementById('contactForm')
        ?.addEventListener('submit', handleContactSubmit);

    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute('href'));
            target?.scrollIntoView({ behavior: 'smooth' });
        });
    });

});
