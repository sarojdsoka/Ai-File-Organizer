#!/bin/bash

# AI File Organizer - Easy wrapper script
# Supports multiple AI providers for smart file organization

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/organizer.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

show_banner() {
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║     🤖 AI File Organizer & Analyzer - Interactive Mode   ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

check_dependencies() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is not installed${NC}"
        exit 1
    fi
}

list_ai_providers() {
    python3 "$PYTHON_SCRIPT" --list-ai
}

show_ai_setup() {
    echo -e "${YELLOW}🔑 AI Provider Setup Instructions${NC}"
    echo ""
    
    echo -e "${GREEN}1. Groq (Recommended - Fast & Free Tier Available)${NC}"
    echo "   • Sign up: https://console.groq.com/"
    echo "   • Get API key from: https://console.groq.com/keys"
    echo "   • Add to .zshrc: export GROQ_API_KEY='your-key-here'"
    echo "   • Then run: source ~/.zshrc"
    echo ""
    
    echo -e "${GREEN}2. OpenAI${NC}"
    echo "   • Sign up: https://platform.openai.com/"
    echo "   • Get API key from: https://platform.openai.com/api-keys"
    echo "   • Add to .zshrc: export OPENAI_API_KEY='your-key-here'"
    echo "   • Then run: source ~/.zshrc"
    echo ""
    
    echo -e "${GREEN}3. Anthropic (Claude)${NC}"
    echo "   • Sign up: https://console.anthropic.com/"
    echo "   • Get API key from: https://console.anthropic.com/settings/keys"
    echo "   • Add to .zshrc: export ANTHROPIC_API_KEY='your-key-here'"
    echo "   • Then run: source ~/.zshrc"
    echo ""
    
    echo -e "${GREEN}4. Ollama (Local - Completely Free)${NC}"
    echo "   • Install: curl -fsSL https://ollama.com/install.sh | sh"
    echo "   • Pull model: ollama pull llama3"
    echo "   • No API key needed!"
    echo ""
    
    echo -e "${GREEN}5. None (No AI)${NC}"
    echo "   • Uses only file extensions and MIME types"
    echo "   • No API key needed"
    echo "   • Fast and reliable for common file types"
}

check_api_key() {
    local provider=$1
    
    case $provider in
        groq)
            if [ -z "$GROQ_API_KEY" ]; then
                echo -e "${YELLOW}⚠️  GROQ_API_KEY not found in environment${NC}"
                return 1
            fi
            ;;
        openai)
            if [ -z "$OPENAI_API_KEY" ]; then
                echo -e "${YELLOW}⚠️  OPENAI_API_KEY not found in environment${NC}"
                return 1
            fi
            ;;
        anthropic)
            if [ -z "$ANTHROPIC_API_KEY" ]; then
                echo -e "${YELLOW}⚠️  ANTHROPIC_API_KEY not found in environment${NC}"
                return 1
            fi
            ;;
    esac
    return 0
}

interactive_mode() {
    show_banner
    python3 "$PYTHON_SCRIPT" --interactive
}

dry_run_mode() {
    local ai_provider=$1
    local directory=${2:-"$HOME"}
    
    show_banner
    echo -e "${YELLOW}🔍 Dry Run Mode - No files will be moved${NC}"
    echo ""
    
    if [ "$ai_provider" != "none" ]; then
        check_api_key "$ai_provider"
        if [ $? -eq 1 ]; then
            echo ""
            echo -e "${YELLOW}Run 'organizer --setup' for setup instructions${NC}"
        fi
    fi
    
    python3 "$PYTHON_SCRIPT" --ai "$ai_provider" --directory "$directory" --dry-run --verbose
}

execute_mode() {
    local ai_provider=$1
    local directory=${2:-"$HOME"}
    
    show_banner
    echo -e "${RED}⚠️  WARNING: This will actually move files!${NC}"
    echo ""
    
    if [ "$ai_provider" != "none" ]; then
        check_api_key "$ai_provider"
        if [ $? -eq 1 ]; then
            echo ""
            echo -e "${YELLOW}Run 'organizer --setup' for setup instructions${NC}"
            echo -e "${YELLOW}Continuing without AI...${NC}"
            ai_provider="none"
        fi
    fi
    
    read -p "Are you sure you want to proceed? (yes/no): " confirm
    if [ "$confirm" != "yes" ]; then
        echo -e "${YELLOW}❌ Cancelled${NC}"
        exit 0
    fi
    
    echo ""
    python3 "$PYTHON_SCRIPT" --ai "$ai_provider" --directory "$directory" --execute --verbose
}

show_help() {
    show_banner
    echo ""
    echo "Usage: organizer [OPTIONS] [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  -i, --interactive     Interactive mode (Recommended - All features!)"
    echo "  --dry-run             Preview organization without moving files"
    echo "  --execute             Actually move files (careful!)"
    echo "  --list-ai             List all available AI providers"
    echo "  --setup               Show AI provider setup instructions"
    echo ""
    echo "Options:"
    echo "  -a, --ai PROVIDER     AI provider: none, groq, openai, anthropic, ollama"
    echo "  -d, --dir DIRECTORY   Directory to organize (default: \$HOME)"
    echo "  -h, --help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  organizer --interactive              # Interactive mode (Best!)"
    echo "  organizer --dry-run --ai groq"
    echo "  organizer --execute --ai openai --dir ~/Downloads"
    echo "  organizer --setup"
    echo ""
    echo "Quick Start:"
    echo "  1. Run: organizer --interactive     # Start interactive mode"
    echo "  2. Choose: Organize or Analyze"
    echo "  3. Follow prompts!"
    echo ""
    echo "Interactive Mode Features:"
    echo "  • 📁 File Organization with preview"
    echo "  • 🔍 File System Analysis with insights"
    echo "  • 🤖 AI-powered recommendations"
    echo "  • 📊 Visual overviews and statistics"
    echo "  • 🧹 Cleanup suggestions"
    echo ""
}

# Main script logic
check_dependencies

case "${1:-}" in
    -i|--interactive)
        interactive_mode
        ;;
    --dry-run)
        dry_run_mode "${2:-none}" "${3:-$HOME}"
        ;;
    --execute)
        execute_mode "${2:-none}" "${3:-$HOME}"
        ;;
    --list-ai)
        show_banner
        list_ai_providers
        ;;
    --setup)
        show_banner
        show_ai_setup
        ;;
    -h|--help|"")
        show_help
        ;;
    *)
        echo -e "${RED}Unknown option: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
