#!/bin/bash

# Firefly SBOM Tool Installation Script
# Copyright 2024 Firefly OSS
# Licensed under the Apache License, Version 2.0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
TOOL_NAME="Firefly SBOM Tool"
GITHUB_REPO="firefly-oss/sbom-tool"
INSTALL_DIR="${HOME}/.local/bin"
VENV_DIR="${HOME}/.firefly-sbom"
MIN_PYTHON_VERSION="3.8"

# Functions
print_banner() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║     Firefly SBOM Tool Installation        ║${NC}"
    echo -e "${BLUE}║         Apache License 2.0                ║${NC}"
    echo -e "${BLUE}╚════════════════════════════════════════════╝${NC}"
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

check_command() {
    if command -v "$1" &> /dev/null; then
        return 0
    else
        return 1
    fi
}

check_python_version() {
    local python_cmd=$1
    local version=$($python_cmd -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    local required_version=$MIN_PYTHON_VERSION
    
    if [ "$(printf '%s\n' "$required_version" "$version" | sort -V | head -n1)" = "$required_version" ]; then
        return 0
    else
        return 1
    fi
}

find_python() {
    # Try to find suitable Python installation
    for cmd in python3 python python3.11 python3.10 python3.9 python3.8; do
        if check_command "$cmd"; then
            if check_python_version "$cmd"; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    return 1
}

install_dependencies() {
    print_info "Checking system dependencies..."
    
    # Check for Python
    PYTHON_CMD=$(find_python)
    if [ $? -ne 0 ]; then
        print_error "Python ${MIN_PYTHON_VERSION}+ is required but not found"
        print_info "Please install Python ${MIN_PYTHON_VERSION} or higher and try again"
        exit 1
    fi
    print_success "Found Python: $PYTHON_CMD"
    
    # Check for pip
    if ! $PYTHON_CMD -m pip --version &> /dev/null; then
        print_warning "pip not found, attempting to install..."
        $PYTHON_CMD -m ensurepip --default-pip || {
            print_error "Failed to install pip"
            exit 1
        }
    fi
    print_success "pip is available"
    
    # Check for Git
    if ! check_command git; then
        print_error "Git is required but not found"
        print_info "Please install Git and try again"
        exit 1
    fi
    print_success "Git is available"
    
    # Check for optional tools and provide recommendations
    print_info "Checking optional dependencies for enhanced functionality..."
    
    local optional_tools=(
        "maven:Java/Maven project scanning"
        "npm:Node.js/TypeScript project scanning"
        "go:Go project scanning"
        "flutter:Flutter/Dart project scanning"
        "cargo:Rust project scanning"
        "bundle:Ruby project scanning"
    )
    
    for tool_info in "${optional_tools[@]}"; do
        IFS=':' read -r tool description <<< "$tool_info"
        if check_command "$tool"; then
            print_success "$tool is available - $description will be enhanced"
        else
            print_warning "$tool not found - $description will use fallback parsing"
        fi
    done
}

create_directories() {
    print_info "Creating installation directories..."
    
    # Create local bin directory if it doesn't exist
    mkdir -p "$INSTALL_DIR"
    
    # Create virtual environment directory
    mkdir -p "$VENV_DIR"
    
    print_success "Directories created"
}

install_from_source() {
    local source_dir=$1
    
    print_info "Installing from source directory: $source_dir"
    
    # Create virtual environment
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    # Install the package
    print_info "Installing Firefly SBOM Tool..."
    cd "$source_dir"
    pip install -e .
    
    # Create wrapper script
    create_wrapper_script
    
    print_success "Installation from source completed"
}

install_from_pypi() {
    print_info "Installing from PyPI..."
    
    # Create virtual environment
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    # Install the package
    print_info "Installing Firefly SBOM Tool..."
    pip install firefly-sbom-tool
    
    # Create wrapper script
    create_wrapper_script
    
    print_success "Installation from PyPI completed"
}

install_from_github() {
    print_info "Installing from GitHub..."
    
    # Create virtual environment first
    print_info "Creating virtual environment..."
    $PYTHON_CMD -m venv "$VENV_DIR"
    
    # Activate virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Upgrade pip
    pip install --upgrade pip setuptools wheel
    
    # Install directly from GitHub
    print_info "Installing Firefly SBOM Tool from GitHub..."
    pip install "git+https://github.com/${GITHUB_REPO}.git"
    
    # Create wrapper script
    create_wrapper_script
    
    print_success "Installation from GitHub completed"
}

create_wrapper_script() {
    print_info "Creating wrapper script..."
    
    cat > "$INSTALL_DIR/firefly-sbom" << 'EOF'
#!/bin/bash
# Firefly SBOM Tool wrapper script

VENV_DIR="${HOME}/.firefly-sbom"

if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please run the install script again"
    exit 1
fi

# Activate virtual environment and run the tool
source "$VENV_DIR/bin/activate"
exec python -m firefly_sbom.cli "$@"
EOF
    
    chmod +x "$INSTALL_DIR/firefly-sbom"
    print_success "Wrapper script created"
}

update_path() {
    print_info "Updating PATH configuration..."
    
    # Detect shell
    local shell_rc=""
    if [ -n "$ZSH_VERSION" ]; then
        shell_rc="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        shell_rc="$HOME/.bashrc"
    else
        shell_rc="$HOME/.profile"
    fi
    
    # Check if PATH already contains install directory
    if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        echo "" >> "$shell_rc"
        echo "# Firefly SBOM Tool" >> "$shell_rc"
        echo "export PATH=\"\$PATH:$INSTALL_DIR\"" >> "$shell_rc"
        print_success "PATH updated in $shell_rc"
        print_warning "Please run 'source $shell_rc' or restart your terminal"
    else
        print_success "PATH already contains $INSTALL_DIR"
    fi
}

verify_installation() {
    print_info "Verifying installation..."
    
    # Check if wrapper script exists
    if [ ! -f "$INSTALL_DIR/firefly-sbom" ]; then
        print_error "Installation verification failed: wrapper script not found"
        return 1
    fi
    
    # Try to run the tool
    if "$INSTALL_DIR/firefly-sbom" --version &> /dev/null; then
        local version=$("$INSTALL_DIR/firefly-sbom" --version 2>&1 | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
        print_success "Firefly SBOM Tool v${version} installed successfully"
        return 0
    else
        print_error "Installation verification failed: tool not working"
        return 1
    fi
}

install_completion() {
    print_info "Installing shell completions..."
    
    # Create completions directory if it doesn't exist
    local completion_dir=""
    
    if [ -n "$ZSH_VERSION" ]; then
        completion_dir="$HOME/.zsh/completions"
        mkdir -p "$completion_dir"
        
        # Generate completion script for zsh
        cat > "$completion_dir/_firefly-sbom" << 'EOF'
#compdef firefly-sbom

_firefly-sbom() {
    local -a commands
    commands=(
        'scan:Scan a single repository'
        'scan-org:Scan entire GitHub organization'
        'detect:Detect technology stack'
        'init:Initialize configuration'
    )
    
    _arguments \
        '1: :->command' \
        '*::arg:->args'
    
    case $state in
        command)
            _describe 'command' commands
            ;;
    esac
}
EOF
        print_success "Zsh completions installed"
        
    elif [ -n "$BASH_VERSION" ]; then
        completion_dir="$HOME/.local/share/bash-completion/completions"
        mkdir -p "$completion_dir"
        
        # Generate completion script for bash
        cat > "$completion_dir/firefly-sbom" << 'EOF'
_firefly_sbom_completion() {
    local cur prev commands
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    commands="scan scan-org detect init --help --version"
    
    if [ $COMP_CWORD -eq 1 ]; then
        COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
    fi
    
    return 0
}
complete -F _firefly_sbom_completion firefly-sbom
EOF
        print_success "Bash completions installed"
    fi
}

show_usage() {
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --source DIR    Install from source directory"
    echo "  --github        Install from GitHub (default)"
    echo "  --pypi          Install from PyPI"
    echo "  --no-path       Don't update PATH"
    echo "  --no-completion Don't install shell completions"
    echo "  --help          Show this help message"
    echo ""
}

main() {
    # Parse arguments
    INSTALL_METHOD="github"
    SOURCE_DIR=""
    UPDATE_PATH=true
    INSTALL_COMPLETION=true
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --source)
                INSTALL_METHOD="source"
                SOURCE_DIR="$2"
                shift 2
                ;;
            --github)
                INSTALL_METHOD="github"
                shift
                ;;
            --pypi)
                INSTALL_METHOD="pypi"
                shift
                ;;
            --no-path)
                UPDATE_PATH=false
                shift
                ;;
            --no-completion)
                INSTALL_COMPLETION=false
                shift
                ;;
            --help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
    
    # Print banner
    print_banner
    
    # Check dependencies
    install_dependencies
    
    # Create directories
    create_directories
    
    # Install based on method
    case $INSTALL_METHOD in
        source)
            if [ -z "$SOURCE_DIR" ] || [ ! -d "$SOURCE_DIR" ]; then
                print_error "Source directory not specified or doesn't exist"
                exit 1
            fi
            install_from_source "$SOURCE_DIR"
            ;;
        github)
            install_from_github
            ;;
        pypi)
            install_from_pypi
            ;;
    esac
    
    # Update PATH if requested
    if [ "$UPDATE_PATH" = true ]; then
        update_path
    fi
    
    # Install completions if requested
    if [ "$INSTALL_COMPLETION" = true ]; then
        install_completion
    fi
    
    # Verify installation
    verify_installation
    
    # Print success message
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║     Installation Completed Successfully!   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
    echo ""
    print_info "Quick start:"
    echo ""
    echo "  # Scan a single repository"
    echo "  firefly-sbom scan --path /path/to/repo"
    echo ""
    echo "  # Scan a GitHub organization"
    echo "  firefly-sbom scan-org --org firefly-oss"
    echo ""
    echo "  # Get help"
    echo "  firefly-sbom --help"
    echo ""
    
    if [ "$UPDATE_PATH" = true ] && [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
        print_warning "Remember to reload your shell or run: source ~/.bashrc (or ~/.zshrc)"
    fi
}

# Run main function
main "$@"
