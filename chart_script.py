import plotly.graph_objects as go

# Create a comprehensive system architecture diagram
fig = go.Figure()

# Define layers with exact specifications from instructions
layers = [
    {
        "name": "Frontend Layer",
        "components": ["React Web App", "Mobile PWA", "API Docs"],
        "color": "#1FB8CD",
        "y_position": 7
    },
    {
        "name": "Gateway Layer", 
        "components": ["NGINX Load Bal", "SSL Termination", "Rate Limiting"],
        "color": "#DB4545",
        "y_position": 6
    },
    {
        "name": "Application Layer",
        "components": ["FastAPI Resume", "Job Matcher", "User Mgmt", "Webhook Svc"],
        "color": "#2E8B57",
        "y_position": 5
    },
    {
        "name": "Processing Layer",
        "components": ["Celery Workers", "NLP BERT/spaCy", "OCR Service", "ML Models"],
        "color": "#5D878F",
        "y_position": 4
    },
    {
        "name": "Data Layer",
        "components": ["PostgreSQL", "Redis Cache", "MinIO/S3 Store", "Search Index"],
        "color": "#D2BA4C",
        "y_position": 3
    },
    {
        "name": "Monitoring Layer",
        "components": ["Prometheus", "Grafana Dash", "ELK Logging", "Sentry Errors"],
        "color": "#B4413C",
        "y_position": 2
    },
    {
        "name": "Infrastructure",
        "components": ["Docker", "Kubernetes", "Orchestration"],
        "color": "#964325",
        "y_position": 1
    }
]

# Create layer backgrounds and components with better spacing
for layer in layers:
    y_pos = layer["y_position"]
    num_components = len(layer["components"])
    
    # Add wider layer background rectangle
    fig.add_shape(
        type="rect",
        x0=-1.2, y0=y_pos-0.45,
        x1=num_components*1.8-0.2, y1=y_pos+0.45,
        fillcolor=layer["color"],
        opacity=0.15,
        line=dict(color=layer["color"], width=2)
    )
    
    # Add layer title with better styling
    fig.add_annotation(
        x=-0.9, y=y_pos,
        text=f"<b>{layer['name']}</b>",
        showarrow=False,
        font=dict(size=14, color=layer["color"]),
        xanchor="center",
        bgcolor="white",
        bordercolor=layer["color"],
        borderwidth=2,
        borderpad=4
    )
    
    # Add component boxes with better spacing
    for i, component in enumerate(layer["components"]):
        x_pos = i * 1.8
        
        # Component rectangle
        fig.add_shape(
            type="rect",
            x0=x_pos-0.7, y0=y_pos-0.35,
            x1=x_pos+0.7, y1=y_pos+0.35,
            fillcolor=layer["color"],
            opacity=0.9,
            line=dict(color="white", width=2)
        )
        
        # Component text with better contrast
        fig.add_annotation(
            x=x_pos, y=y_pos,
            text=f"<b>{component}</b>",
            showarrow=False,
            font=dict(size=11, color="white"),
            bgcolor="rgba(0,0,0,0)"
        )

# Add prominent data flow arrows with labels
flow_data = [
    {"from_y": 7, "to_y": 6, "label": "HTTP/HTTPS", "x": 2.7, "color": "#1FB8CD"},
    {"from_y": 6, "to_y": 5, "label": "Load Balanced", "x": 3.6, "color": "#DB4545"},
    {"from_y": 5, "to_y": 4, "label": "Async Tasks", "x": 1.8, "color": "#2E8B57"},
    {"from_y": 4, "to_y": 3, "label": "Query/Store", "x": 2.7, "color": "#5D878F"},
    {"from_y": 3, "to_y": 2, "label": "Metrics/Logs", "x": 3.6, "color": "#D2BA4C"},
    {"from_y": 2, "to_y": 1, "label": "Deploy/Scale", "x": 1.8, "color": "#B4413C"}
]

# Add main data flow arrows
for flow in flow_data:
    # Large prominent arrow
    fig.add_annotation(
        x=flow["x"], y=flow["from_y"] - 0.5,
        ax=flow["x"], ay=flow["to_y"] + 0.5,
        arrowhead=2,
        arrowsize=2,
        arrowwidth=4,
        arrowcolor=flow["color"],
        showarrow=True,
        text=""
    )
    
    # Flow type label with better visibility
    mid_y = (flow["from_y"] + flow["to_y"]) / 2
    fig.add_annotation(
        x=flow["x"] + 0.9, y=mid_y,
        text=f"<b>{flow['label']}</b>",
        showarrow=False,
        font=dict(size=10, color=flow["color"]),
        bgcolor="white",
        bordercolor=flow["color"],
        borderwidth=2,
        borderpad=3
    )

# Add monitoring data flows (bidirectional)
monitoring_sources = [7, 6, 5, 4, 3, 1]  # All layers except monitoring
for source_y in monitoring_sources:
    fig.add_annotation(
        x=5.4, y=source_y,
        ax=5.4, ay=2,
        arrowhead=1,
        arrowsize=1.5,
        arrowwidth=2,
        arrowcolor="#B4413C",
        opacity=0.7,
        showarrow=True,
        text=""
    )

# Add monitoring label
fig.add_annotation(
    x=6.2, y=4.5,
    text="<b>All Layers →<br>Monitoring</b>",
    showarrow=False,
    font=dict(size=10, color="#B4413C"),
    bgcolor="white",
    bordercolor="#B4413C",
    borderwidth=2,
    borderpad=3
)

# Add data flow legend
fig.add_annotation(
    x=0.5, y=0.2,
    text="<b>Data Flow Types:</b><br>• HTTP/HTTPS Requests<br>• Load Balanced Traffic<br>• Async Task Queues<br>• Database Queries<br>• Metrics & Logs<br>• Container Management",
    showarrow=False,
    font=dict(size=9, color="#13343B"),
    bgcolor="rgba(255,255,255,0.95)",
    bordercolor="#13343B",
    borderwidth=1,
    borderpad=5,
    align="left"
)

# Configure layout with better spacing
fig.update_layout(
    title="Resume Parser 2025 System Architecture",
    showlegend=False,
    xaxis=dict(
        range=[-1.5, 7.5],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    yaxis=dict(
        range=[0, 8],
        showgrid=False,
        showticklabels=False,
        zeroline=False
    ),
    plot_bgcolor="white",
    paper_bgcolor="white"
)

# Save as both PNG and SVG
fig.write_image("chart.png")
fig.write_image("chart.svg", format="svg")

fig.show()