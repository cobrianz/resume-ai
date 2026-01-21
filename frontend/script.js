// API Configuration
// Auto-detect environment
const getAPIBaseURL = () => {
    if (typeof window !== 'undefined') {
        const hostname = window.location.hostname;
        const protocol = window.location.protocol;
        
        // If on localhost, use localhost API
        if (hostname === 'localhost' || hostname === '127.0.0.1') {
            return 'http://localhost:8000/api/v1';
        }
        
        // If deployed, use same domain API
        // Railway and most platforms serve frontend and backend from same domain
        return `${protocol}//${hostname}/api/v1`;
    }
    return 'http://localhost:8000/api/v1'; // Fallback
};

const API_BASE_URL = getAPIBaseURL();

// Mobile Menu Toggle
const mobileMenuBtn = document.getElementById('mobileMenuBtn');
const mainNav = document.getElementById('mainNav');

if (mobileMenuBtn) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenuBtn.classList.toggle('active');
        mainNav.classList.toggle('active');
    });

    // Close menu when clicking nav links
    mainNav.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            mobileMenuBtn.classList.remove('active');
            mainNav.classList.remove('active');
        });
    });
}

// State
let selectedFile = null;
let extractedResumeText = '';

// DOM Elements
const fileUpload = document.getElementById('fileUpload');
const resumeFileInput = document.getElementById('resumeFile');
const uploadPlaceholder = document.getElementById('uploadPlaceholder');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const fileSize = document.getElementById('fileSize');
const removeFileBtn = document.getElementById('removeFile');
const jobDescription = document.getElementById('jobDescription');
const analyzeBtn = document.getElementById('analyzeBtn');
const btnText = document.getElementById('btnText');
const spinner = document.getElementById('spinner');
const results = document.getElementById('results');

// File Upload Handlers
fileUpload.addEventListener('click', () => resumeFileInput.click());

fileUpload.addEventListener('dragover', (e) => {
    e.preventDefault();
    fileUpload.style.borderColor = 'var(--primary)';
    fileUpload.style.background = 'var(--bg-secondary)';
});

fileUpload.addEventListener('dragleave', () => {
    fileUpload.style.borderColor = 'var(--border)';
    fileUpload.style.background = 'transparent';
});

fileUpload.addEventListener('drop', (e) => {
    e.preventDefault();
    fileUpload.style.borderColor = 'var(--border)';
    fileUpload.style.background = 'transparent';

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

resumeFileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

removeFileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    selectedFile = null;
    resumeFileInput.value = '';
    uploadPlaceholder.style.display = 'block';
    fileInfo.style.display = 'none';
    checkFormValidity();
});

function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!validTypes.includes(file.type)) {
        showNotification('Please upload a PDF or DOCX file', 'error');
        return;
    }

    // Validate file size (10MB)
    if (file.size > 10 * 1024 * 1024) {
        showNotification('File size must be less than 10MB', 'error');
        return;
    }

    selectedFile = file;
    fileName.textContent = file.name;
    fileSize.textContent = formatFileSize(file.size);
    uploadPlaceholder.style.display = 'none';
    fileInfo.style.display = 'flex';
    checkFormValidity();
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

// Form Validation
jobDescription.addEventListener('input', checkFormValidity);

function checkFormValidity() {
    const isValid = selectedFile && jobDescription.value.trim().length > 50;
    analyzeBtn.disabled = !isValid;
}

// Analyze Button Handler
analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile || !jobDescription.value.trim()) return;

    // Show loading state
    analyzeBtn.disabled = true;
    btnText.textContent = 'Analyzing...';
    spinner.style.display = 'block';
    results.style.display = 'none';

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('resume_file', selectedFile);
        formData.append('job_description', jobDescription.value.trim());

        // Make API request
        const response = await fetch(`${API_BASE_URL}/match/`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }

        const data = await response.json();
        extractedResumeText = data.resume_text || '';
        displayResults(data);

        // Scroll to results
        setTimeout(() => {
            results.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);

    } catch (error) {
        console.error('Error:', error);
        showNotification(error.message || 'Failed to analyze resume. Please try again.', 'error');
    } finally {
        // Reset button state
        analyzeBtn.disabled = false;
        btnText.textContent = 'Analyze Resume';
        spinner.style.display = 'none';
        checkFormValidity();
    }
});

// Display Results
function displayResults(data) {
    results.style.display = 'block';

    // Overall Score
    const overallScore = document.getElementById('overallScore');
    overallScore.textContent = Math.round(data.match_score.overall_match) + '%';

    // Component Scores
    const components = data.match_score.components;
    updateScoreBar('skill', components.skill_match);
    updateScoreBar('exp', components.experience_match);
    updateScoreBar('keyword', components.keyword_match);

    // Missing Skills
    const missingSkillsSection = document.getElementById('missingSkillsSection');
    const missingSkillsContainer = document.getElementById('missingSkills');

    if (data.missing_skills && data.missing_skills.length > 0) {
        missingSkillsSection.style.display = 'block';
        missingSkillsContainer.innerHTML = data.missing_skills
            .map(skill => `<span class="skill-tag">${escapeHtml(skill)}</span>`)
            .join('');
    } else {
        missingSkillsSection.style.display = 'none';
    }

    // Suggestions
    const suggestionsList = document.getElementById('suggestionsList');
    suggestionsList.innerHTML = data.suggestions
        .map(suggestion => `
            <div class="suggestion-item">
                <h5>${escapeHtml(suggestion.section)}</h5>
                <p><strong>${escapeHtml(suggestion.suggestion)}</strong></p>
                <small>${escapeHtml(suggestion.justification)}</small>
            </div>
        `)
        .join('');
}

function updateScoreBar(type, score) {
    const scoreElement = document.getElementById(`${type}Score`);
    const progressElement = document.getElementById(`${type}Progress`);

    scoreElement.textContent = Math.round(score) + '%';

    // Animate progress bar
    setTimeout(() => {
        progressElement.style.width = score + '%';
    }, 100);
}

// Utility Functions
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'error' ? '#ef4444' : '#10b981'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;

    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});


// Refine Button Handler
const refineBtn = document.getElementById('refineBtn');
const refineSpinner = document.getElementById('refineSpinner');
const refinedContent = document.getElementById('refinedContent');

if (refineBtn) {
    refineBtn.addEventListener('click', async () => {
        if (!extractedResumeText || !jobDescription.value.trim()) {
            showNotification('Missing resume text or job description', 'error');
            return;
        }

        refineBtn.disabled = true;
        document.getElementById('refineBtnText').textContent = 'Refining...';
        refineSpinner.style.display = 'block';
        refinedContent.style.display = 'none';

        try {
            const formData = new FormData();
            formData.append('resume_text', extractedResumeText);
            formData.append('job_description', jobDescription.value.trim());

            const response = await fetch(`${API_BASE_URL}/refine/`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.detail || `HTTP ${response.status}: Refinement failed`);
            }

            const data = await response.json();

            // Update UI
            document.getElementById('refinedSummary').textContent = data.summary || 'No summary generated';

            // Format Experience (convert Markdown list to HTML)
            const expText = data.experience || 'No experience generated';
            const expHTML = expText
                .split('\n')
                .filter(line => line.trim().startsWith('-') || line.trim().startsWith('•'))
                .map(line => `<div style="margin-bottom: 8px;"><strong>✓</strong> ${line.replace(/^[-•]\s*/, '')}</div>`)
                .join('');

            document.getElementById('refinedExperience').innerHTML = expHTML || `<p>${expText}</p>`;

            refinedContent.style.display = 'block';
            refinedContent.scrollIntoView({ behavior: 'smooth', block: 'start' });

        } catch (error) {
            console.error('Refine error:', error);
            showNotification(`Failed to refine resume: ${error.message}`, 'error');
        } finally {
            refineBtn.disabled = false;
            document.getElementById('refineBtnText').textContent = 'Refine Resume';
            refineSpinner.style.display = 'none';
        }
    });
}
