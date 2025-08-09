# Scripts Directory

This directory contains development and utility scripts for the ALX Project Nexus.

## Files:

### `dev.sh`
Main development environment setup script. Activates virtual environment and provides an interactive development shell.

**Usage:**
```bash
./scripts/dev.sh                    # Interactive shell
./scripts/dev.sh python manage.py runserver  # Run specific command
```

### `activate_env.sh`
Quick virtual environment activation script.

**Usage:**
```bash
source ./scripts/activate_env.sh
```

### `quick_activate.sh`
Alternative quick activation script.

**Usage:**
```bash
source ./scripts/quick_activate.sh
```

### `setup_aliases.sh`
Sets up useful command aliases for development.

**Usage:**
```bash
source ./scripts/setup_aliases.sh
```

## Note:
These scripts are for local development only and are excluded from version control via `.gitignore`.
