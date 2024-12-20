const container = document.getElementById('image-container');
const pageIndice = document.getElementById('page');
const paginationControls = document.getElementById('pagination-controls');
const prevButton = document.getElementById('prev-button');
const nextButton = document.getElementById('next-button');
const detectorLaunch = document.getElementById('launch-detector');
const sorterLaunch = document.getElementById('launch-sorter');
const clear = document.getElementById('clear');
let duplicates = [];
const itemsPerPage = 10;
let currentPage = 1;
let statusInterval;
const interval = 1000;
const API = 'http://localhost:5000';

// Charger les données JSON via l'API Flask
function getDuplicates(){
    fetch(API+'/api/duplicates')
    .then(response => response.json())
    .then(data => {
        duplicates = Object.entries(data); 
        displayPage(1);
        createPaginationControls();
    })
    .catch(error => console.error('Error loading JSON file :', error));
}
getDuplicates()

function displayPage(page) {
    pageIndice.innerHTML = page
    container.innerHTML = '';
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = Math.min(startIndex + itemsPerPage, duplicates.length);

    for (let i = startIndex; i < endIndex; i++) {
        let row = createRowElement()
        const [group_id, imgs] = duplicates[i];
        
        imgs.forEach(img => {
            const imgBlock = document.createElement('div');
            imgBlock.classList.add('container');
            const imgElement = createImageElement(group_id, img.image_id, img.image_path, img.tag);
            const infoElement = createInfoElement(img.hamming_distance);
            const binElement = createBinElement(group_id, img.image_id, img.tag);
            imgElement.addEventListener('click', () => keepImageClick(group_id, img.image_id));
            binElement.addEventListener('click', () => trowImageClick(group_id, img.image_id));
            imgBlock.append(imgElement, infoElement, binElement);
            row.appendChild(imgBlock);
        });

        container.appendChild(row);
        container.appendChild(document.createElement('br'));
    }
}

function createImageElement(group_id, image_id, image_path, tag) {
    const el = document.createElement('img');
    //el.src = path;
    el.id = group_id+'_'+image_id
    el.src = `${API}/img/${group_id}/${image_id}`;
    el.alt = image_path;
    el.tag = tag;
    el.classList.add('img');
    if(tag == "keep")
        el.classList.add('keep');
    else if(tag == "trash")
        el.classList.add('trash');

    return el;
}

function createBinElement(group_id, image_id, tag) {
    const el = document.createElement('div');
    el.id = group_id + '_' + image_id + '_bin'
    el.innerText = "X"
    el.classList.add('bin');
    if(tag == "trash")
        el.classList.add('hidden');
    return el;
}

function createInfoElement(info) {
    const el = document.createElement('p');
    if(isNaN(info))
        el.innerText = info
    else
        el.innerText = "Ecart : " + info
    el.classList.add('score');
    return el;
}

function createRowElement() {
    const el = document.createElement('div');
    el.classList.add('row');
    el.classList.add('box');
    return el;
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

function keepImageClick(group_id, image_id) {
    const newTag ='keep'
    const id = `${group_id}_${image_id}`
    const imgElement = document.getElementById(id);
    if(imgElement.tag == newTag) return
    
    fetch(`${API}/api/img/keep/${group_id}/${image_id}`, {
        method: 'PUT'
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const binElement = document.getElementById(`${id}_bin`);
                imgElement.tag = newTag;
                imgElement.classList.remove('trash');
                imgElement.classList.add('keep');
                binElement.classList.remove('hidden')
            } else {
                console.error('Error updating tag:', data.message);
            }
        })
        .catch(error => console.error('Error updating tag:', error));
}

function trowImageClick(group_id, image_id) {
    const newTag ='trash'
    const id = `${group_id}_${image_id}`
    const imgElement = document.getElementById(id);
    if(imgElement.tag == newTag) return
    
    fetch(`${API}/api/img/trow/${group_id}/${image_id}`, {
        method: 'DELETE',
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                const binElement = document.getElementById(`${id}_bin`);
                imgElement.tag = newTag;
                imgElement.classList.remove('keep');
                imgElement.classList.add('trash');
                binElement.classList.add('hidden')
            } else {
                console.error('Error updating tag:', data.message);
            }
        })
        .catch(error => console.error('Error updating tag:', error));
}

function SendDetectionRequest(){
    const form = document.getElementById('form-detection');
    const data = {};
    const imageDir = form.image_dir.value;
    const hsize = form.hsize.value;
    const tolerance = form.tolerance.value;

    if (imageDir) data.image_dir = imageDir;
    if (hsize) data.hsize = parseInt(hsize);
    if (tolerance) data.tolerance = parseInt(tolerance);

    fetch('/api/detection', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === 'success') {
            statusInterval = setInterval(checkDetectorStatus, interval);
            checkDetectorStatus();
        } else {
            console.error('Error starting script:', data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function SendSortRequest(){
    const form = document.getElementById('form-sorter');
    const data = {};
    const trashDir = form.trash_folder.value;

    if (trashDir) data.trash_folder = trashDir;
    fetch('/api/sort', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.status === 'success') {
            statusInterval = setInterval(checkSorterStatus, interval);
            checkSorterStatus();
        } else {
            console.error('Error starting script:', data.message);
        }
    })
    .catch(error => console.error('Error:', error));
}

function checkDetectorStatus() {
    fetch('http://localhost:5000/api/script-status')
        .then(response => response.json())
        .then(data => {
            console.log(`Script status: ${data.status}`);
            if (data.status === 'idle') {
                clearInterval(statusInterval);
                console.log('Script finished');
                getDuplicates()
            }
        })
        .catch(error => console.error('Error checking script status:', error));
}

function checkSorterStatus() {
    fetch('http://localhost:5000/api/script-status')
        .then(response => response.json())
        .then(data => {
            console.log(`Script status: ${data.status}`);
            if (data.status === 'idle') {
                clearInterval(statusInterval);
                console.log('Script finished');
                SendClearRequest()
            }
        })
        .catch(error => console.error('Error checking script status:', error));
}

function SendClearRequest(){
    fetch('http://localhost:5000/api/clear', {
        method: 'DELETE'
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            getDuplicates()
        })
        .catch(error => console.error('Error:', error));
}

sorterLaunch.addEventListener('click', SendSortRequest);
detectorLaunch.addEventListener('click', SendDetectionRequest);

clear.addEventListener('click', SendClearRequest);

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