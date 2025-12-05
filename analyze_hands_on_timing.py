#!/usr/bin/env python3
import os
import re
import glob

def analyze_hands_on_activities(file_path):
    """Analyze hands-on activities in a lab markdown file"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count PromQL code blocks (hands-on queries) - including those in details sections
    promql_blocks = re.findall(r'```promql\n(.*?)\n```', content, re.DOTALL)
    
    # Count exercise sections (usually numbered or bullet points)
    exercise_patterns = [
        r'##\s*Exercise\s*\d+',  # ## Exercise 1
        r'###\s*Exercise\s*\d+', # ### Exercise 1
        r'##\s*\d+\.',           # ## 1.
        r'###\s*\d+\.',          # ### 1.
        r'##\s*Step\s*\d+',      # ## Step 1
        r'###\s*Step\s*\d+',     # ### Step 1
        r'^\d+\.\s+\*\*',        # 1. **something**
    ]
    
    total_exercises = 0
    for pattern in exercise_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE | re.MULTILINE)
        total_exercises += len(matches)
    
    # Count numbered instructions (1. 2. 3. etc.)
    numbered_instructions = len(re.findall(r'^\d+\.\s+\*\*.*?\*\*', content, re.MULTILINE))
    
    # Count challenge sections
    challenge_sections = len(re.findall(r'##\s*Challenge', content, re.IGNORECASE))
    
    # Look for bonus sections to exclude (but we're excluding them anyway)
    bonus_sections = len(re.findall(r'(bonus|optional)', content, re.IGNORECASE))
    
    # Count different types of queries for complexity estimation
    simple_queries = len([q for q in promql_blocks if len(q.strip()) < 100])  # Short queries
    complex_queries = len([q for q in promql_blocks if len(q.strip()) >= 100])  # Longer queries
    
    # Count solution sections (these contain additional queries to practice)
    solution_sections = len(re.findall(r'<summary>.*?Show Solution.*?</summary>', content, re.IGNORECASE))
    
    return {
        'promql_queries': len(promql_blocks),
        'exercises': total_exercises,
        'numbered_instructions': numbered_instructions,
        'challenge_sections': challenge_sections,
        'solution_sections': solution_sections,
        'bonus_sections': bonus_sections,
        'simple_queries': simple_queries,
        'complex_queries': complex_queries,
        'total_activities': numbered_instructions + challenge_sections
    }

def estimate_activity_time(analysis):
    """Estimate time needed for hands-on activities"""
    
    # Time estimates per activity type (in minutes)
    SIMPLE_QUERY_TIME = 1.0      # Copy, paste, run, observe - quick queries
    COMPLEX_QUERY_TIME = 2.5     # Copy, paste, run, understand - longer queries  
    INSTRUCTION_TIME = 2.0       # Read numbered instruction, execute, observe
    CHALLENGE_TIME = 4.0         # Challenge section with multiple queries
    SOLUTION_TIME = 2.0          # Reviewing solution sections
    
    estimated_time = (
        analysis['simple_queries'] * SIMPLE_QUERY_TIME +
        analysis['complex_queries'] * COMPLEX_QUERY_TIME +
        analysis['numbered_instructions'] * INSTRUCTION_TIME +
        analysis['challenge_sections'] * CHALLENGE_TIME +
        analysis['solution_sections'] * SOLUTION_TIME
    )
    
    return estimated_time

def analyze_advanced_labs():
    """Analyze all Advanced labs for hands-on timing"""
    
    labs_path = r"c:\Users\sean\git_repos\promql-labs\Advanced"
    lab_files = [f for f in os.listdir(labs_path) if f.startswith('Lab') and f.endswith('.md')]
    
    print("🔬 ADVANCED LABS HANDS-ON ANALYSIS")
    print("=" * 60)
    print("Assumptions:")
    print("- Users copy/paste and explore briefly")
    print("- Killercoda environment already running")
    print("- No bonus exercises included")
    print("- Quick slide intro per lab")
    print()
    
    total_time = 0
    total_queries = 0
    
    labs_data = []
    
    for lab_file in sorted(lab_files):
        file_path = os.path.join(labs_path, lab_file)
        lab_name = lab_file.replace('.md', '').replace('_', ' ')
        
        analysis = analyze_hands_on_activities(file_path)
        estimated_time = estimate_activity_time(analysis)
        
        # Add time for quick slide intro (2-3 minutes per lab)
        slide_intro_time = 2.5
        total_lab_time = estimated_time + slide_intro_time
        
        labs_data.append({
            'name': lab_name,
            'file': lab_file,
            'analysis': analysis,
            'hands_on_time': estimated_time,
            'slide_intro_time': slide_intro_time,
            'total_time': total_lab_time
        })
        
        total_time += total_lab_time
        total_queries += analysis['promql_queries']
        
        print(f"{lab_name:<35} | {analysis['promql_queries']:>3} queries | {analysis['numbered_instructions']:>2} steps | {analysis['challenge_sections']:>1} challenges | {estimated_time:>5.1f}min hands-on | {total_lab_time:>5.1f}min total")
    
    print("=" * 60)
    print(f"TOTAL ADVANCED LABS TIME: {total_time:.1f} minutes ({total_time/60:.1f} hours)")
    print(f"Total PromQL queries: {total_queries}")
    print()
    
    # Recommendations for 2.5 hour constraint
    available_minutes = 2.5 * 60  # 150 minutes
    
    print("🎯 2.5 HOUR WORKSHOP RECOMMENDATIONS")
    print("=" * 60)
    
    if total_time <= available_minutes:
        print(f"✅ FITS PERFECTLY! You have {available_minutes - total_time:.1f} minutes buffer")
        print("\nRecommended approach:")
        print("- Use all 6 Advanced labs")
        print("- 2.5 min slide intro per lab")
        print("- Focus on copy/paste/explore workflow")
        
    else:
        print(f"⚠️  TIGHT FIT: Need to cut {total_time - available_minutes:.1f} minutes")
        print("\nOptions to fit 2.5 hours:")
        
        # Option 1: Reduce labs
        print("\n1. REDUCE NUMBER OF LABS:")
        cumulative_time = 0
        for i, lab in enumerate(labs_data):
            cumulative_time += lab['total_time']
            if cumulative_time <= available_minutes:
                print(f"   Include: {lab['name']} (running total: {cumulative_time:.1f}min)")
            else:
                print(f"   ❌ Skip: {lab['name']} (would exceed time)")
        
        # Option 2: Reduce slide time
        print(f"\n2. REDUCE SLIDE INTRO TIME:")
        reduced_slide_time = 1.0  # 1 minute instead of 2.5
        total_with_reduced_slides = sum(lab['hands_on_time'] + reduced_slide_time for lab in labs_data)
        print(f"   With 1min slide intros: {total_with_reduced_slides:.1f} minutes")
        
        # Option 3: Select high-impact labs
        print(f"\n3. HIGH-IMPACT LAB SELECTION:")
        # Sort by query density (more learning per minute)
        labs_by_efficiency = sorted(labs_data, key=lambda x: x['analysis']['promql_queries'] / x['total_time'], reverse=True)
        cumulative_time = 0
        selected_labs = []
        for lab in labs_by_efficiency:
            if cumulative_time + lab['total_time'] <= available_minutes:
                cumulative_time += lab['total_time']
                selected_labs.append(lab)
                print(f"   ✅ {lab['name']:<35} | {lab['analysis']['promql_queries']:>3} queries | {lab['total_time']:>5.1f}min")
            else:
                print(f"   ❌ {lab['name']:<35} | {lab['analysis']['promql_queries']:>3} queries | {lab['total_time']:>5.1f}min")
        
        print(f"   Selected labs total: {cumulative_time:.1f} minutes")
    
    print(f"\n💡 BUFFER TIME RECOMMENDATIONS:")
    print(f"- Always reserve 10-15 minutes for Q&A and troubleshooting")
    print(f"- Consider 5-minute bio break after 75 minutes")
    print(f"- Have backup queries ready if moving faster than expected")

if __name__ == "__main__":
    analyze_advanced_labs()
