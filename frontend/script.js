const loginView = document.getElementById('loginView');
const dashboardView = document.getElementById('dashboardView');
const loginBtn = document.getElementById('loginBtn');
const logoutBtn = document.getElementById('logoutBtn');

loginBtn.addEventListener('click', () => {
    loginView.classList.remove('active');
    dashboardView.classList.add('active');
});

logoutBtn.addEventListener('click', () => {
    dashboardView.classList.remove('active');
    loginView.classList.add('active');
});

const tabBtns = document.querySelectorAll('.tab-btn');
const tabContents = document.querySelectorAll('.tab-content');

tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        tabBtns.forEach(b => b.classList.remove('active'));
        tabContents.forEach(c => c.classList.remove('active'));

        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');
    });
});

const soilImageInput = document.getElementById('soilImage');
const fileNameDisplay = document.getElementById('fileNameDisplay');
if(soilImageInput) {
    soilImageInput.addEventListener('change', (e) => {
        if(e.target.files.length > 0) {
            fileNameDisplay.textContent = `Selected: ${e.target.files[0].name}`;
        }
    });
}

document.getElementById('manualForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const ph = document.getElementById('ph').value;
    const texture = document.getElementById('texture').value;
    const nitrogen = document.getElementById('nitrogen').value;
    
    await submitData('/analyze', { ph: parseFloat(ph), texture, nitrogen });
});

document.getElementById('imageForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    const fileInput = document.getElementById('soilImage');
    if(fileInput.files.length === 0) {
        alert("Please select an image file first.");
        return;
    }

    const formData = new FormData();
    formData.append("soil_image", fileInput.files[0]);

    await submitData('/analyze', formData, true);
});

async function submitData(url, payload, isFormData = false) {
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'block';
    resultsDiv.innerHTML = 'Analyzing soil parameters & generating crop matches...';

    try {
        const options = {
            method: 'POST',
            body: isFormData ? payload : JSON.stringify(payload)
        };

        if (!isFormData) {
            options.headers = { 'Content-Type': 'application/json' };
        }

        const response = await fetch(url, options);
        const data = await response.json();

        if (data.status !== 'success') {
            throw new Error(data.message || 'Analysis failed');
        }

        let htmlOutput = `<strong>Analysis Complete (${data.mode.toUpperCase()} Mode)</strong><br>`;
        if(data.mode === 'image') {
            htmlOutput += `• Detected Texture: <strong>${data.texture}</strong><br>`;
            htmlOutput += `• Estimated pH: <strong>${data.ph}</strong><br>`;
        } else {
            htmlOutput += `• pH Level: ${data.ph} | Texture: ${data.texture} | Nitrogen: ${data.nitrogen}<br>`;
        }

        htmlOutput += `<br><strong>Soil Evaluation:</strong><br>• Health Score: ${data.evaluation.health_score}/100<br>`;
        data.evaluation.issues.forEach(issue => {
            htmlOutput += `• Note: ${issue}<br>`;
        });

        htmlOutput += `<br><strong>Recommended Crops:</strong>`;
        data.recommendations.forEach(rec => {
            htmlOutput += `
                <div class="crop-card">
                    <strong>${rec.crop}</strong> (${rec.match_score} Match)<br>
                    <span style="font-size: 11px; color: #555;">${rec.description}</span>
                </div>
            `;
        });

        resultsDiv.innerHTML = htmlOutput;
    } catch (error) {
        console.error('Error:', error);
        resultsDiv.innerHTML = `<span style="color: #dc2626;">Error: ${error.message}</span>`;
    }
}