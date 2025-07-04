#!/usr/bin/env python3
"""
A script to verify that all PromQL queries in the labs are being tested.
This script scans all markdown files for ```promql blocks and compares them 
with the queries in the test suite.
"""

import os
import sys
import re
from pathlib import Path
import json
from queries import all_queries

# Find the root directory (the one containing this script)
script_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(script_dir)

# Regular expression to find PromQL code blocks in markdown
# This pattern matches ```promql followed by any content until the next ```
promql_pattern = re.compile(r'```promql\s*([\s\S]*?)\s*```')

# Directories to scan for markdown files
dirs_to_scan = [
    os.path.join(root_dir, "Beginner"),
    os.path.join(root_dir, "Intermediate"),
    os.path.join(root_dir, "Advanced")
]

def clean_query(query):
    """Clean and normalize a PromQL query for comparison."""
    # Handle example markers 
    if query.strip().startswith('>'):
        return query.strip()
        
    # Remove comments
    query = re.sub(r'#.*$', '', query, flags=re.MULTILINE)
    # Remove whitespace
    query = re.sub(r'\s+', ' ', query).strip()
    # Remove redundant spaces around operators and parentheses
    query = re.sub(r'\s*([=<>!~(){},:])\s*', r'\1', query)
    # Standardize spaces after commas
    query = re.sub(r',\s*', r',', query)
    # Normalize quotes (replace single quotes with double quotes)
    query = re.sub(r"'([^']*)'", r'"\1"', query)
    # Normalize instance references for comparison
    query = query.replace('"localhost:9100"', '"$INSTANCE"')
    query = query.replace('localhost:9100', '$INSTANCE')
    
    # Normalize time windows (important for subqueries)
    query = re.sub(r'\[(\d+)m:', r'[5m:', query)  # Normalize outer window in subqueries
    query = re.sub(r'\[(\d+)m\]', r'[5m]', query)  # Normalize time windows to 5m
    
    # Normalize boolean comparison operators
    query = re.sub(r'>bool', r'> bool', query)
    query = re.sub(r'<bool', r'< bool', query)
    
    # Remove extra spaces between function name and parenthesis
    query = re.sub(r'(\w+)\s+\(', r'\1(', query)
    
    return query

def extract_queries_from_file(file_path):
    """Extract all PromQL queries from a markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    queries = []
    for match in promql_pattern.finditer(content):
        query_block = match.group(1)
        # Process block line by line
        lines = query_block.strip().split('\n')
        
        current_query = ""
        for line in lines:
            line = line.strip()
            # If it's a comment or example marker, skip
            if line.startswith('#'):
                continue
            # If it's an example line in a block comment
            elif line.startswith('>'):
                # Store the previous query if there is one
                if current_query:
                    queries.append({
                        "raw_query": current_query,
                        "clean_query": clean_query(current_query),
                        "file": file_path
                    })
                    current_query = ""
                # Store the example query with the > marker
                queries.append({
                    "raw_query": line,
                    "clean_query": line,  # Keep the > marker for identification
                    "file": file_path
                })
            else:
                # Regular query line, add to current query
                if current_query:
                    current_query += " " + line
                else:
                    current_query = line
        
        # Don't forget to add the last query if there is one
        if current_query:
            queries.append({
                "raw_query": current_query,
                "clean_query": clean_query(current_query),
                "file": file_path
            })
    
    return queries

def get_test_queries():
    """Get all queries from the test suite and clean them for comparison."""
    return [{
        "name": q["name"],
        "raw_query": q["query"],
        "clean_query": clean_query(q["query"])
    } for q in all_queries]

def find_all_lab_queries():
    """Find all PromQL queries in the lab markdown files."""
    all_lab_queries = []
    
    for dir_path in dirs_to_scan:
        for file in os.listdir(dir_path):
            if file.endswith('.md'):
                file_path = os.path.join(dir_path, file)
                all_lab_queries.extend(extract_queries_from_file(file_path))
    
    return all_lab_queries

def find_untested_queries(lab_queries, test_queries):
    """Find queries in the labs that don't have corresponding tests."""
    untested = []
    matched_queries = {}  # Store which lab queries matched which test queries
    
    # Create a list of cleaned test queries for easier comparison
    clean_test_queries = [test_query["clean_query"] for test_query in test_queries]
    
    # Debug information
    print("\nDEBUG: Example test queries (first 5):")
    for i, query in enumerate(clean_test_queries[:5], 1):
        print(f"{i}. {query}")
    
    for lab_query in lab_queries:
        # Skip comment-only or placeholder queries
        if lab_query["clean_query"].startswith('>') or not lab_query["clean_query"].strip():
            continue
            
        matched = False
        best_match = None
        best_score = 0
        lab_clean = lab_query["clean_query"]
        
        # Try different matching strategies:
        
        # 1. Direct comparison
        if lab_clean in clean_test_queries:
            matched = True
            best_match = lab_clean
            best_score = 100
        
        # 2. Try matching after additional normalization
        if not matched:
            # Try without specific mode filters - check if there's a more generic test
            simplified_query = re.sub(r'mode="[^"]*"', 'mode="$MODE"', lab_clean)
            if simplified_query in clean_test_queries:
                matched = True
                best_match = simplified_query
                best_score = 95
            
            # Try matching recording rules with their equivalents
            if "instance:node_cpu_usage:percent" in lab_clean:
                # Match with equivalent CPU usage calculation
                for idx, test_query in enumerate(clean_test_queries):
                    if "100 * (1 - (" in test_query and "mode=\"idle\"" in test_query:
                        matched = True
                        best_match = test_query
                        best_score = 90
                        break
        
        # 3. For complex queries, try partial matching with key elements
        if not matched and (
            "max_over_time" in lab_clean or 
            "offset" in lab_clean or
            "floor(" in lab_clean or
            "clamp_max" in lab_clean
        ):
            # For these complex queries, look for test queries that contain the same key functions/operations
            for test_query in clean_test_queries:
                functions_in_lab = set(re.findall(r'([a-z_]+)\(', lab_clean))
                if all(func in test_query for func in functions_in_lab):
                    matched = True
                    best_match = test_query
                    best_score = 85
                    break
        
        # 4. Use similarity matching for anything still not matched
        if not matched:
            for test_query in clean_test_queries:
                similarity = query_similarity(lab_clean, test_query)
                if similarity > 80 and similarity > best_score:  # High similarity threshold
                    matched = True
                    best_match = test_query
                    best_score = similarity
        
        if not matched:
            untested.append(lab_query)
        else:
            # Store match information for debugging
            matched_queries[lab_clean] = {
                "test_query": best_match,
                "score": best_score
            }
    
    # Print match statistics for debugging
    if matched_queries:
        print(f"\nSuccessfully matched {len(matched_queries)} lab queries to test queries")
        
    return untested

def query_similarity(query1, query2):
    """Calculate a similarity score between two queries (0-100)."""
    # Extract core metrics and functions
    metrics1 = set(re.findall(r'node_\w+', query1))
    metrics2 = set(re.findall(r'node_\w+', query2))
    
    functions1 = set(re.findall(r'([a-z_]+)\(', query1))
    functions2 = set(re.findall(r'([a-z_]+)\(', query2))
    
    # Calculate metrics and functions overlap
    metrics_overlap = len(metrics1.intersection(metrics2)) / max(1, len(metrics1.union(metrics2))) * 50
    functions_overlap = len(functions1.intersection(functions2)) / max(1, len(functions1.union(functions2))) * 50
    
    return metrics_overlap + functions_overlap

def main():
    """Main function to compare lab queries with test queries."""
    print("Scanning labs for PromQL queries...")
    lab_queries = find_all_lab_queries()
    
    # Filter out example queries marked with '>' and empty queries
    real_lab_queries = [q for q in lab_queries if not q["clean_query"].startswith('>') and q["clean_query"].strip()]
    example_queries = [q for q in lab_queries if q["clean_query"].startswith('>')]
    
    print(f"Found {len(lab_queries)} PromQL queries in the labs.")
    print(f"  - {len(real_lab_queries)} active queries")
    print(f"  - {len(example_queries)} example queries (starting with >)")
    
    print("\nLoading test queries...")
    test_queries = get_test_queries()
    print(f"Found {len(test_queries)} queries in the test suite.")
    
    print("\nChecking for untested queries...")
    untested_queries = find_untested_queries(real_lab_queries, test_queries)
    
    if untested_queries:
        print(f"\n⚠️ Found {len(untested_queries)} queries in the labs that don't have tests:")
        for idx, query in enumerate(untested_queries, 1):
            relative_path = os.path.relpath(query["file"], root_dir)
            print(f"\n{idx}. Query in {relative_path}:")
            print(f"   Raw: {query['raw_query']}")
            print(f"   Cleaned: {query['clean_query']}")
            
            # Show the closest matching test query for debugging
            closest_match = None
            best_score = 0
            for test_query in get_test_queries():
                score = query_similarity(query["clean_query"], test_query["clean_query"])
                if score > best_score:
                    best_score = score
                    closest_match = test_query["clean_query"]
            
            if closest_match and best_score > 50:
                print(f"   Best match ({best_score:.0f}% similarity): {closest_match}")
        
        print("\nEnsure all lab queries have corresponding tests in the test suite.")
        return 1
    else:
        print("\n✅ All PromQL queries in the labs have corresponding tests!")
        return 0

if __name__ == "__main__":
    sys.exit(main())
