#!/usr/bin/env python3
import os
import re
from bs4 import BeautifulSoup
import glob

def extract_speaker_notes(html_content):
    """Extract speaker notes from reveal.js HTML (both <aside> and Note: sections)"""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    all_notes = []
    
    # Method 1: Look for <aside class="notes"> elements
    notes_elements = soup.find_all('aside', class_='notes')
    for note in notes_elements:
        text = note.get_text(strip=True)
        if text:
            all_notes.append(text)
    
    # Method 2: Look for "Note:" sections in textarea data-template
    textareas = soup.find_all('textarea', {'data-template': True})
    for textarea in textareas:
        content = textarea.get_text()
        # Split by "Note:" and take everything after it
        if 'Note:' in content:
            note_parts = content.split('Note:')
            for i in range(1, len(note_parts)):  # Skip first part (before first Note:)
                # Get text until next slide or end
                note_text = note_parts[i].strip()
                if note_text:
                    all_notes.append(note_text)
    
    return ' '.join(all_notes)

def count_words(text):
    """Count words in text"""
    # Clean up the text and count words
    words = re.findall(r'\b\w+\b', text.lower())
    return len(words)

def analyze_presentations():
    """Analyze all presentations in the docs folder"""
    docs_path = r"c:\Users\sean\git_repos\promql-labs\docs"
    
    presentations = []
    
    # Find all index.html files in subdirectories
    pattern = os.path.join(docs_path, "*", "index.html")
    html_files = glob.glob(pattern)
    
    for file_path in html_files:
        folder_name = os.path.basename(os.path.dirname(file_path))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            speaker_notes = extract_speaker_notes(content)
            word_count = count_words(speaker_notes)
            
            presentations.append({
                'name': folder_name,
                'path': file_path,
                'word_count': word_count,
                'notes_preview': speaker_notes[:200] + "..." if len(speaker_notes) > 200 else speaker_notes
            })
            
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    
    return presentations

def calculate_timings(presentations, baseline_name="Prometheus_Overview", baseline_minutes=29.5):
    """Calculate speaking rate and estimate timings"""
    
    # Find baseline presentation
    baseline = None
    for p in presentations:
        if p['name'] == baseline_name:
            baseline = p
            break
    
    if not baseline:
        print(f"Baseline presentation '{baseline_name}' not found!")
        return
    
    # Calculate speaking rate (words per minute)
    speaking_rate = baseline['word_count'] / baseline_minutes
    
    print(f"📊 SPEAKING RATE ANALYSIS")
    print(f"=" * 50)
    print(f"Baseline: {baseline_name}")
    print(f"Word count: {baseline['word_count']} words")
    print(f"Actual time: {baseline_minutes} minutes")
    print(f"Speaking rate: {speaking_rate:.1f} words per minute")
    print()
    
    print(f"📋 PRESENTATION TIMING ESTIMATES")
    print(f"=" * 50)
    
    total_time = 0
    beginner_time = 0
    intermediate_time = 0
    advanced_time = 0
    
    for p in sorted(presentations, key=lambda x: x['name']):
        estimated_minutes = p['word_count'] / speaking_rate
        total_time += estimated_minutes
        
        # Categorize by difficulty
        name = p['name']
        if name.startswith('00_') or name.startswith('01_') or name.startswith('02_'):
            beginner_time += estimated_minutes
            level = "BEGINNER"
        elif name.startswith('03_') or name.startswith('04_'):
            intermediate_time += estimated_minutes
            level = "INTERMEDIATE"
        elif name.startswith('05_') or name.startswith('06_') or name.startswith('07_') or name.startswith('08_') or name.startswith('09_') or name.startswith('10_'):
            advanced_time += estimated_minutes
            level = "ADVANCED"
        else:
            level = "OVERVIEW"
        
        print(f"{name:<30} | {p['word_count']:>6} words | {estimated_minutes:>6.1f} min | {level}")
    
    print(f"=" * 50)
    print(f"📈 SUMMARY BY LEVEL")
    print(f"Beginner labs:     {beginner_time:6.1f} minutes")
    print(f"Intermediate labs: {intermediate_time:6.1f} minutes") 
    print(f"Advanced labs:     {advanced_time:6.1f} minutes")
    print(f"Overview:          {baseline_minutes:6.1f} minutes")
    print(f"TOTAL TIME:        {total_time:6.1f} minutes ({total_time/60:.1f} hours)")

if __name__ == "__main__":
    presentations = analyze_presentations()
    
    if presentations:
        print(f"Found {len(presentations)} presentations\n")
        calculate_timings(presentations)
    else:
        print("No presentations found!")
