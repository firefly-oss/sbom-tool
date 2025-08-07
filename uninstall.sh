#!/bin/bash

# Firefly SBOM Tool Uninstallation Script
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
INSTALL_DIR="${HOME}/.local/bin"
VENV_DIR="${HOME}/.firefly-sbom"
WRAPPER_SCRIPT="$INSTALL_DIR/firefly-sbom"

# Functions
print_banner() {
    echo ""
    echo -e "${BLUE}╔════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║    Firefly SBOM Tool Uninstallation       ║${NC}"
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

check_installation() {
    local found=false
    
    print_info "Checking for existing installation..."
    
    if [ -d "$VENV_DIR" ]; then
        print_success "Found virtual environment at $VENV_DIR"
        found=true
    else
        print_warning "Virtual environment not found at $VENV_DIR"
    fi
    
    if [ -f "$WRAPPER_SCRIPT" ]; then
        print_success "Found wrapper script at $WRAPPER_SCRIPT"
        found=true
    else
        print_warning "Wrapper script not found at $WRAPPER_SCRIPT"
    fi
    
    if [ "$found" = false ]; then
        print_error "No Firefly SBOM Tool installation found"
        exit 1
    fi
}

confirm_uninstall() {
    echo ""
    print_warning "This will remove the following:"
    echo "  • Virtual environment at $VENV_DIR"
    echo "  • Wrapper script at $WRAPPER_SCRIPT"
    echo "  • Shell completions (if installed)"
    echo "  • PATH entries (if added)"
    echo ""
    
    read -p "Are you sure you want to uninstall Firefly SBOM Tool? (y/N): " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Uninstallation cancelled"
        exit 0
    fi
}

remove_virtual_environment() {
    print_info "Removing virtual environment..."
    
    if [ -d "$VENV_DIR" ]; then
        rm -rf "$VENV_DIR"
        print_success "Virtual environment removed"
    else
        print_warning "Virtual environment not found"
    fi
}

remove_wrapper_script() {
    print_info "Removing wrapper script..."
    
    if [ -f "$WRAPPER_SCRIPT" ]; then
        rm -f "$WRAPPER_SCRIPT"
        print_success "Wrapper script removed"
    else
        print_warning "Wrapper script not found"
    fi
}

remove_completions() {
    print_info "Removing shell completions..."
    
    local removed=false
    
    # Remove zsh completions
    if [ -f "$HOME/.zsh/completions/_firefly-sbom" ]; then
        rm -f "$HOME/.zsh/completions/_firefly-sbom"
        print_success "Removed zsh completions"
        removed=true
    fi
    
    # Remove bash completions
    if [ -f "$HOME/.local/share/bash-completion/completions/firefly-sbom" ]; then
        rm -f "$HOME/.local/share/bash-completion/completions/firefly-sbom"
        print_success "Removed bash completions"
        removed=true
    fi
    
    if [ "$removed" = false ]; then
        print_warning "No shell completions found"
    fi
}

clean_path() {
    print_info "Cleaning PATH configuration..."
    
    local cleaned=false
    
    # Clean common shell configuration files
    for rc_file in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
        if [ -f "$rc_file" ]; then
            # Create backup
            cp "$rc_file" "${rc_file}.bak.$(date +%Y%m%d_%H%M%S)"
            
            # Remove PATH export lines for firefly-sbom
            if grep -q "Firefly SBOM Tool" "$rc_file"; then
                # Remove the comment line and the export line
                sed -i.tmp '/# Firefly SBOM Tool/d' "$rc_file"
                sed -i.tmp "/export PATH.*\.local\/bin/d" "$rc_file"
                rm -f "${rc_file}.tmp"
                
                print_success "Cleaned PATH configuration in $rc_file"
                cleaned=true
            fi
        fi
    done
    
    if [ "$cleaned" = false ]; then
        print_warning "No PATH configurations found to clean"
    else
        print_info "Backup files created with .bak extension"
    fi
}

remove_cache() {
    print_info "Removing cache and temporary files..."
    
    local cache_removed=false
    
    # Remove any cache directories
    if [ -d "$HOME/.cache/firefly-sbom" ]; then
        rm -rf "$HOME/.cache/firefly-sbom"
        print_success "Removed cache directory"
        cache_removed=true
    fi
    
    # Remove any config files
    if [ -f "$HOME/.config/firefly-sbom/config.yml" ]; then
        read -p "Remove configuration file? (y/N): " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$HOME/.config/firefly-sbom"
            print_success "Removed configuration directory"
            cache_removed=true
        else
            print_info "Configuration directory preserved"
        fi
    fi
    
    if [ "$cache_removed" = false ]; then
        print_info "No cache or temporary files found"
    fi
}

verify_uninstall() {
    print_info "Verifying uninstallation..."
    
    local all_removed=true
    
    if [ -d "$VENV_DIR" ]; then
        print_error "Virtual environment still exists"
        all_removed=false
    fi
    
    if [ -f "$WRAPPER_SCRIPT" ]; then
        print_error "Wrapper script still exists"
        all_removed=false
    fi
    
    if command -v firefly-sbom &> /dev/null; then
        print_warning "firefly-sbom command still available in PATH"
        print_info "You may need to restart your terminal or run 'hash -r'"
    fi
    
    if [ "$all_removed" = true ]; then
        print_success "Uninstallation verified successfully"
        return 0
    else
        print_error "Some components were not removed properly"
        return 1
    fi
}

show_usage() {
    echo ""
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --force         Skip confirmation prompt"
    echo "  --keep-config   Keep configuration files"
    echo "  --help          Show this help message"
    echo ""
}

main() {
    # Parse arguments
    FORCE_UNINSTALL=false
    KEEP_CONFIG=false
    
    while [[ $# -gt 0 ]]; do
        case $1 in
            --force)
                FORCE_UNINSTALL=true
                shift
                ;;
            --keep-config)
                KEEP_CONFIG=true
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
    
    # Check for existing installation
    check_installation
    
    # Confirm uninstallation
    if [ "$FORCE_UNINSTALL" = false ]; then
        confirm_uninstall
    fi
    
    # Perform uninstallation steps
    remove_wrapper_script
    remove_virtual_environment
    remove_completions
    clean_path
    
    # Remove cache unless config should be kept
    if [ "$KEEP_CONFIG" = false ]; then
        remove_cache
    else
        print_info "Configuration files preserved"
    fi
    
    # Verify uninstallation
    verify_uninstall
    
    # Print success message
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   Uninstallation Completed Successfully!   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════════╝${NC}"
    echo ""
    print_info "Thank you for using Firefly SBOM Tool!"
    print_info "You can reinstall anytime by running the install.sh script"
    echo ""
    
    if command -v firefly-sbom &> /dev/null 2>&1; then
        print_warning "Note: You may need to restart your terminal for changes to take effect"
    fi
}

# Run main function
main "$@"
