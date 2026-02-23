// AI Resume Analyzer Demo JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const fileDisplay = document.getElementById('fileDisplay');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const removeFile = document.getElementById('removeFile');
    const jobDesc = document.getElementById('jobDesc');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const loading = document.getElementById('loading');
    const resultsSection = document.getElementById('resultsSection');
    const matchScore = document.getElementById('matchScore');
    const matchedSkills = document.getElementById('matchedSkills');
    const missingSkills = document.getElementById('missingSkills');
    const matchedCount = document.getElementById('matchedCount');
    const missingCount = document.getElementById('missingCount');
    const messageBox = document.getElementById('messageBox');

    let uploadedFile = null;

    // Drag and Drop Events
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileUpload(files[0]);
        }
    });

    // File Input Change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });

    // Remove File
    removeFile.addEventListener('click', () => {
        uploadedFile = null;
        fileDisplay.style.display = 'none';
        uploadArea.style.display = 'block';
        fileInput.value = '';
        resetResults();
    });

    // Analyze Button
    analyzeBtn.addEventListener('click', performAnalysis);

    // Handle File Upload
    function handleFileUpload(file) {
        // Validate file type
        const validTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
        if (!validTypes.includes(file.type)) {
            alert('Please upload a PDF, DOC, or DOCX file.');
            return;
        }

        // Validate file size (200MB limit)
        const maxSize = 200 * 1024 * 1024; // 200MB in bytes
        if (file.size > maxSize) {
            alert('File size exceeds 200MB limit.');
            return;
        }

        uploadedFile = file;
        
        // Update UI
        fileName.textContent = file.name;
        fileSize.textContent = formatFileSize(file.size);
        uploadArea.style.display = 'none';
        fileDisplay.style.display = 'flex';
        
        // Reset results
        resetResults();
    }

    // Format File Size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // Perform Analysis
    function performAnalysis() {
        if (!uploadedFile) {
            alert('Please upload a resume first.');
            return;
        }

        if (!jobDesc.value.trim()) {
            alert('Please enter a job description.');
            return;
        }

        // Show loading
        loading.classList.add('active');
        resultsSection.style.display = 'none';
        analyzeBtn.disabled = true;

        // Simulate API call
        setTimeout(() => {
            const analysisResult = simulateAnalysis();
            displayResults(analysisResult);
            
            // Hide loading
            loading.classList.remove('active');
            resultsSection.style.display = 'block';
            analyzeBtn.disabled = false;
        }, 2000);
    }

    // Simulate Analysis (Demo Function)
    function simulateAnalysis() {
        const jobDescription = jobDesc.value.toLowerCase();
        const resumeSkills = ['python', 'javascript', 'react', 'node.js', 'sql', 'git', 'docker', 'aws', 'machine learning', 'data analysis'];
        const jobSkills = extractSkills(jobDescription);
        
        const matched = resumeSkills.filter(skill => 
            jobSkills.some(jobSkill => skill.toLowerCase().includes(jobSkill) || jobSkill.includes(skill.toLowerCase()))
        );
        
        const missing = jobSkills.filter(skill => 
            !matched.some(matchedSkill => 
                matchedSkill.toLowerCase().includes(skill) || skill.includes(matchedSkill.toLowerCase())
            )
        );

        const matchPercentage = Math.round((matched.length / Math.max(jobSkills.length, 1)) * 100);

        return {
            matchScore: matchPercentage,
            matchedSkills: matched,
            missingSkills: missing,
            message: generateMessage(matchPercentage, missing.length)
        };
    }

    // Extract Skills from Job Description
    function extractSkills(text) {
        const commonSkills = [
            'python', 'java', 'javascript', 'react', 'angular', 'vue', 'node.js', 'nodejs',
            'sql', 'mysql', 'postgresql', 'mongodb', 'git', 'docker', 'kubernetes',
            'aws', 'azure', 'gcp', 'machine learning', 'ml', 'data analysis', 'data science',
            'html', 'css', 'typescript', 'c++', 'c#', 'php', 'ruby', 'swift',
            'kotlin', 'scala', 'go', 'rust', 'tensorflow', 'pytorch', 'numpy', 'pandas'
        ];

        const found = [];
        const words = text.split(/\s+/);
        
        commonSkills.forEach(skill => {
            if (text.includes(skill.toLowerCase())) {
                found.push(skill);
            }
        });

        return found;
    }

    // Generate Message
    function generateMessage(matchScore, missingCount) {
        if (matchScore >= 70) {
            return 'Excellent match! Your resume aligns well with this job.';
        } else if (matchScore >= 40) {
            return missingCount === 0 
                ? 'Good match! Consider highlighting more relevant experience.'
                : `Good match! Add ${missingCount} missing skills to improve your chances.`;
        } else {
            return missingCount === 0
                ? 'Low match. Consider reformatting your resume to highlight relevant skills.'
                : `Low match. Add ${missingCount} key skills to significantly improve your chances.`;
        }
    }

    // Display Results
    function displayResults(result) {
        // Update match score
        matchScore.textContent = result.matchScore + '%';
        matchScore.className = 'match-score';
        
        if (result.matchScore >= 70) {
            matchScore.classList.add('high');
        } else if (result.matchScore >= 40) {
            matchScore.classList.add('medium');
        } else {
            matchScore.classList.add('low');
        }

        // Update match score message
        const scoreMessage = matchScore.nextElementSibling;
        if (result.matchScore >= 70) {
            scoreMessage.textContent = 'High match - strong candidate';
        } else if (result.matchScore >= 40) {
            scoreMessage.textContent = 'Medium match - good potential';
        } else {
            scoreMessage.textContent = 'Low match - needs improvement';
        }

        // Update matched skills
        matchedSkills.innerHTML = '';
        result.matchedSkills.forEach(skill => {
            const tag = document.createElement('span');
            tag.className = 'skill-tag';
            tag.textContent = skill;
            matchedSkills.appendChild(tag);
        });
        matchedCount.textContent = result.matchedSkills.length;

        // Update missing skills
        missingSkills.innerHTML = '';
        result.missingSkills.forEach(skill => {
            const tag = document.createElement('span');
            tag.className = 'skill-tag';
            tag.textContent = skill;
            missingSkills.appendChild(tag);
        });
        missingCount.textContent = result.missingSkills.length;

        // Update message box
        messageBox.textContent = result.message;
        messageBox.className = result.missingSkills.length > 0 ? 'message-box warning' : 'message-box';
    }

    // Reset Results
    function resetResults() {
        resultsSection.style.display = 'none';
        matchScore.textContent = '0%';
        matchScore.className = 'match-score';
        matchedSkills.innerHTML = '';
        missingSkills.innerHTML = '';
        matchedCount.textContent = '0';
        missingCount.textContent = '0';
        messageBox.className = 'message-box';
    }

    // Add some sample data for demonstration
    setTimeout(() => {
        if (!uploadedFile && jobDesc.value.includes('python')) {
            // Auto-populate with sample data for demo
            const sampleFile = { name: 'sample_resume.pdf', size: 2048000 };
            handleFileUpload(sampleFile);
        }
    }, 1000);
});
