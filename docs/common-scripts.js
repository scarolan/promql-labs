// Load all necessary RevealJS scripts
document.write('<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/dist/reveal.js"></script>');
document.write('<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/plugin/markdown/markdown.js"></script>');
document.write('<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/plugin/highlight/highlight.js"></script>');
document.write('<script src="https://cdn.jsdelivr.net/npm/reveal.js@4.3.1/plugin/notes/notes.js"></script>');

// Initialize RevealJS when the page is loaded
window.addEventListener('DOMContentLoaded', (event) => {
    Reveal.initialize({
        hash: true,
        transition: 'none', // Disable slide animations
        plugins: [RevealMarkdown, RevealHighlight, RevealNotes],
        highlight: {
            highlightOnLoad: true,
            languages: ['promql']
        }
    });
    
    // Add Grafana logo
    const grafanaLogo = document.createElement('img');
    grafanaLogo.src = "../images/grafana_icon.svg";
    grafanaLogo.alt = "Grafana";
    grafanaLogo.className = "grafana-logo";
    document.body.appendChild(grafanaLogo);
    
    // Fix speaker notes formatting
    Reveal.addEventListener('ready', function() {
        document.querySelectorAll('.reveal aside.notes, .notes-preview').forEach(function(noteElem) {
            noteElem.style.fontFamily = 'inherit';
            noteElem.style.whiteSpace = 'normal';
            
            // Also fix all paragraph elements within notes
            noteElem.querySelectorAll('p').forEach(function(p) {
                p.style.fontFamily = 'inherit';
                p.style.whiteSpace = 'normal';
            });
        });
    });
});
