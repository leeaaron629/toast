# Toast

A Python package for Git operations management.

## Installation

```bash
pip install -e .
```

## Usage

```python
from toast import GitOperations

# Initialize with SSH key
git_ops = GitOperations(base_path="./repos", ssh_key_path="~/.ssh/id_rsa")
```

## Development

1. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run tests:
```bash
python -m unittest discover tests
```

## License

MIT License - See LICENSE file for details