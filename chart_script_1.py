import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Data from the provided JSON
data = {
  "project_status": {
    "overall_completion": 100,
    "total_features": 47,
    "completed_features": 47,
    "in_progress": 0,
    "planned": 0
  },
  "core_features": [
    {"name": "Multi-format Support", "status": "complete", "details": "PDF, DOCX, TXT, RTF, ODT, HTML"},
    {"name": "BERT NER Engine", "status": "complete", "details": "90.87% F1-score accuracy"},
    {"name": "OCR Integration", "status": "complete", "details": "Tesseract + Google Vision"},
    {"name": "Job Matching", "status": "complete", "details": "TF-IDF + Semantic Similarity"},
    {"name": "Real-time Processing", "status": "complete", "details": "<2 second response time"},
    {"name": "Async Task Queue", "status": "complete", "details": "Celery + Redis"},
    {"name": "Skills Extraction", "status": "complete", "details": "10,000+ skills taxonomy"},
    {"name": "Entity Recognition", "status": "complete", "details": "25+ entity types"}
  ],
  "performance_metrics": [
    {"metric": "Parsing Accuracy", "value": "90.87%", "target": "90%", "status": "exceeded"},
    {"metric": "Processing Speed", "value": "1.2-2.3s", "target": "2s", "status": "met"},
    {"metric": "Throughput", "value": "500+/min", "target": "300/min", "status": "exceeded"},
    {"metric": "Uptime Target", "value": "99.9%", "target": "99.5%", "status": "exceeded"},
    {"metric": "Contact Accuracy", "value": "96.5%", "target": "95%", "status": "exceeded"},
    {"metric": "Skills Recall", "value": "94.2%", "target": "90%", "status": "exceeded"}
  ],
  "technology_stack": [
    {"category": "Backend", "technologies": ["FastAPI", "Python 3.11", "SQLAlchemy", "Alembic"]},
    {"category": "AI/ML", "technologies": ["BERT", "spaCy", "Transformers", "scikit-learn"]},
    {"category": "Database", "technologies": ["PostgreSQL", "Redis", "Full-text Search"]},
    {"category": "Infrastructure", "technologies": ["Docker", "Kubernetes", "NGINX", "MinIO"]},
    {"category": "Monitoring", "technologies": ["Prometheus", "Grafana", "Sentry", "ELK Stack"]},
    {"category": "Frontend", "technologies": ["React", "Material-UI", "Chart.js", "WebSockets"]}
  ],
  "enterprise_features": [
    {"name": "GDPR Compliance", "status": "complete", "description": "Data retention, anonymization, consent"},
    {"name": "Authentication", "status": "complete", "description": "JWT with RBAC"},
    {"name": "Rate Limiting", "status": "complete", "description": "Per-user and IP-based limits"},
    {"name": "Audit Logging", "status": "complete", "description": "Complete activity tracking"},
    {"name": "Data Encryption", "status": "complete", "description": "At rest and in transit"},
    {"name": "Webhook Integration", "status": "complete", "description": "Real-time notifications"},
    {"name": "API Documentation", "status": "complete", "description": "OpenAPI/Swagger specs"},
    {"name": "Health Checks", "status": "complete", "description": "Kubernetes readiness probes"}
  ],
  "deployment_capabilities": [
    {"name": "Containerization", "status": "complete", "description": "Multi-stage Docker builds"},
    {"name": "Orchestration", "status": "complete", "description": "Kubernetes manifests"},
    {"name": "Auto-scaling", "status": "complete", "description": "HPA for API and workers"},
    {"name": "Load Balancing", "status": "complete", "description": "NGINX ingress"},
    {"name": "SSL/TLS", "status": "complete", "description": "Let's Encrypt integration"},
    {"name": "Monitoring", "status": "complete", "description": "Prometheus + Grafana"},
    {"name": "Backup Strategy", "status": "complete", "description": "Automated DB and file backups"},
    {"name": "CI/CD Ready", "status": "complete", "description": "Pipeline configurations"}
  ]
}

# Create a comprehensive dashboard-style visualization
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=['Core Features ✓', 'Performance Metrics ✓', 'Enterprise Features ✓', 
                   'Deployment ✓', 'Tech Stack ✓', 'Project Status ✓'],
    specs=[[{"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "indicator"}]],
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# Colors for different sections
colors = ['#2E8B57', '#1FB8CD', '#DB4545', '#5D878F', '#D2BA4C', '#B4413C']

# 1. Core Features
core_names = [f['name'][:12] for f in data['core_features']]
core_details = [f['details'] for f in data['core_features']]
fig.add_trace(
    go.Bar(x=core_names, y=[100]*len(core_names), 
           text=['✓'] * len(core_names),
           textposition='inside', textfont=dict(size=16, color='white'),
           marker_color=colors[0], name='Core Features',
           hovertemplate='<b>%{x}</b><br>%{customdata}<br><extra></extra>',
           customdata=core_details),
    row=1, col=1
)

# 2. Performance Metrics with actual values
perf_names = [m['metric'][:12] for m in data['performance_metrics']]
perf_values = [m['value'] for m in data['performance_metrics']]
perf_status = ['✓✓' if m['status'] == 'exceeded' else '✓' for m in data['performance_metrics']]
fig.add_trace(
    go.Bar(x=perf_names, y=[100]*len(perf_names),
           text=perf_status,
           textposition='inside', textfont=dict(size=16, color='white'),
           marker_color=colors[1], name='Performance',
           hovertemplate='<b>%{x}</b><br>Value: %{customdata}<br><extra></extra>',
           customdata=perf_values),
    row=1, col=2
)

# 3. Enterprise Features
ent_names = [f['name'][:12] for f in data['enterprise_features']]
ent_desc = [f['description'] for f in data['enterprise_features']]
fig.add_trace(
    go.Bar(x=ent_names, y=[100]*len(ent_names),
           text=['✓'] * len(ent_names),
           textposition='inside', textfont=dict(size=16, color='white'),
           marker_color=colors[2], name='Enterprise',
           hovertemplate='<b>%{x}</b><br>%{customdata}<br><extra></extra>',
           customdata=ent_desc),
    row=2, col=1
)

# 4. Deployment Features
dep_names = [f['name'][:12] for f in data['deployment_capabilities']]
dep_desc = [f['description'] for f in data['deployment_capabilities']]
fig.add_trace(
    go.Bar(x=dep_names, y=[100]*len(dep_names),
           text=['✓'] * len(dep_names),
           textposition='inside', textfont=dict(size=16, color='white'),
           marker_color=colors[3], name='Deployment',
           hovertemplate='<b>%{x}</b><br>%{customdata}<br><extra></extra>',
           customdata=dep_desc),
    row=2, col=2
)

# 5. Technology Stack
tech_list = []
tech_categories = []
for cat in data['technology_stack']:
    for tech in cat['technologies']:
        tech_list.append(tech[:10])
        tech_categories.append(cat['category'])

# Show top 8 technologies
tech_display = tech_list[:8]
cat_display = tech_categories[:8]
fig.add_trace(
    go.Bar(x=tech_display, y=[100]*len(tech_display),
           text=['✓'] * len(tech_display),
           textposition='inside', textfont=dict(size=16, color='white'),
           marker_color=colors[4], name='Tech Stack',
           hovertemplate='<b>%{x}</b><br>Category: %{customdata}<br><extra></extra>',
           customdata=cat_display),
    row=3, col=1
)

# 6. Project Status Indicator
fig.add_trace(
    go.Indicator(
        mode = "gauge+number+delta",
        value = 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Complete"},
        delta = {'reference': 95},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': colors[0]},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': colors[0]}],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90}}
    ),
    row=3, col=2
)

# Update layout
fig.update_layout(
    title_text="Resume Parser 2025 Feature Matrix",
    showlegend=False,
    height=1000
)

# Update all bar chart y-axes to show percentage
for i in range(1, 4):
    for j in range(1, 3):
        if not (i == 3 and j == 2):  # Skip the gauge chart
            fig.update_yaxes(range=[0, 105], ticksuffix='%', row=i, col=j)
            fig.update_xaxes(tickangle=45, row=i, col=j)

# Add key metrics as annotations
key_metrics = [
    "90.87% F1-score",
    "500+ resumes/min", 
    "99.9% uptime",
    "47/47 features ✓"
]

for i, metric in enumerate(key_metrics):
    fig.add_annotation(
        text=metric,
        xref="paper", yref="paper",
        x=0.02 + (i * 0.24), y=0.02,
        showarrow=False,
        font=dict(size=12, color='#2E8B57'),
        bgcolor='rgba(46, 139, 87, 0.1)',
        bordercolor='#2E8B57',
        borderwidth=1
    )

# Apply cliponaxis only to bar traces
for trace in fig.data:
    if trace.type == 'bar':
        trace.update(cliponaxis=False)

# Save the chart
fig.write_image("resume_parser_dashboard.png")
fig.write_image("resume_parser_dashboard.svg", format="svg")

fig.show()