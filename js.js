console.log("JS Connected");
const fileInput = document.getElementById("pdfFile");
const fileName = document.getElementById("fileName");

fileInput.addEventListener("change", () => {

    if(fileInput.files.length > 0){
        fileName.textContent =
        "Selected: " + fileInput.files[0].name;
    }

});