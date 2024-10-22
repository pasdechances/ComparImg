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
        let row = createRowElement()
        const [group_id, imgs] = duplicates[i];
        
        imgs.forEach(img => {
            const imgBlock = createImageElement(group_id, img.image_id, img.image_path, img.tag);
            imgBlock.addEventListener('click', (e) => handleImageClick(group_id, img.image_id, e.target.tag));
            row.appendChild(imgBlock);
        });

        container.appendChild(row);
        container.appendChild(document.createElement('br'));
    }
}

function createImageElement(group_id, image_id, image_path, tag) {
    const imgElement = document.createElement('img');
    //imgElement.src = path;
    imgElement.id = group_id+'_'+image_id
    imgElement.src = `${API}/img/${group_id}/${image_id}`;
    imgElement.alt = image_path;
    imgElement.tag = tag;
    imgElement.classList.add('img');
    if(tag == "keep")
        imgElement.classList.add('keep');
    else if(tag == "trash")
        imgElement.classList.add('trash');

    return imgElement;
}

function createRowElement() {
    const element = document.createElement('div');
    element.classList.add('row');
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

function handleImageClick(group_id, image_id, currentTag) {
    const newTag = currentTag === 'keep' ? 'trash' : 'keep';
    const endpoint = newTag === 'keep' ? '/api/img/keep' : '/api/img/trow';
    
    fetch(`${API}${endpoint}/${group_id}/${image_id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ group_id, image_id, tag: newTag }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const imgElement = document.getElementById(`${group_id}_${image_id}`);
                imgElement.tag = newTag;
                if(newTag == "keep"){
                    imgElement.classList.remove('trash');
                    imgElement.classList.add('keep');
                }
                else if(newTag == "trash"){
                    imgElement.classList.remove('keep');
                    imgElement.classList.add('trash');
                }
            } else {
                console.error('Error updating tag:', data.message);
            }
        })
        .catch(error => console.error('Erreur lors de la mise à jour du tag:', error));
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



