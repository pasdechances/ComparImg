const modalDetector = document.getElementById("modal-detector");
const btnDetector = document.getElementById("configure-detector");
const spanDetector = document.getElementById("close-detector");
const modalSorter = document.getElementById("modal-sorter");
const btnSorter = document.getElementById("configure-sorter");
const spanSorter = document.getElementById("close-sorter");
const hsize = document.getElementById("hsize")
const tolerance = document.getElementById("tolerance")
const valueHsize = document.getElementById("value-hsize")
const valueTolerance = document.getElementById("value-tolerance")
const btn1 = document.getElementById("btn1")
const btn2 = document.getElementById("btn2")

btnDetector.onclick = function() {
    modalDetector.style.display = "block";
}
spanDetector.onclick = function() {
    modalDetector.style.display = "none";
}
btn1.onclick = function() {
    SendDetectionRequest()
    modalDetector.style.display = "none";
}

btnSorter.onclick = function() {
    modalSorter.style.display = "block";
}
spanSorter.onclick = function() {
    modalSorter.style.display = "none";
}
btn2.onclick = function() {
    SendSortRequest()
    modalSorter.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modalDetector) {
    modalDetector.style.display = "none";
  }
  if (event.target == modalSorter) {
    modalSorter.style.display = "none";
  }
}

hsize.addEventListener("input", (event) => {
    valueHsize.textContent = event.target.value;
});

tolerance.addEventListener("input", (event) => {
    valueTolerance.textContent = event.target.value;
});