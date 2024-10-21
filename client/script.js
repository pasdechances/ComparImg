const container = document.getElementById('image-container');
const pageIndice = document.getElementById('page');
const paginationControls = document.getElementById('pagination-controls');
const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');
let duplicates = [];
const itemsPerPage = 10;
let currentPage = 1;
const API = 'http://localhost:5000';

// Charger les données JSON via l'API Flask
fetch(API+'/api/duplicates')
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
            const imgBlock = createImageElement(group_id, img.image_id, img.image_path, img.tag);
            block.appendChild(imgBlock);
        });

        container.appendChild(block);
        container.appendChild(document.createElement('br'));
    }
}

function createImageElement(group_id, image_id, image_path, tag) {
    const imgElement = document.createElement('img');
    //imgElement.src = path;
    imgElement.id = group_id+'_'+image_id
    imgElement.src = `${API}/img/${group_id}/${image_id}`;
    imgElement.alt = image_path;
    imgElement.style.width = '200px';
    imgElement.style.margin = '10px';
    if(tag == "keep")
        imgElement.style.borderStyle = 'solid';
        imgElement.style.borderColor = 'green';
        imgElement.style.borderRadius = '10px';
        imgElement.style.borderWidth = '5px';
    
    if(tag == "trash")
        imgElement.style.opacity = '0.2';
    
    return imgElement;
}

function createContainerElement() {
    const element = document.createElement('div');
    element.style.borderStyle = 'solid';
    element.style.borderColor = 'grey';
    element.style.borderRadius = '10px';
    element.style.borderWidth = '1px';
    element.style.display = 'flex';
    element.style.alignItems = 'center';
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
