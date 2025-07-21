let currentSearch = '';
let currentOffset = 0;
let isLoading = false;
let hasMoreResults = false;

async function searchProgram() {
    const input = document.getElementById('programInput');
    const programName = input.value.trim();
    
    if (!programName) {
        alert('Please enter a program name');
        return;
    }
    
    currentSearch = programName;
    currentOffset = 0;
    hasMoreResults = false;
    
    const existingResults = document.querySelector('.results-container');
    if (existingResults) {
        existingResults.remove();
    }
    
    await performSearch(programName, 0, true);
}

async function loadMoreResults() {
    if (isLoading || !hasMoreResults) return;
    isLoading = true;
    currentOffset += 3;
    await performSearch(currentSearch, currentOffset, false);
    isLoading = false;
}

async function performSearch(programName, offset, isNewSearch) {
    const loading = document.getElementById('loading');
    const btnText = document.getElementById('btnText');
    const searchBtn = document.querySelector('.search-btn');
    
    if (isNewSearch) {
        loading.style.display = 'block';
        btnText.textContent = 'Searching...';
        searchBtn.disabled = true;
    }
    
    try {
        const response = await fetch(`/api/search?program=${encodeURIComponent(programName)}&offset=${offset}&limit=3`);
        const data = await response.json();
        
        if (isNewSearch) {
            loading.style.display = 'none';
            btnText.textContent = 'Search Program';
            searchBtn.disabled = false;
        }
        
        if (response.ok) {
            hasMoreResults = data.has_more;
            displayResults(data, isNewSearch);
        } else {
            showError(data.error);
        }
        
    } catch (error) {
        if (isNewSearch) {
            loading.style.display = 'none';
            btnText.textContent = 'Search Program';
            searchBtn.disabled = false;
        }
        
        showError(`Network error: ${error.message}`);
    }
}

function displayResults(data, isNewSearch) {
    let resultsContainer = document.querySelector('.results-container');
    
    if (isNewSearch || !resultsContainer) {
        resultsContainer = document.createElement('div');
        resultsContainer.className = 'results-container';
        document.querySelector('.container').appendChild(resultsContainer);
    }
    
    if (data.programs.length === 0 && isNewSearch) {
        resultsContainer.innerHTML = '<p class="no-results">No programs found matching your search.</p>';
        return;
    }
    
    const programsHTML = data.programs.map(program => `
        <div class="program-result">
            <h3 class="program-name">${formatProgramName(program.program_name)}</h3>
            
            ${program.section_title ? `<div class="section-title">${program.section_title}</div>` : ''}
            
            ${program.description ? `<p class="program-description">${program.description}</p>` : ''}
            
            <div class="requirements">
                <h4>Requirements:</h4>
                <ul>
                    ${program.requirements && program.requirements.length > 0 
                        ? program.requirements.map(req => `<li>${req}</li>`).join('') 
                        : '<li>No specific requirements listed</li>'}
                </ul>
            </div>
            
            <a href="${program.url}" target="_blank" class="view-full-details">View Full Details</a>
        </div>
    `).join('');
    
    if (isNewSearch) {
        resultsContainer.innerHTML = programsHTML;
    } else {
        const loadingMore = resultsContainer.querySelector('.loading-more');
        if (loadingMore) loadingMore.remove();
        resultsContainer.innerHTML += programsHTML;
    }


    if (!isNewSearch && isLoading) {
        const loadingMoreDiv = document.createElement('div');
        loadingMoreDiv.className = 'loading-more';
        loadingMoreDiv.innerHTML = `<p>Loading more results...</p>`;
        resultsContainer.appendChild(loadingMoreDiv);
    }
    
    if (isNewSearch) {
        const summaryContainer = document.createElement('div');
        summaryContainer.className = 'results-summary';
        summaryContainer.innerHTML = `
            <p>Showing ${Math.min(data.offset + data.limit, data.total)} of ${data.total} results</p>
        `;
        resultsContainer.insertBefore(summaryContainer, resultsContainer.firstChild);
    } else {
        const summary = resultsContainer.querySelector('.results-summary p');
        if (summary) {
            summary.textContent = `Showing ${Math.min(data.offset + data.limit, data.total)} of ${data.total} results`;
        }
    }
}

function showError(message) {
    const existingResults = document.querySelector('.results-container');
    if (existingResults) {
        existingResults.remove();
    }
    
    const errorContainer = document.createElement('div');
    errorContainer.className = 'results-container';
    errorContainer.innerHTML = `<div class="error-message">${message}</div>`;
    
    document.querySelector('.container').appendChild(errorContainer);
}

function formatProgramName(name) {
    return name.replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

document.getElementById('programInput').addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        searchProgram();
    }
});

window.addEventListener('scroll', function() {
    const resultsContainer = document.querySelector('.results-container');
    if (!resultsContainer || !hasMoreResults || isLoading) return;

    const rect = resultsContainer.getBoundingClientRect();
    if (rect.bottom - window.innerHeight < 200) {
        loadMoreResults();
    }
});