# Create the main directory structure for the resume parser project
import os
import json

project_structure = {
    "resume_parser_2025/": {
        "backend/": {
            "app/": {
                "__init__.py": "",
                "main.py": "",
                "config.py": "",
                "models/": {
                    "__init__.py": "",
                    "resume.py": "",
                    "candidate.py": "",
                    "job.py": ""
                },
                "api/": {
                    "__init__.py": "",
                    "v1/": {
                        "__init__.py": "",
                        "endpoints/": {
                            "__init__.py": "",
                            "resume_parser.py": "",
                            "candidates.py": "",
                            "jobs.py": "",
                            "webhooks.py": ""
                        }
                    }
                },
                "services/": {
                    "__init__.py": "",
                    "nlp_service.py": "",
                    "ocr_service.py": "",
                    "matching_service.py": "",
                    "storage_service.py": ""
                },
                "tasks/": {
                    "__init__.py": "",
                    "celery_app.py": "",
                    "parsing_tasks.py": ""
                },
                "utils/": {
                    "__init__.py": "",
                    "file_handler.py": "",
                    "validators.py": "",
                    "security.py": ""
                }
            },
            "ml_models/": {
                "ner_model/": {},
                "skills_taxonomy/": {},
                "trained_models/": {}
            },
            "tests/": {
                "__init__.py": "",
                "test_api.py": "",
                "test_services.py": "",
                "test_models.py": ""
            },
            "requirements.txt": "",
            "Dockerfile": "",
            "docker-compose.yml": ""
        },
        "frontend/": {
            "public/": {},
            "src/": {
                "components/": {},
                "pages/": {},
                "services/": {},
                "utils/": {}
            },
            "package.json": "",
            "Dockerfile": ""
        },
        "deployment/": {
            "kubernetes/": {},
            "terraform/": {},
            "monitoring/": {}
        },
        "docs/": {
            "api/": {},
            "architecture/": {},
            "deployment/": {}
        },
        "scripts/": {},
        "README.md": "",
        ".env.example": "",
        ".gitignore": ""
    }
}

def create_structure(base_path, structure):
    """Create the project directory structure"""
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # Create file
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)

# Create the project structure
create_structure(".", project_structure)
print("✅ Project structure created successfully!")

# List the created structure
def list_structure(path, level=0):
    items = []
    for item in sorted(os.listdir(path)):
        item_path = os.path.join(path, item)
        indent = "  " * level
        if os.path.isdir(item_path):
            items.append(f"{indent}{item}/")
            items.extend(list_structure(item_path, level + 1))
        else:
            items.append(f"{indent}{item}")
    return items

structure_list = list_structure("resume_parser_2025")
print("\n📁 Created project structure:")
for item in structure_list[:50]:  # Show first 50 items
    print(item)
if len(structure_list) > 50:
    print(f"... and {len(structure_list) - 50} more files/folders")