import streamlit as st
import re
import ast
import keyword
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass

@dataclass
class CodeIssue:
    type: str
    line: int
    message: str
    severity: str
    suggestion: str = ""

class CodeReviewer:
    def __init__(self):
        self.issues = []
        
    def analyze_code(self, code: str, language: str = "python") -> List[CodeIssue]:
        self.issues = []
        
        if language.lower() == "python":
            self._analyze_python_code(code)
        else:
            self._analyze_general_code(code)
            
        return self.issues
    
    def _analyze_python_code(self, code: str):
        lines = code.split('\n')
        
        try:
            tree = ast.parse(code)
            self._check_python_ast(tree, lines)
        except SyntaxError as e:
            self.issues.append(CodeIssue(
                type="Syntax Error",
                line=e.lineno if e.lineno else 1,
                message=f"Syntax error: {e.msg}",
                severity="High",
                suggestion="Fix the syntax error to proceed with analysis"
            ))
            return
        
        self._check_line_length(lines)
        self._check_naming_conventions(lines)
        self._check_imports(lines)
        self._check_comments_and_docstrings(lines)
        self._check_complexity(lines)
        self._check_common_antipatterns(lines)
    
    def _analyze_general_code(self, code: str):
        lines = code.split('\n')
        self._check_line_length(lines)
        self._check_general_patterns(lines)
    
    def _check_python_ast(self, tree: ast.AST, lines: List[str]):
        class FunctionAnalyzer(ast.NodeVisitor):
            def __init__(self, reviewer):
                self.reviewer = reviewer
                
            def visit_FunctionDef(self, node):
                if len(node.args.args) > 5:
                    self.reviewer.issues.append(CodeIssue(
                        type="Code Complexity",
                        line=node.lineno,
                        message=f"Function '{node.name}' has too many parameters ({len(node.args.args)})",
                        severity="Medium",
                        suggestion="Consider using a configuration object or breaking down the function"
                    ))
                
                if not ast.get_docstring(node):
                    self.reviewer.issues.append(CodeIssue(
                        type="Documentation",
                        line=node.lineno,
                        message=f"Function '{node.name}' lacks a docstring",
                        severity="Low",
                        suggestion="Add a docstring explaining the function's purpose, parameters, and return value"
                    ))
                
                body_length = len([n for n in ast.walk(node) if isinstance(n, ast.stmt)])
                if body_length > 20:
                    self.reviewer.issues.append(CodeIssue(
                        type="Code Complexity",
                        line=node.lineno,
                        message=f"Function '{node.name}' is too long ({body_length} statements)",
                        severity="Medium",
                        suggestion="Break this function into smaller, more focused functions"
                    ))
                
                self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                if not ast.get_docstring(node):
                    self.reviewer.issues.append(CodeIssue(
                        type="Documentation",
                        line=node.lineno,
                        message=f"Class '{node.name}' lacks a docstring",
                        severity="Low",
                        suggestion="Add a docstring explaining the class purpose and usage"
                    ))
                
                self.generic_visit(node)
        
        analyzer = FunctionAnalyzer(self)
        analyzer.visit(tree)
    
    def _check_line_length(self, lines: List[str]):
        max_length = 88  # PEP 8 recommends 79, but 88 is more practical
        for i, line in enumerate(lines, 1):
            if len(line) > max_length:
                self.issues.append(CodeIssue(
                    type="Style",
                    line=i,
                    message=f"Line too long ({len(line)} characters)",
                    severity="Low",
                    suggestion=f"Keep lines under {max_length} characters for better readability"
                ))
    
    def _check_naming_conventions(self, lines: List[str]):
        for i, line in enumerate(lines, 1):
            line = line.strip()
            
            # Check for camelCase variables (should be snake_case in Python)
            if re.search(r'\b[a-z]+[A-Z][a-zA-Z]*\s*=', line):
                self.issues.append(CodeIssue(
                    type="Naming Convention",
                    line=i,
                    message="Use snake_case for variable names, not camelCase",
                    severity="Low",
                    suggestion="Convert camelCase variables to snake_case (e.g., myVar -> my_var)"
                ))
            
            # Check for single letter variables (except common ones like i, j, x, y)
            single_char_pattern = r'\b[a-df-hk-wz]\s*='
            if re.search(single_char_pattern, line) and not re.search(r'for\s+[a-z]\s+in', line):
                self.issues.append(CodeIssue(
                    type="Naming Convention",
                    line=i,
                    message="Avoid single-letter variable names",
                    severity="Low",
                    suggestion="Use descriptive variable names that explain the data they hold"
                ))
    
    def _check_imports(self, lines: List[str]):
        import_lines = []
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith('import ') or stripped.startswith('from '):
                import_lines.append((i, stripped))
        
        # Check if imports are at the top
        first_non_comment_line = None
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('"""') and not stripped.startswith("'''"):
                first_non_comment_line = i
                break
        
        if import_lines:
            first_import_line = min(import_lines, key=lambda x: x[0])[0]
            if first_non_comment_line and first_import_line != first_non_comment_line:
                self.issues.append(CodeIssue(
                    type="Import Style",
                    line=first_import_line,
                    message="Imports should be at the top of the file",
                    severity="Low",
                    suggestion="Move all imports to the beginning of the file, after module docstring"
                ))
        
        # Check for wildcard imports
        for line_num, line in import_lines:
            if 'import *' in line:
                self.issues.append(CodeIssue(
                    type="Import Style",
                    line=line_num,
                    message="Avoid wildcard imports (import *)",
                    severity="Medium",
                    suggestion="Import specific functions/classes or use 'import module' syntax"
                ))
    
    def _check_comments_and_docstrings(self, lines: List[str]):
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for TODO comments without clear action
            if 'TODO' in line.upper() and not re.search(r'TODO:?\s*\w+', line, re.IGNORECASE):
                self.issues.append(CodeIssue(
                    type="Code Maintenance",
                    line=i,
                    message="TODO comment should include specific action or assignee",
                    severity="Low",
                    suggestion="Make TODO comments actionable: 'TODO: [description] - [assignee]'"
                ))
    
    def _check_complexity(self, lines: List[str]):
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for deeply nested code
            indent_level = len(line) - len(line.lstrip())
            if indent_level > 16:  # More than 4 levels of indentation
                self.issues.append(CodeIssue(
                    type="Code Complexity",
                    line=i,
                    message="Code is deeply nested (consider refactoring)",
                    severity="Medium",
                    suggestion="Extract nested logic into separate functions or use early returns"
                ))
    
    def _check_common_antipatterns(self, lines: List[str]):
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for bare except clauses
            if re.match(r'^\s*except\s*:\s*$', line):
                self.issues.append(CodeIssue(
                    type="Exception Handling",
                    line=i,
                    message="Bare except clause catches all exceptions",
                    severity="High",
                    suggestion="Catch specific exception types: 'except SpecificException:'"
                ))
            
            # Check for mutable default arguments
            if re.search(r'def\s+\w+\([^)]*=\s*(\[\]|\{\})', line):
                self.issues.append(CodeIssue(
                    type="Common Pitfall",
                    line=i,
                    message="Mutable default argument detected",
                    severity="High",
                    suggestion="Use None as default and create the mutable object inside the function"
                ))
            
            # Check for string concatenation in loops
            if '+=' in line and any(loop_keyword in lines[max(0, i-5):i] for loop_keyword in ['for ', 'while ']):
                if any('str' in prev_line or '"' in prev_line or "'" in prev_line for prev_line in lines[max(0, i-3):i]):
                    self.issues.append(CodeIssue(
                        type="Performance",
                        line=i,
                        message="String concatenation in loop can be inefficient",
                        severity="Medium",
                        suggestion="Consider using join() or f-strings for better performance"
                    ))
    
    def _check_general_patterns(self, lines: List[str]):
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for hardcoded values
            if re.search(r'\b\d{3,}\b', stripped) and not re.search(r'#.*\d{3,}', stripped):
                self.issues.append(CodeIssue(
                    type="Code Quality",
                    line=i,
                    message="Consider extracting magic numbers into named constants",
                    severity="Low",
                    suggestion="Replace magic numbers with descriptive constants"
                ))
            
            # Check for very long lines in any language
            if len(line) > 120:
                self.issues.append(CodeIssue(
                    type="Readability",
                    line=i,
                    message=f"Line is very long ({len(line)} characters)",
                    severity="Low",
                    suggestion="Break long lines for better readability"
                ))


def main():
    st.set_page_config(
        page_title="Code Review Assistant",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 Code Review Assistant")
    st.markdown("Get instant feedback on your code for best practices, style, and common anti-patterns.")
    
    # Sidebar for settings
    with st.sidebar:
        st.header("⚙️ Settings")
        language = st.selectbox(
            "Select Language",
            options=["Python", "JavaScript", "Java", "C++", "Other"],
            index=0
        )
        
        severity_filter = st.multiselect(
            "Filter by Severity",
            options=["High", "Medium", "Low"],
            default=["High", "Medium", "Low"]
        )
        
        st.markdown("---")
        st.markdown("### 📋 Review Categories")
        st.markdown("""
        - **Style**: Code formatting and conventions
        - **Documentation**: Missing docstrings/comments  
        - **Code Complexity**: Functions too long/complex
        - **Performance**: Potential performance issues
        - **Common Pitfalls**: Known anti-patterns
        - **Exception Handling**: Error handling best practices
        - **Import Style**: Import organization
        - **Naming Convention**: Variable/function naming
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Code Input")
        code_input = st.text_area(
            "Paste your code here:",
            height=400,
            placeholder="# Paste your code here for review\n\ndef example_function():\n    pass"
        )
        
        if st.button("🔍 Review Code", type="primary"):
            if code_input.strip():
                with st.spinner("Analyzing code..."):
                    reviewer = CodeReviewer()
                    issues = reviewer.analyze_code(code_input, language.lower())
                    
                    # Filter issues by severity
                    filtered_issues = [issue for issue in issues if issue.severity in severity_filter]
                    
                    # Store results in session state
                    st.session_state.issues = filtered_issues
                    st.session_state.total_issues = len(issues)
                    st.success(f"Analysis complete! Found {len(filtered_issues)} issues.")
            else:
                st.error("Please enter some code to review.")
    
    with col2:
        st.subheader("📊 Review Results")
        
        if hasattr(st.session_state, 'issues'):
            issues = st.session_state.issues
            total_issues = st.session_state.total_issues
            
            if issues:
                # Summary metrics
                col_metrics = st.columns(3)
                with col_metrics[0]:
                    high_count = len([i for i in issues if i.severity == "High"])
                    st.metric("🚨 High Priority", high_count)
                
                with col_metrics[1]:
                    medium_count = len([i for i in issues if i.severity == "Medium"])
                    st.metric("⚠️ Medium Priority", medium_count)
                
                with col_metrics[2]:
                    low_count = len([i for i in issues if i.severity == "Low"])
                    st.metric("💡 Low Priority", low_count)
                
                st.markdown("---")
                
                # Group issues by type
                issues_by_type = {}
                for issue in issues:
                    if issue.type not in issues_by_type:
                        issues_by_type[issue.type] = []
                    issues_by_type[issue.type].append(issue)
                
                # Display issues
                for issue_type, type_issues in issues_by_type.items():
                    with st.expander(f"📂 {issue_type} ({len(type_issues)} issues)", expanded=True):
                        for issue in sorted(type_issues, key=lambda x: x.line):
                            severity_color = {
                                "High": "🔴",
                                "Medium": "🟡", 
                                "Low": "🔵"
                            }[issue.severity]
                            
                            st.markdown(f"""
                            **Line {issue.line}** {severity_color} {issue.severity}
                            
                            **Issue:** {issue.message}
                            
                            **Suggestion:** {issue.suggestion}
                            """)
                            st.divider()
                
            else:
                st.success("🎉 No issues found! Your code looks great!")
                
        else:
            st.info("👆 Enter code in the left panel and click 'Review Code' to see results here.")
    
    # Footer with tips
    st.markdown("---")
    st.markdown("### 💡 Code Review Tips")
    
    tips_col1, tips_col2, tips_col3 = st.columns(3)
    
    with tips_col1:
        st.markdown("""
        **🎨 Style Guidelines**
        - Keep lines under 88 characters
        - Use consistent naming conventions
        - Add proper spacing and indentation
        """)
    
    with tips_col2:
        st.markdown("""
        **📚 Documentation**
        - Write clear docstrings
        - Add comments for complex logic
        - Use meaningful variable names
        """)
    
    with tips_col3:
        st.markdown("""
        **🏗️ Code Structure**
        - Keep functions small and focused
        - Avoid deep nesting
        - Handle exceptions properly
        """)

if __name__ == "__main__":
    main()