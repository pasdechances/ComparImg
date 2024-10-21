const container = document.getElementById('image-container');
const pageIndice = document.getElementById('page');
const paginationControls = document.getElementById('pagination-controls');
const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');
let duplicates = [];
const itemsPerPage = 10;
let currentPage = 1;

// Charger les données JSON via l'API Flask
fetch('http://127.0.0.1:5000/api/duplicates')
    .then(response => response.json())
    .then(data => {
        duplicates = Object.entries(data); 
        displayPage(1);
        createPaginationControls();
    })
    .catch(error => console.error('Erreur lors du chargement du fichier JSON:', error));

function displayPage(page) {
    pageIndice.innerHTML = page
    container.innerHTML = '';
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, duplicates.length);

    for (let i = startIndex; i < endIndex; i++) {
        let block = createContainerElement()
        const [group_id, imgs] = duplicates[i];
        
        imgs.forEach(img => {
            const imgBlock = createImageElement(img.image_path);
            block.appendChild(imgBlock);
        });

        container.appendChild(block);
        container.appendChild(document.createElement('br'));
    }
}

function createImageElement(path) {
    const imgElement = document.createElement('img');
    imgElement.src = path;
    imgElement.alt = 'Image en double';
    imgElement.style.width = '200px';
    imgElement.style.margin = '10px';
    return imgElement;
}

function createContainerElement() {
    const element = document.createElement('div');
    element.style.borderStyle = 'solid';
    element.style.borderColor = 'grey';
    element.style.borderRadius = '10px';
    element.style.borderWidth = '1px';
    return element;
}

function createPaginationControls() {
    paginationControls.innerHTML = '';
    const totalPages = Math.ceil(duplicates.length / itemsPerPage);

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.innerText = i;
        button.addEventListener('click', () => {
            currentPage = i;
            displayPage(currentPage);
        });
        paginationControls.appendChild(button);
    }
}

function updatePaginationControls() {
    prevButton.disabled = currentPage === 1;
    nextButton.disabled = currentPage === Math.ceil(duplicates.length / itemsPerPage);
}

prevButton.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        displayPage(currentPage);
        updatePaginationControls();
    }
});

nextButton.addEventListener('click', () => {
    if (currentPage < Math.ceil(duplicates.length / itemsPerPage)) {
        currentPage++;
        displayPage(currentPage);
        updatePaginationControls();
    }
});
