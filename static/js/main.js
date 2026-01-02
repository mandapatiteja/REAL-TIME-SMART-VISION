async function analyzeImage() {
    // ... existing code ...
    
    const response = await fetch('/api/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({filepath: uploadedFilePath})
    });
    
    const results = await response.json();
    
    // *** ADD THIS LINE TO DEBUG ***
    console.log('Analysis results:', results);
    
    // Store results
    localStorage.setItem('analysisResults', JSON.stringify(results));
    localStorage.setItem('imagePath', uploadedFilePath);
    
    // Redirect to results
    window.location.href = '/results';
}
