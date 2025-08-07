# 🔍 Code Review Assistant

An intelligent Streamlit application that provides instant code reviews focusing on best practices, code style, readability, and common anti-patterns. Get automated feedback on your code to improve quality and maintainability.

## ✨ Features

### 🎯 Comprehensive Code Analysis
- **Style Guidelines**: Line length, formatting, and code conventions
- **Documentation**: Missing docstrings, comments, and code clarity
- **Code Complexity**: Function length, nesting depth, and parameter count
- **Performance**: Inefficient patterns and optimization opportunities
- **Common Pitfalls**: Anti-patterns and known problematic code structures
- **Exception Handling**: Proper error handling best practices
- **Import Organization**: Import style and organization
- **Naming Conventions**: Variable and function naming standards

### 🔧 Multi-Language Support
- **Python**: Full AST-based analysis with Python-specific rules
- **JavaScript, Java, C++**: General code pattern analysis
- **Extensible**: Easy to add support for additional languages

### 📊 Interactive Interface
- **Real-time Analysis**: Instant feedback on code input
- **Severity Filtering**: Filter issues by High, Medium, and Low priority
- **Categorized Results**: Issues grouped by type for easy navigation
- **Actionable Suggestions**: Specific recommendations for each issue
- **Metrics Dashboard**: Quick overview of issue distribution

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the app files**:
   ```bash
   # If you have the full repository
   cd code-review-assistant
   
   # Or create a new directory and copy the files
   mkdir code-review-assistant
   cd code-review-assistant
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser**:
   The app will automatically open at `http://localhost:8501`

### Alternative Installation (using virtual environment)

1. **Create a virtual environment**:
   ```bash
   python -m venv code-review-env
   source code-review-env/bin/activate  # On Windows: code-review-env\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## 📖 Usage Guide

### Basic Usage

1. **Select Language**: Choose your programming language from the sidebar
2. **Paste Code**: Enter your code in the left text area
3. **Review**: Click "🔍 Review Code" to analyze
4. **Filter Results**: Use severity filters to focus on specific issue types
5. **Review Issues**: Examine categorized results with specific suggestions

### Understanding Results

#### Severity Levels
- **🔴 High Priority**: Critical issues that could cause bugs or security problems
- **🟡 Medium Priority**: Important improvements for maintainability and performance
- **🔵 Low Priority**: Style and minor improvements

#### Issue Categories
- **Style**: Code formatting and visual consistency
- **Documentation**: Missing or inadequate documentation
- **Code Complexity**: Overly complex functions or structures
- **Performance**: Potential performance bottlenecks
- **Common Pitfalls**: Known anti-patterns and bad practices
- **Exception Handling**: Improper error handling
- **Import Style**: Import organization and best practices
- **Naming Convention**: Variable and function naming issues

### Example Code Review

**Input Code**:
```python
def calc(a,b,c,d,e,f):
    try:
        result=a+b+c+d+e+f
        return result
    except:
        return None
```

**Issues Found**:
- **High Priority**: Bare except clause catches all exceptions
- **Medium Priority**: Function has too many parameters (6)
- **Low Priority**: Function lacks a docstring
- **Low Priority**: Use snake_case spacing around operators

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit web framework
- **Code Analysis**: Python AST (Abstract Syntax Tree) parsing
- **Pattern Matching**: Regular expressions for general code patterns
- **Data Classes**: Structured issue representation

### Supported Analysis Types

#### Python-Specific Analysis
- AST-based function and class analysis
- Import statement validation
- Python naming convention checks
- Exception handling patterns
- Mutable default argument detection

#### General Code Analysis
- Line length and formatting
- Magic number detection
- Comment quality assessment
- Code complexity metrics

### Customization

The app can be easily extended by modifying the `CodeReviewer` class:

```python
def _check_custom_rule(self, lines: List[str]):
    # Add your custom analysis rules here
    for i, line in enumerate(lines, 1):
        if your_condition:
            self.issues.append(CodeIssue(
                type="Custom Rule",
                line=i,
                message="Your custom message",
                severity="Medium",
                suggestion="Your suggestion"
            ))
```

## 🔧 Configuration

### Environment Variables
No environment variables required for basic functionality.

### Streamlit Configuration
You can customize the app appearance by creating a `.streamlit/config.toml` file:

```toml
[theme]
primaryColor = "#FF4B4B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
port = 8501
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Error**: `ModuleNotFoundError: No module named 'streamlit'`
   - Solution: Install dependencies with `pip install -r requirements.txt`

2. **Port Already in Use**:
   - Solution: Use a different port with `streamlit run app.py --server.port 8502`

3. **Code Analysis Fails**:
   - Check if the code has syntax errors
   - Ensure the selected language matches your code

### Performance Tips
- For large code files, consider breaking them into smaller functions
- The app works best with code snippets under 1000 lines
- Complex AST analysis may take longer for very large files

## 🤝 Contributing

This app is part of the "Apps by Agents" repository. Contributions should follow the AI-agent contribution model:

1. AI agents create improvements autonomously
2. Follow the existing code structure and patterns
3. Add comprehensive tests for new features
4. Update documentation for any changes

## 📄 License

This application is part of the Apps by Agents project and follows the same licensing terms.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Verify your Python and Streamlit installation
3. Ensure all dependencies are correctly installed
4. Check the Streamlit logs for detailed error messages

## 🚀 Future Enhancements

Potential improvements for future versions:
- Support for more programming languages
- Integration with version control systems
- Custom rule configuration files
- Code diff analysis
- Export reports to PDF/HTML
- Integration with popular IDEs
- Team collaboration features

---

**Created by**: AI Agent (Claude)  
**Framework**: Streamlit  
**Language**: Python 3.8+  
**Last Updated**: August 2025