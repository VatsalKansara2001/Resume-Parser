// Resume Parser 2025 - Main Application Logic

// Sample data from the provided JSON
const sampleData = {
  parsedResume: {
    resume_id: "123e4567-e89b-12d3-a456-426614174000",
    filename: "john_smith_resume.pdf",
    status: "completed",
    confidence_score: 0.92,
    processing_time: 2.3,
    parsed_data: {
      personal_info: {
        name: "John Smith",
        email: "john.smith@email.com",
        phone: "+1-555-123-4567",
        location: "San Francisco, CA"
      },
      contact_info: {
        linkedin: "https://linkedin.com/in/johnsmith",
        github: "https://github.com/johnsmith",
        website: "https://johnsmith.dev"
      },
      professional_summary: "Senior Software Engineer with 8+ years of experience in full-stack development, specializing in cloud-native applications and scalable web solutions.",
      work_experience: [
        {
          job_title: "Senior Software Engineer",
          company: "Tech Corp",
          start_date: "2020-01",
          end_date: "present",
          duration_months: 48,
          description: "Led development of cloud-native applications using Python, React, and AWS. Managed a team of 5 developers and improved system performance by 40%.",
          confidence: 0.95
        },
        {
          job_title: "Software Engineer",
          company: "StartupXYZ",
          start_date: "2018-06",
          end_date: "2019-12",
          duration_months: 18,
          description: "Developed microservices architecture and RESTful APIs. Built CI/CD pipelines and implemented automated testing.",
          confidence: 0.89
        }
      ],
      education: [
        {
          degree: "Bachelor of Science",
          field_of_study: "Computer Science",
          institution: "Stanford University",
          graduation_year: "2018",
          confidence: 0.96
        }
      ],
      skills: {
        technical_skills: [
          { skill: "Python", category: "programming", confidence: 0.98 },
          { skill: "React", category: "frontend", confidence: 0.92 },
          { skill: "AWS", category: "cloud", confidence: 0.87 },
          { skill: "Docker", category: "devops", confidence: 0.84 },
          { skill: "PostgreSQL", category: "database", confidence: 0.79 }
        ],
        soft_skills: [
          { skill: "Leadership", confidence: 0.85 },
          { skill: "Communication", confidence: 0.82 },
          { skill: "Project Management", confidence: 0.78 }
        ]
      },
      certifications: [
        {
          name: "AWS Certified Solutions Architect",
          issuer: "Amazon Web Services",
          issue_date: "2021-03",
          confidence: 0.94
        }
      ],
      projects: [
        {
          title: "E-commerce Platform",
          description: "Built scalable e-commerce platform handling 10k+ concurrent users",
          technologies: ["Python", "Django", "React", "AWS"],
          confidence: 0.88
        }
      ]
    }
  },
  jobMatch: {
    resume_id: "123e4567-e89b-12d3-a456-426614174000",
    job_title: "Senior Python Developer",
    overall_score: 0.87,
    confidence: 0.91,
    skill_match_score: 0.92,
    experience_score: 0.85,
    recommendation: "strong_match",
    matched_skills: ["Python", "Django", "AWS", "Docker"],
    missing_skills: ["Kubernetes", "Machine Learning"],
    experience_analysis: {
      required_years: 5,
      candidate_years: 8,
      meets_requirement: true
    }
  },
  analytics: {
    total_resumes: 1247,
    successful_parses: 1189,
    failed_parses: 58,
    success_rate: 95.3,
    avg_processing_time: 32.5,
    avg_confidence_score: 0.88,
    top_skills: [
      { skill: "Python", count: 423 },
      { skill: "JavaScript", count: 387 },
      { skill: "AWS", count: 298 },
      { skill: "React", count: 267 },
      { skill: "Docker", count: 198 }
    ]
  }
};

// Application State
let currentSection = 'home';
let uploadedFiles = [];
let processingQueue = [];
let theme = 'auto';

// Global navigation function
function showSection(sectionName) {
  console.log('Navigating to section:', sectionName);
  
  // Hide all sections
  const sections = document.querySelectorAll('.section');
  sections.forEach(section => {
    section.classList.add('hidden');
  });

  // Hide hero section
  const heroSection = document.getElementById('heroSection');
  if (heroSection) {
    heroSection.classList.add('hidden');
  }

  // Show target section
  if (sectionName === 'home') {
    if (heroSection) {
      heroSection.classList.remove('hidden');
      console.log('Showed hero section');
    }
  } else {
    const targetSection = document.getElementById(sectionName + 'Section');
    if (targetSection) {
      targetSection.classList.remove('hidden');
      console.log('Showed section:', targetSection.id);
    } else {
      console.error('Section not found:', sectionName + 'Section');
    }
  }

  // Update navigation state
  currentSection = sectionName;
  updateNavigation();

  // Initialize section-specific features
  if (sectionName === 'analytics') {
    setTimeout(initializeCharts, 200);
  } else if (sectionName === 'results') {
    populateResults();
  } else if (sectionName === 'matching') {
    populateJobMatch();
  }
}

function updateNavigation() {
  const navTabs = document.querySelectorAll('.nav-tab');
  navTabs.forEach(tab => {
    const tabSection = tab.getAttribute('data-section');
    if (tabSection === currentSection) {
      tab.classList.add('active');
    } else {
      tab.classList.remove('active');
    }
  });
}

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM loaded, initializing app...');
  
  initializeApp();
  setupEventListeners();
  setupTheme();
  populateResults();
  
  setTimeout(() => {
    initializeCharts();
    showToast('Welcome to Resume Parser 2025!', 'Ready to parse resumes with AI-powered accuracy.', 'success');
  }, 500);
});

// Initialize app
function initializeApp() {
  showSection('home');
}

// Event Listeners Setup
function setupEventListeners() {
  console.log('Setting up event listeners...');
  
  // Hero CTA button
  const ctaBtn = document.querySelector('.cta-btn');
  if (ctaBtn) {
    console.log('Found CTA button, adding listener');
    ctaBtn.addEventListener('click', function(e) {
      e.preventDefault();
      console.log('CTA button clicked');
      showSection('upload');
    });
  } else {
    console.error('CTA button not found');
  }

  // Navigation tabs - bottom navigation
  const navTabs = document.querySelectorAll('.nav-tab');
  console.log('Found', navTabs.length, 'navigation tabs');
  
  navTabs.forEach((tab, index) => {
    const section = tab.getAttribute('data-section');
    console.log('Setting up tab', index, 'for section:', section);
    
    if (section) {
      tab.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('Nav tab clicked for section:', section);
        showSection(section);
      });
    }
  });

  // Theme toggle
  const themeToggle = document.getElementById('themeToggle');
  if (themeToggle) {
    console.log('Setting up theme toggle');
    themeToggle.addEventListener('click', function(e) {
      e.preventDefault();
      toggleTheme();
    });
  }

  // Settings modal
  const settingsBtn = document.getElementById('settingsBtn');
  if (settingsBtn) {
    console.log('Setting up settings button');
    settingsBtn.addEventListener('click', function(e) {
      e.preventDefault();
      openModal('settingsModal');
    });
  }

  // File upload
  setupFileUpload();
  
  // Job matching
  setupJobMatching();
  
  // Export buttons
  setupExportButtons();
  
  // Tab buttons in results section
  setupResultsTabs();
  
  // Settings tabs
  setupSettingsTabs();
}

function setupFileUpload() {
  const uploadArea = document.getElementById('uploadArea');
  const fileInput = document.getElementById('fileInput');
  const browseBtn = document.getElementById('browseBtn');

  if (uploadArea) {
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleFileDrop);
    uploadArea.addEventListener('click', function() {
      if (fileInput) {
        console.log('Upload area clicked, triggering file input');
        fileInput.click();
      }
    });
  }

  if (browseBtn) {
    browseBtn.addEventListener('click', function(e) {
      e.stopPropagation();
      console.log('Browse button clicked');
      if (fileInput) fileInput.click();
    });
  }

  if (fileInput) {
    fileInput.addEventListener('change', handleFileSelect);
  }
}

function setupJobMatching() {
  // Add a slight delay to ensure elements are available
  setTimeout(() => {
    const analyzeBtn = document.querySelector('#matchingSection button[onclick*="analyzeMatch"]');
    if (analyzeBtn) {
      analyzeBtn.removeAttribute('onclick');
      analyzeBtn.addEventListener('click', function(e) {
        e.preventDefault();
        analyzeMatch();
      });
    }
  }, 100);
}

function setupExportButtons() {
  setTimeout(() => {
    const exportJsonBtn = document.querySelector('button[onclick*="exportResults(\'json\')"]');
    const exportCsvBtn = document.querySelector('button[onclick*="exportResults(\'csv\')"]');
    
    if (exportJsonBtn) {
      exportJsonBtn.removeAttribute('onclick');
      exportJsonBtn.addEventListener('click', () => exportResults('json'));
    }
    
    if (exportCsvBtn) {
      exportCsvBtn.removeAttribute('onclick');
      exportCsvBtn.addEventListener('click', () => exportResults('csv'));
    }
  }, 100);
}

function setupResultsTabs() {
  setTimeout(() => {
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
      btn.addEventListener('click', function(e) {
        e.preventDefault();
        const tabName = this.getAttribute('onclick')?.match(/'(\w+)'/)?.[1];
        if (tabName) {
          this.removeAttribute('onclick');
          showTab(tabName);
        }
      });
    });
  }, 100);
}

function setupSettingsTabs() {
  setTimeout(() => {
    const settingsTabs = document.querySelectorAll('.settings-tab');
    settingsTabs.forEach(tab => {
      tab.addEventListener('click', function(e) {
        e.preventDefault();
        const tabName = this.getAttribute('onclick')?.match(/'(\w+)'/)?.[1];
        if (tabName) {
          this.removeAttribute('onclick');
          showSettingsTab(tabName);
        }
      });
    });
    
    const saveBtn = document.querySelector('button[onclick*="saveSettings"]');
    if (saveBtn) {
      saveBtn.removeAttribute('onclick');
      saveBtn.addEventListener('click', saveSettings);
    }
  }, 100);
}

// Theme Management
function setupTheme() {
  const savedTheme = localStorage.getItem('theme') || 'auto';
  theme = savedTheme;
  applyTheme(theme);
  updateThemeSelect();
}

function toggleTheme() {
  console.log('Toggling theme from:', theme);
  const themes = ['auto', 'light', 'dark'];
  const currentIndex = themes.indexOf(theme);
  const nextIndex = (currentIndex + 1) % themes.length;
  theme = themes[nextIndex];
  console.log('New theme:', theme);
  applyTheme(theme);
  updateThemeIcon();
  localStorage.setItem('theme', theme);
}

function applyTheme(themeName) {
  const html = document.documentElement;
  
  if (themeName === 'auto') {
    html.removeAttribute('data-color-scheme');
  } else {
    html.setAttribute('data-color-scheme', themeName);
  }
}

function updateThemeIcon() {
  const themeIcon = document.querySelector('#themeToggle .material-icons');
  if (themeIcon) {
    const iconMap = {
      auto: 'brightness_auto',
      light: 'light_mode',
      dark: 'dark_mode'
    };
    themeIcon.textContent = iconMap[theme] || 'light_mode';
  }
}

function updateThemeSelect() {
  const themeSelect = document.getElementById('themeSelect');
  if (themeSelect) {
    themeSelect.value = theme;
  }
  updateThemeIcon();
}

// File Upload Handling
function handleDragOver(e) {
  e.preventDefault();
  e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
  e.preventDefault();
  e.currentTarget.classList.remove('dragover');
}

function handleFileDrop(e) {
  e.preventDefault();
  e.currentTarget.classList.remove('dragover');
  const files = Array.from(e.dataTransfer.files);
  processUploadedFiles(files);
}

function handleFileSelect(e) {
  const files = Array.from(e.target.files);
  processUploadedFiles(files);
}

function processUploadedFiles(files) {
  console.log('Processing uploaded files:', files.length);
  
  const validFiles = files.filter(file => {
    const validTypes = ['.pdf', '.docx', '.txt', '.rtf', '.odt'];
    const fileExt = '.' + file.name.split('.').pop().toLowerCase();
    const isValidType = validTypes.includes(fileExt);
    const isValidSize = file.size <= 10 * 1024 * 1024; // 10MB
    
    if (!isValidType) {
      showToast('Invalid File Type', `${file.name} is not a supported format.`, 'error');
      return false;
    }
    if (!isValidSize) {
      showToast('File Too Large', `${file.name} exceeds 10MB limit.`, 'error');
      return false;
    }
    return true;
  });

  if (validFiles.length > 0) {
    uploadedFiles.push(...validFiles);
    displayUploadQueue();
    showToast('Files Added', `${validFiles.length} file(s) added to queue.`, 'success');
  }
}

function displayUploadQueue() {
  const queueContainer = document.getElementById('uploadQueue');
  const queueList = document.getElementById('queueList');
  
  if (!queueContainer || !queueList) return;
  
  if (uploadedFiles.length === 0) {
    queueContainer.classList.add('hidden');
    return;
  }

  queueContainer.classList.remove('hidden');
  queueList.innerHTML = '';

  uploadedFiles.forEach((file, index) => {
    const queueItem = document.createElement('div');
    queueItem.className = 'queue-item';
    queueItem.innerHTML = `
      <div class="file-info">
        <span class="file-name">${file.name}</span>
        <span class="file-size">${formatFileSize(file.size)}</span>
      </div>
      <div class="queue-actions">
        <button class="btn btn--outline btn--sm" data-index="${index}">
          <span class="material-icons">delete</span>
        </button>
      </div>
    `;
    
    // Add event listener to remove button
    const removeBtn = queueItem.querySelector('button');
    removeBtn.addEventListener('click', () => removeFromQueue(index));
    
    queueList.appendChild(queueItem);
  });
}

function removeFromQueue(index) {
  uploadedFiles.splice(index, 1);
  displayUploadQueue();
  showToast('File Removed', 'File removed from processing queue.', 'info');
}

function clearQueue() {
  uploadedFiles = [];
  displayUploadQueue();
  showToast('Queue Cleared', 'All files removed from queue.', 'info');
}

function processAll() {
  if (uploadedFiles.length === 0) {
    showToast('No Files', 'Please add files to the queue first.', 'warning');
    return;
  }

  showToast('Processing Started', `Processing ${uploadedFiles.length} file(s)...`, 'info');
  
  // Simulate processing
  uploadedFiles.forEach((file, index) => {
    setTimeout(() => {
      simulateProcessing(file);
    }, index * 1000);
  });

  // Navigate to dashboard
  setTimeout(() => {
    showSection('dashboard');
  }, 500);
}

function simulateProcessing(file) {
  const processingItem = document.getElementById('currentProcessing');
  if (processingItem) {
    const fileName = processingItem.querySelector('.file-name');
    const status = processingItem.querySelector('.status');
    const progressFill = processingItem.querySelector('.progress-fill');
    const details = processingItem.querySelector('.processing-details');

    if (fileName) fileName.textContent = file.name;
    if (status) {
      status.textContent = 'Processing';
      status.className = 'status status--info';
    }

    // Simulate progress
    let progress = 0;
    const interval = setInterval(() => {
      progress += Math.random() * 15;
      if (progress >= 100) {
        progress = 100;
        clearInterval(interval);
        
        // Complete processing
        if (status) {
          status.textContent = 'Completed';
          status.className = 'status status--success';
        }
        if (details) {
          details.innerHTML = `
            <span>Processing complete - Ready for review</span>
            <span>Confidence: 92%</span>
          `;
        }
        
        showToast('Processing Complete', `${file.name} processed successfully!`, 'success');
      }
      
      if (progressFill) progressFill.style.width = `${Math.min(progress, 100)}%`;
      if (details && progress < 100) {
        const steps = ['Extracting text...', 'Analyzing structure...', 'Extracting entities...', 'Processing skills...', 'Finalizing results...'];
        const currentStep = Math.floor((progress / 100) * steps.length);
        const eta = Math.ceil((100 - progress) / 10);
        details.innerHTML = `
          <span>${Math.min(progress, 100).toFixed(0)}% complete - ${steps[Math.min(currentStep, steps.length - 1)]}</span>
          <span>ETA: ${eta}s</span>
        `;
      }
    }, 200);
  }
}

// Results Display Functions
function populateResults() {
  populatePersonalInfo();
  populateExperience();
  populateSkills();
  populateEducation();
  populateProjects();
}

function populatePersonalInfo() {
  const personalInfo = document.getElementById('personalInfo');
  if (!personalInfo) return;

  const { personal_info, contact_info } = sampleData.parsedResume.parsed_data;
  const allInfo = { ...personal_info, ...contact_info };
  
  personalInfo.innerHTML = Object.entries(allInfo).map(([key, value]) => `
    <div class="info-item">
      <span class="info-label">${formatLabel(key)}</span>
      <span class="info-value">${formatValue(key, value)}</span>
    </div>
  `).join('');
}

function populateExperience() {
  const timeline = document.getElementById('experienceTimeline');
  if (!timeline) return;

  const experiences = sampleData.parsedResume.parsed_data.work_experience;
  timeline.innerHTML = experiences.map(exp => `
    <div class="timeline-item">
      <div class="experience-header">
        <div>
          <div class="job-title">${exp.job_title}</div>
          <div class="company">${exp.company}</div>
        </div>
        <div class="duration">${formatDuration(exp.start_date, exp.end_date)}</div>
      </div>
      <div class="experience-description">${exp.description}</div>
      <div class="confidence-indicator">
        <small>Confidence: ${(exp.confidence * 100).toFixed(0)}%</small>
      </div>
    </div>
  `).join('');
}

function populateSkills() {
  const skillsContainer = document.getElementById('skillsContainer');
  if (!skillsContainer) return;

  const { technical_skills, soft_skills } = sampleData.parsedResume.parsed_data.skills;
  
  skillsContainer.innerHTML = `
    <div class="skill-category">
      <h4>Technical Skills</h4>
      <div class="skill-list">
        ${technical_skills.map(skill => `
          <span class="skill-tag">
            ${skill.skill}
            <span class="skill-confidence">${(skill.confidence * 100).toFixed(0)}%</span>
          </span>
        `).join('')}
      </div>
    </div>
    <div class="skill-category">
      <h4>Soft Skills</h4>
      <div class="skill-list">
        ${soft_skills.map(skill => `
          <span class="skill-tag">
            ${skill.skill}
            <span class="skill-confidence">${(skill.confidence * 100).toFixed(0)}%</span>
          </span>
        `).join('')}
      </div>
    </div>
  `;
}

function populateEducation() {
  const educationList = document.getElementById('educationList');
  if (!educationList) return;

  const education = sampleData.parsedResume.parsed_data.education;
  educationList.innerHTML = education.map(edu => `
    <div class="education-item">
      <div class="education-header">
        <div>
          <div class="degree">${edu.degree} in ${edu.field_of_study}</div>
          <div class="institution">${edu.institution}</div>
        </div>
        <div class="graduation-year">${edu.graduation_year}</div>
      </div>
      <div class="confidence-indicator">
        <small>Confidence: ${(edu.confidence * 100).toFixed(0)}%</small>
      </div>
    </div>
  `).join('');
}

function populateProjects() {
  const projectsList = document.getElementById('projectsList');
  if (!projectsList) return;

  const { projects, certifications } = sampleData.parsedResume.parsed_data;
  
  let html = '<h4>Certifications</h4>';
  html += certifications.map(cert => `
    <div class="certification-item">
      <div class="cert-name">${cert.name}</div>
      <div class="cert-issuer">${cert.issuer}</div>
      <div class="cert-date">Issued: ${formatDate(cert.issue_date)}</div>
    </div>
  `).join('');

  html += '<h4 style="margin-top: 24px;">Projects</h4>';
  html += projects.map(project => `
    <div class="project-item">
      <div class="project-title">${project.title}</div>
      <div class="project-description">${project.description}</div>
      <div class="project-technologies">
        ${project.technologies.map(tech => `<span class="tech-tag">${tech}</span>`).join('')}
      </div>
    </div>
  `).join('');

  projectsList.innerHTML = html;
}

function populateJobMatch() {
  const matchedSkillsContainer = document.getElementById('matchedSkills');
  const missingSkillsContainer = document.getElementById('missingSkills');
  
  if (matchedSkillsContainer) {
    matchedSkillsContainer.innerHTML = sampleData.jobMatch.matched_skills
      .map(skill => `<span class="skill-tag matched">${skill}</span>`).join('');
  }
  
  if (missingSkillsContainer) {
    missingSkillsContainer.innerHTML = sampleData.jobMatch.missing_skills
      .map(skill => `<span class="skill-tag missing">${skill}</span>`).join('');
  }
}

// Job Matching
function analyzeMatch() {
  console.log('Analyzing job match...');
  const jobDescription = document.getElementById('jobDescription');
  const jobDescriptionValue = jobDescription ? jobDescription.value.trim() : '';
  
  if (!jobDescriptionValue) {
    showToast('Missing Job Description', 'Please enter a job description to analyze.', 'warning');
    return;
  }

  showToast('Analyzing Match', 'Processing job match analysis...', 'info');
  
  // Simulate analysis delay
  setTimeout(() => {
    showToast('Analysis Complete', 'Job match analysis completed successfully!', 'success');
  }, 2000);
}

// Charts Initialization
function initializeCharts() {
  if (typeof Chart === 'undefined') {
    console.warn('Chart.js not loaded, skipping chart initialization');
    return;
  }
  
  try {
    initializeSuccessChart();
    initializeSkillsChart();
    initializePerformanceChart();
  } catch (error) {
    console.warn('Chart initialization failed:', error);
  }
}

function initializeSuccessChart() {
  const ctx = document.getElementById('successChart');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Successful', 'Failed'],
      datasets: [{
        data: [sampleData.analytics.successful_parses, sampleData.analytics.failed_parses],
        backgroundColor: ['#1FB8CD', '#B4413C'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}

function initializeSkillsChart() {
  const ctx = document.getElementById('skillsChart');
  if (!ctx) return;

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: sampleData.analytics.top_skills.map(s => s.skill),
      datasets: [{
        label: 'Frequency',
        data: sampleData.analytics.top_skills.map(s => s.count),
        backgroundColor: ['#1FB8CD', '#FFC185', '#B4413C', '#ECEBD5', '#5D878F'],
        borderWidth: 0
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        legend: {
          display: false
        }
      }
    }
  });
}

function initializePerformanceChart() {
  const ctx = document.getElementById('performanceChart');
  if (!ctx) return;

  const mockData = [28, 32, 35, 29, 31, 33, 30];
  const labels = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

  new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Processing Time (seconds)',
        data: mockData,
        borderColor: '#1FB8CD',
        backgroundColor: 'rgba(31, 184, 205, 0.1)',
        tension: 0.4,
        fill: true
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}

// Tab Management
function showTab(tabName) {
  console.log('Showing tab:', tabName);
  
  // Hide all tab contents
  document.querySelectorAll('.tab-content').forEach(content => {
    content.classList.remove('active');
    content.classList.add('hidden');
  });

  // Remove active class from all tab buttons
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.classList.remove('active');
  });

  // Show target tab content
  const targetContent = document.getElementById(tabName + 'Tab');
  if (targetContent) {
    targetContent.classList.add('active');
    targetContent.classList.remove('hidden');
  }

  // Add active class to clicked tab button - find by onclick attribute content
  const activeBtn = document.querySelector(`.tab-btn[onclick*="${tabName}"]`);
  if (activeBtn) {
    activeBtn.classList.add('active');
  }
}

// Modal Management
function openModal(modalId) {
  console.log('Opening modal:', modalId);
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.remove('hidden');
    document.body.style.overflow = 'hidden';
  }
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.classList.add('hidden');
    document.body.style.overflow = '';
  }
}

// Settings Management
function showSettingsTab(tabName) {
  console.log('Showing settings tab:', tabName);
  
  // Hide all settings tab contents
  document.querySelectorAll('.settings-tab-content').forEach(content => {
    content.classList.remove('active');
    content.classList.add('hidden');
  });

  // Remove active class from all settings tab buttons
  document.querySelectorAll('.settings-tab').forEach(btn => {
    btn.classList.remove('active');
  });

  // Show target settings tab content
  const targetContent = document.getElementById(tabName + 'Settings');
  if (targetContent) {
    targetContent.classList.add('active');
    targetContent.classList.remove('hidden');
  }

  // Add active class to clicked tab button
  const activeBtn = document.querySelector(`.settings-tab[onclick*="${tabName}"]`);
  if (activeBtn) {
    activeBtn.classList.add('active');
  }
}

function saveSettings() {
  const themeSelect = document.getElementById('themeSelect');
  if (themeSelect) {
    theme = themeSelect.value;
    applyTheme(theme);
    localStorage.setItem('theme', theme);
    updateThemeIcon();
  }

  showToast('Settings Saved', 'Your preferences have been updated.', 'success');
  closeModal('settingsModal');
}

// Export Functions
function exportResults(format) {
  console.log('Exporting results as:', format);
  
  const data = sampleData.parsedResume.parsed_data;
  let content, filename, mimeType;

  if (format === 'json') {
    content = JSON.stringify(data, null, 2);
    filename = 'resume_data.json';
    mimeType = 'application/json';
  } else if (format === 'csv') {
    content = convertToCSV(data);
    filename = 'resume_data.csv';
    mimeType = 'text/csv';
  }

  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  link.href = url;
  link.download = filename;
  link.click();
  URL.revokeObjectURL(url);

  showToast('Export Complete', `Data exported as ${format.toUpperCase()}.`, 'success');
}

// Toast Notifications
function showToast(title, message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <div class="toast-content">
      <div class="toast-title">${title}</div>
      <div class="toast-message">${message}</div>
    </div>
    <button class="toast-close">
      <span class="material-icons">close</span>
    </button>
  `;

  // Add close functionality
  const closeBtn = toast.querySelector('.toast-close');
  closeBtn.addEventListener('click', () => toast.remove());

  container.appendChild(toast);

  // Auto-remove after 5 seconds
  setTimeout(() => {
    if (toast.parentElement) {
      toast.remove();
    }
  }, 5000);
}

// Utility Functions
function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function formatLabel(key) {
  return key.replace(/_/g, ' ')
    .split(' ')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ');
}

function formatValue(key, value) {
  if (key === 'email') {
    return `<a href="mailto:${value}" target="_blank">${value}</a>`;
  }
  if (key === 'phone') {
    return `<a href="tel:${value}">${value}</a>`;
  }
  if (key.includes('linkedin') || key.includes('github') || key.includes('website')) {
    return `<a href="${value}" target="_blank">${value}</a>`;
  }
  return value;
}

function formatDuration(startDate, endDate) {
  const start = new Date(startDate + '-01');
  const end = endDate === 'present' ? new Date() : new Date(endDate + '-01');
  const months = (end.getFullYear() - start.getFullYear()) * 12 + (end.getMonth() - start.getMonth());
  const years = Math.floor(months / 12);
  const remainingMonths = months % 12;
  
  let duration = '';
  if (years > 0) duration += `${years} year${years > 1 ? 's' : ''}`;
  if (remainingMonths > 0) {
    if (duration) duration += ' ';
    duration += `${remainingMonths} month${remainingMonths > 1 ? 's' : ''}`;
  }
  
  return duration || '1 month';
}

function formatDate(dateStr) {
  const date = new Date(dateStr + '-01');
  return date.toLocaleDateString('en-US', { year: 'numeric', month: 'long' });
}

function convertToCSV(data) {
  const headers = ['Field', 'Value'];
  const rows = [headers.join(',')];
  
  function addRows(obj, prefix = '') {
    for (const [key, value] of Object.entries(obj)) {
      const fieldName = prefix ? `${prefix}.${key}` : key;
      if (typeof value === 'object' && value !== null && !Array.isArray(value)) {
        addRows(value, fieldName);
      } else {
        const cellValue = Array.isArray(value) ? value.join('; ') : String(value);
        rows.push(`"${fieldName}","${cellValue.replace(/"/g, '""')}"`);
      }
    }
  }
  
  addRows(data);
  return rows.join('\n');
}

// Global functions for backwards compatibility
window.showSection = showSection;
window.showTab = showTab;
window.showSettingsTab = showSettingsTab;
window.openModal = openModal;
window.closeModal = closeModal;
window.saveSettings = saveSettings;
window.exportResults = exportResults;
window.analyzeMatch = analyzeMatch;
window.clearQueue = clearQueue;
window.processAll = processAll;
window.removeFromQueue = removeFromQueue;