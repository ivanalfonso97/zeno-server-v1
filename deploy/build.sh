# Upgrade Resources
pip install --upgrade pip
pip install uv

# Install dependencies
echo "Installing dependencies..."
source "${VENV_ROOT}/bin/activate"
uv sync