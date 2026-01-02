let analysisResults = null;
let imagePath = null;
let imageUrl = null;

// Load results from localStorage
function loadResults() {
    const resultsData = localStorage.getItem('analysisResults');
    const imagePathData = localStorage.getItem('imagePath');
    
    console.log('Loading results...');
    console.log('Results data:', resultsData);
    console.log('Image path:', imagePathData);
    
    if (resultsData && imagePathData) {
        try {
            analysisResults = JSON.parse(resultsData);
            imagePath = imagePathData;
            console.log('Parsed analysis results:', analysisResults);
            displayResults();
        } catch (error) {
            console.error('Error parsing results:', error);
            alert('Error loading results. Please try again.');
            window.location.href = '/';
        }
    } else {
        console.error('No results found in localStorage');
        alert('No analysis results found. Please upload an image first.');
        window.location.href = '/';
    }
}

function displayResults() {
    console.log('Displaying results...');
    
    try {
        // Display original image
        const originalImage = document.getElementById('originalImage');
        if (originalImage) {
            let filename = imagePath;
            
            if (filename.includes('/')) {
                filename = filename.split('/').pop();
            } else if (filename.includes('\\')) {
                filename = filename.split('\\').pop();
            }
            
            console.log('Setting original image:', filename);
            originalImage.src = `/uploads/${filename}`;
            imageUrl = `${window.location.origin}/uploads/${filename}`;
            
            originalImage.onload = function() {
                console.log('Original image loaded successfully');
            };
            
            originalImage.onerror = function() {
                console.error('Failed to load original image:', `/uploads/${filename}`);
                this.alt = 'Image failed to load';
                this.style.display = 'none';
            };
        }
        
        // Display annotated image if available
        if (analysisResults.annotated_image) {
            console.log('Annotated image path:', analysisResults.annotated_image);
            
            const annotatedImageCard = document.getElementById('annotatedImageCard');
            const annotatedImage = document.getElementById('annotatedImage');
            
            if (annotatedImageCard && annotatedImage) {
                let annotatedFilename = analysisResults.annotated_image;
                
                if (annotatedFilename.includes('/')) {
                    annotatedFilename = annotatedFilename.split('/').pop();
                } else if (annotatedFilename.includes('\\')) {
                    annotatedFilename = annotatedFilename.split('\\').pop();
                }
                
                console.log('Setting annotated image:', annotatedFilename);
                annotatedImage.src = `/uploads/${annotatedFilename}`;
                
                annotatedImage.onload = function() {
                    console.log('Annotated image loaded successfully');
                    annotatedImageCard.style.display = 'block';
                };
                
                annotatedImage.onerror = function() {
                    console.error('Failed to load annotated image:', `/uploads/${annotatedFilename}`);
                    annotatedImageCard.style.display = 'none';
                };
            }
        } else {
            console.log('No annotated image available');
        }
        
        displayObjects();
        displayFaces();
        displayDescription();
        generateShoppingLinks();
        generateLensInsights();
        
        const descriptionElement = document.getElementById('description');
        if (descriptionElement && descriptionElement.textContent.trim()) {
            generateAudio({ en: descriptionElement.textContent.trim() });
        }
        
    } catch (error) {
        console.error('Error displaying results:', error);
        alert('Error displaying results. Please try again.');
    }
}

function generateLensInsights() {
    const container = document.getElementById('lensInsights');
    if (!container) return;
    
    container.innerHTML = '';
    
    const descriptionElement = document.getElementById('description');
    const baseDescription = descriptionElement && descriptionElement.textContent
        ? descriptionElement.textContent.trim()
        : generateDescription();
    
    const objects = analysisResults.objects || [];
    const faces = analysisResults.faces || [];
    
    const objectNames = [];
    const objectCounts = {};
    
    objects.forEach(obj => {
        if (!obj.class) return;
        const name = String(obj.class).toLowerCase();
        if (!objectCounts[name]) {
            objectCounts[name] = 0;
            objectNames.push(name);
        }
        objectCounts[name] += 1;
    });
    
    const queries = [];
    
    faces.forEach(face => {
        if (face.is_celebrity && face.celebrity_name) {
            const name = String(face.celebrity_name).trim();
            if (name && !queries.includes(name)) {
                queries.push(name);
            }
        } else {
            const parts = [];
            if (face.emotion) parts.push(face.emotion);
            if (face.gender) parts.push(face.gender);
            if (face.age) parts.push(`around ${face.age} years old`);
            const phrase = parts.join(' ');
            if (phrase && !queries.includes(phrase)) {
                queries.push(phrase);
            }
        }
    });
    
    objectNames.slice(0, 6).forEach(name => {
        const label = objectCounts[name] > 1 ? `${objectCounts[name]} ${name}s` : name;
        if (!queries.includes(label)) {
            queries.push(label);
        }
    });
    
    if (queries.length === 0 && baseDescription) {
        queries.push(baseDescription);
    }
    
    const summaryCard = document.createElement('div');
    summaryCard.className = 'lens-card';
    summaryCard.innerHTML = `
        <div class="lens-card-title">Scene summary</div>
        <div class="lens-card-body">
            ${baseDescription || 'Image analyzed successfully.'}
        </div>
    `;
    container.appendChild(summaryCard);
    
    if (queries.length > 0) {
        const searchesCard = document.createElement('div');
        searchesCard.className = 'lens-card';
        
        const chips = queries
            .slice(0, 8)
            .map(q => `<span class="lens-chip">${q}</span>`)
            .join('');
        
        const primaryQuery = queries[0];
        const encodedPrimary = encodeURIComponent(primaryQuery);
        const encodedImageUrl = imageUrl ? encodeURIComponent(imageUrl) : null;
        
        searchesCard.innerHTML = `
            <div class="lens-card-title">Smart searches</div>
            <div class="lens-card-body">
                <p>Open quick searches based on what was detected in your image.</p>
                <div class="lens-chip-list">
                    ${chips}
                </div>
                <div class="lens-links">
                    <a class="lens-link" target="_blank" href="https://www.google.com/search?q=${encodedPrimary}">
                        <span>🔍</span><span>Google search</span>
                    </a>
                    <a class="lens-link" target="_blank" href="${encodedImageUrl ? `https://www.google.com/searchbyimage?image_url=${encodedImageUrl}` : `https://www.google.com/search?tbm=isch&q=${encodedPrimary}`}">
                        <span>🖼️</span><span>Similar images (by image)</span>
                    </a>
                    <a class="lens-link" target="_blank" href="https://www.youtube.com/results?search_query=${encodedPrimary}">
                        <span>▶️</span><span>Related videos</span>
                    </a>
                    <a class="lens-link" target="_blank" href="https://www.google.com/search?tbm=shop&q=${encodedPrimary}">
                        <span>🛒</span><span>Shopping results</span>
                    </a>
                </div>
            </div>
        `;
        
        container.appendChild(searchesCard);
    }
    
    const celebrityFaces = faces.filter(
        face => face.is_celebrity && face.celebrity_name && face.celebrity_info && face.celebrity_info.url
    );
    
    if (celebrityFaces.length > 0) {
        const refsCard = document.createElement('div');
        refsCard.className = 'lens-card';
        
        const items = celebrityFaces
            .map(face => {
                const name = face.celebrity_name;
                const url = face.celebrity_info.url;
                const encoded = encodeURIComponent(name);
                return `
                    <div style="margin-bottom: 0.75rem;">
                        <div class="lens-card-title" style="margin-bottom: 0.25rem;">${name}</div>
                        <div class="lens-links">
                            <a class="lens-link" target="_blank" href="${url}">
                                <span>📖</span><span>Wikipedia</span>
                            </a>
                            <a class="lens-link" target="_blank" href="https://www.google.com/search?q=${encoded}">
                                <span>🔍</span><span>Google</span>
                            </a>
                            <a class="lens-link" target="_blank" href="https://www.google.com/search?tbm=isch&q=${encoded}">
                                <span>🖼️</span><span>Images</span>
                            </a>
                        </div>
                    </div>
                `;
            })
            .join('');
        
        refsCard.innerHTML = `
            <div class="lens-card-title">Celebrity references</div>
            <div class="lens-card-body">
                ${items}
            </div>
        `;
        
        container.appendChild(refsCard);
    }
}

function displayObjects() {
    const objectsList = document.getElementById('objectsList');
    if (!objectsList) return;
    
    if (analysisResults.objects && analysisResults.objects.length > 0) {
        console.log('Displaying', analysisResults.objects.length, 'objects');
        objectsList.innerHTML = analysisResults.objects.map(obj => `
            <div class="object-item">
                <span class="object-name">${obj.class}</span>
                <span class="object-confidence">${(obj.confidence * 100).toFixed(1)}%</span>
            </div>
        `).join('');
    } else {
        objectsList.innerHTML = '<p style="color: var(--text-secondary);">No objects detected</p>';
    }
}

function displayFaces() {
    const facesList = document.getElementById('facesList');
    if (!facesList) return;
    
    if (analysisResults.faces && analysisResults.faces.length > 0) {
        console.log('Displaying', analysisResults.faces.length, 'faces');
        facesList.innerHTML = analysisResults.faces.map(face => {
            if (face.is_celebrity && face.celebrity_info) {
                return `
                    <div class="face-item celebrity-face">
                        <h3 style="color: #667eea; margin-bottom: 0.5rem;">
                            ⭐ ${face.celebrity_name}
                        </h3>
                        <p style="color: #10b981; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            ${face.celebrity_category || '⭐ Celebrity'} • ${face.celebrity_confidence}% match
                        </p>
                        <p style="margin: 0.75rem 0; line-height: 1.6;">
                            <strong>Wikipedia:</strong> ${face.celebrity_info.summary}
                        </p>
                        ${face.celebrity_info.url ? `
                            <a href="${face.celebrity_info.url}" target="_blank" 
                               style="color: #667eea; text-decoration: none; display: inline-block; margin-top: 0.5rem;">
                                📖 Read full article on Wikipedia →
                            </a>
                        ` : ''}
                        <hr style="margin: 1rem 0; border: none; border-top: 1px solid rgba(255,255,255,0.1);">
                        <p style="font-size: 0.9rem; color: var(--text-secondary);">
                            <strong>Attributes:</strong> ${face.gender}, ~${face.age} years, ${face.emotion}
                        </p>
                    </div>
                `;
            } else {
                return `
                    <div class="face-item">
                        <p><strong>Gender:</strong> ${face.gender} | <strong>Age:</strong> ~${face.age}</p>
                        <p><strong>Emotion:</strong> ${face.emotion}</p>
                        <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">
                            ℹ️ Not recognized as a celebrity
                        </p>
                    </div>
                `;
            }
        }).join('');
    } else {
        facesList.innerHTML = '<p style="color: var(--text-secondary);">No faces detected</p>';
    }
}

function displayDescription() {
    const descriptionElement = document.getElementById('description');
    if (!descriptionElement) return;
    
    let descriptionText = '';
    
    if (analysisResults.detailed_description) {
        if (typeof analysisResults.detailed_description === 'string') {
            descriptionText = analysisResults.detailed_description;
        } else if (analysisResults.detailed_description.full_description) {
            descriptionText = analysisResults.detailed_description.full_description;
        }
    }
    
    if (!descriptionText && analysisResults.description) {
        descriptionText = analysisResults.description;
    }
    
    if (!descriptionText) {
        descriptionText = generateDescription();
    }
    
    console.log('Description:', descriptionText);
    descriptionElement.textContent = descriptionText;
}

function generateDescription() {
    const objects = analysisResults.objects || [];
    const faces = analysisResults.faces || [];
    
    let desc = '';
    
    if (faces.length > 0) {
        if (faces.length === 1) {
            const face = faces[0];
            if (face.is_celebrity) {
                desc += `There is ${face.celebrity_name} in the image`;
            } else {
                desc += `There is a ${face.emotion} ${face.gender} around ${face.age} years old`;
            }
        } else {
            desc += `There are ${faces.length} persons in the image`;
        }
    }
    
    if (objects.length > 0) {
        const uniqueObjects = {};
        objects.forEach(obj => {
            uniqueObjects[obj.class] = (uniqueObjects[obj.class] || 0) + 1;
        });
        
        const objectDesc = Object.entries(uniqueObjects)
            .slice(0, 5)
            .map(([name, count]) => count > 1 ? `${count} ${name}s` : `a ${name}`)
            .join(', ');
        
        if (desc) {
            desc += ` with ${objectDesc}`;
        } else {
            desc += `I can see ${objectDesc}`;
        }
    }
    
    if (desc === '') {
        desc = 'Image analyzed successfully';
    }
    
    return desc + '.';
}

function generateShoppingLinks() {
    const shoppingLinks = document.getElementById('shoppingLinks');
    if (!shoppingLinks) return;
    
    if (analysisResults.shopping_links && Object.keys(analysisResults.shopping_links).length > 0) {
        console.log('Generating shopping links for', Object.keys(analysisResults.shopping_links).length, 'objects');
        shoppingLinks.innerHTML = '';
        
        for (const [objectName, data] of Object.entries(analysisResults.shopping_links)) {
            const linkSection = document.createElement('div');
            linkSection.className = 'shopping-section-item';
            linkSection.innerHTML = `
                <h3>${objectName} ${data.count > 1 ? `(${data.count})` : ''}</h3>
                <p style="color: var(--text-secondary); margin-bottom: 1rem;">${data.description}</p>
                <div class="shopping-links-grid">
                    ${data.shopping_links.map(link => `
                        <a href="${link.url}" target="_blank" class="shopping-link">
                            <span style="font-size: 1.2rem;">${link.icon}</span>
                            <div>
                                <strong>${link.name}</strong>
                                <p style="font-size: 0.85rem; margin: 0.25rem 0 0 0;">${link.description}</p>
                            </div>
                        </a>
                    `).join('')}
                </div>
            `;
            shoppingLinks.appendChild(linkSection);
        }
    } else {
        shoppingLinks.innerHTML = '<p style="color: var(--text-secondary);">No shopping suggestions available</p>';
    }
}

// Translation functionality
const translateBtn = document.getElementById('translateBtn');
if (translateBtn) {
    translateBtn.addEventListener('click', async () => {
        const selectedLanguages = Array.from(
            document.querySelectorAll('.language-selector input:checked')
        ).map(cb => cb.value);
        
        if (selectedLanguages.length === 0) {
            alert('Please select at least one language');
            return;
        }
        
        const description = document.getElementById('description').textContent;
        
        try {
            const response = await fetch('/api/translate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    text: description,
                    languages: selectedLanguages
                })
            });
            
            const data = await response.json();
            displayTranslations(data.translations);
            generateAudio(data.translations);
        } catch (error) {
            console.error('Translation error:', error);
            alert('Error translating text. Please try again.');
        }
    });
}

function displayTranslations(translations) {
    const container = document.getElementById('translationsContainer');
    container.innerHTML = '';
    
    const languageNames = {
        'te': 'Telugu', 
        'hi': 'Hindi', 
        'en': 'English',
        'es': 'Spanish', 
        'de': 'German', 
        'fr': 'French'
    };
    
    for (const [lang, text] of Object.entries(translations)) {
        const item = document.createElement('div');
        item.className = 'translation-item';
        item.innerHTML = `
            <strong>${languageNames[lang] || lang}</strong>
            <p>${text}</p>
        `;
        container.appendChild(item);
    }
}

async function generateAudio(translations) {
    const audioControls = document.getElementById('audioControls');
    if (!audioControls) {
        console.error('Audio controls element not found');
        return;
    }
    
    audioControls.innerHTML = '<p style="color: var(--text-secondary);">🔄 Generating audio...</p>';
    
    const languageNames = {
        'te': 'Telugu', 
        'hi': 'Hindi', 
        'en': 'English',
        'es': 'Spanish', 
        'de': 'German', 
        'fr': 'French'
    };
    
    // Clear loading message after a short delay
    setTimeout(() => {
        audioControls.innerHTML = '';
    }, 500);
    
    for (const [lang, text] of Object.entries(translations)) {
        try {
            console.log(`[${lang}] Requesting audio generation...`);
            
            const response = await fetch('/api/speak', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text, language: lang})
            });
            
            if (!response.ok) {
                console.error(`[${lang}] HTTP error: ${response.status}`);
                continue;
            }
            
            const data = await response.json();
            console.log(`[${lang}] Response:`, data);
            
            if (data.success && data.audio_file) {
                // Create container
                const audioDiv = document.createElement('div');
                audioDiv.className = 'audio-player';
                audioDiv.style.marginBottom = '1rem';
                
                // Create label
                const label = document.createElement('label');
                label.textContent = languageNames[lang] || lang;
                label.style.display = 'block';
                label.style.marginBottom = '0.5rem';
                label.style.fontWeight = '500';
                label.style.color = 'var(--primary-color)';
                
                // Create audio element
                const audioElement = document.createElement('audio');
                audioElement.controls = true;
                audioElement.preload = 'auto';
                audioElement.style.width = '100%';
                audioElement.style.maxWidth = '500px';
                
                // Add error handling
                audioElement.addEventListener('error', (e) => {
                    console.error(`[${lang}] Audio playback error:`, e);
                    if (!audioElement.dataset.fallbackTried) {
                        audioElement.dataset.fallbackTried = 'true';
                        audioElement.src = `/api/audio/${data.audio_file}`;
                        audioElement.load();
                        return;
                    }
                    const errorMsg = document.createElement('p');
                    errorMsg.style.color = 'red';
                    errorMsg.style.fontSize = '0.9rem';
                    errorMsg.textContent = `Failed to load ${languageNames[lang]} audio`;
                    audioDiv.appendChild(errorMsg);
                });
                
                audioElement.addEventListener('loadeddata', () => {
                    console.log(`[${lang}] Audio loaded successfully`);
                });
                
                // Set source directly from static folder
                audioElement.src = `/static/audio/${data.audio_file}`;
                audioElement.type = 'audio/mpeg';
                
                console.log(`[${lang}] Audio URL: /static/audio/${data.audio_file}`);
                
                // Build the player
                audioDiv.appendChild(label);
                audioDiv.appendChild(audioElement);
                audioControls.appendChild(audioDiv);
                
                // Load the audio
                audioElement.load();
                
                console.log(`[${lang}] ✓ Audio player created`);
                
            } else {
                console.error(`[${lang}] Invalid response:`, data);
            }
            
        } catch (error) {
            console.error(`[${lang}] Exception:`, error);
        }
    }
    
    // Show message if no audio was generated
    if (audioControls.children.length === 0) {
        audioControls.innerHTML = '<p style="color: var(--text-secondary);">❌ Failed to generate audio</p>';
    }
}

// Save button
const saveBtn = document.getElementById('saveBtn');
if (saveBtn) {
    saveBtn.addEventListener('click', async () => {
        try {
            const response = await fetch('/api/save', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(analysisResults)
            });
            
            const data = await response.json();
            
            if (data.success) {
                alert('Results saved successfully!');
            } else {
                alert('Error saving results');
            }
        } catch (error) {
            console.error('Error saving:', error);
            alert('Error saving results');
        }
    });
}

// New analysis button
const newAnalysisBtn = document.getElementById('newAnalysisBtn');
if (newAnalysisBtn) {
    newAnalysisBtn.addEventListener('click', () => {
        localStorage.removeItem('analysisResults');
        localStorage.removeItem('imagePath');
        window.location.href = '/';
    });
}

// Load results when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, loading results...');
    loadResults();
});

// Also load immediately if DOM already loaded
if (document.readyState === 'loading') {
    console.log('Waiting for DOM to load...');
} else {
    console.log('DOM already loaded, loading results immediately...');
    loadResults();
}
