document.getElementById('download-btn').addEventListener('click', function() {
    var node = document.getElementById('job-space');

    domtoimage.toPng(node)
        .then(function (dataUrl) {
            var link = document.createElement('a');
            link.download = 'my-image.png';
            link.href = dataUrl;
            link.click();
        })
        .catch(function (error) {
            console.error('An error occurred while capturing the image: ', error);
        });
});


function myFunction() {
    setTimeout(() => {
    const predictButton = document.getElementById('btn-submit-predict');
    const resetButton = document.getElementById('reset');
    predictButton.style.display = 'none';
    resetButton.style.display = 'block';
    },500)
} ;
document.getElementById('upload-form').addEventListener('change', function (e) {
    e.preventDefault();
    const myform = document.getElementById('upload-form')
    myform.style.display = 'none';
    // Create a FormData object to send the form data
    var formData = new FormData(this);

    // Send a POST request to the server
    fetch(this.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            /*
            console.log(data);
            var photoPreview = document.getElementById('photo-preview');
            var img = document.createElement('img');
            img.src = data.photo_url;
            img.alt = 'Uploaded Photo';
            img.style.width = "450px";
            photoPreview.innerHTML = '';
            photoPreview.appendChild(img);
            */
           console.log("ok@ok")
        } else {
            console.error('Gaza Strong');
        }
    })
    .catch(error => {
        console.error('Gaza Strong failed:', error);
    });
});


$(document).ready(function() {
$("#predict").click(function() {
$.ajax({
    url: '/treat/', // URL de votre vue de traitement Django
    type: 'GET',
    dataType: 'json',
    success: function(data) {
        if (data.success) {
            // Mettre à jour l'image traitée
            var photoPreview = document.getElementById('photo-shaked');
            var outputnames = document.getElementById('names');
            var img = document.createElement('img');
            var player = document.createElement('p');
            var measures = document.createElement('ul');
            const node = document.createTextNode(data.treated_photo_name  +" : " + Number(((1-data.score)*100).toFixed(1))
            + " %" );
            player.appendChild(node);
            img.src = 'data:image/jpeg;base64,' + data.treated_photo_base64; // Utilisez le bon format d'image ici (JPEG, PNG, etc.)
            img.alt = 'Treated Photo';
            img.style.width = "450px";
            photoPreview.innerHTML = '';
            photoPreview.appendChild(img);    
            outputnames.appendChild(player);  
            for (var key in data.dict) {
            if (data.dict.hasOwnProperty(key)) {
                var li = document.createElement("li");
                if (Number(((1-data.dict[key])*100).toFixed(1))>100){
                    li.textContent = key + "  :  " + 100 +" %";
                }
                else if (Number(((1-data.dict[key])*100).toFixed(1))>100<0){
                    li.textContent = key + "  :  " + 0 +" %";
                }
                else{
                    li.textContent = key + "  :  " + Number(((1-data.dict[key])*100).toFixed(1)) +" %";
                }
                
                measures.appendChild(li);
            }
            } 
         
            outputnames.appendChild(measures);
        } else {
            console.error('Gaza Strong');
            // Mettre à jour l'image traitée
            var photoPreview = document.getElementById('photo-shaked');
            var p = document.createElement('p'); // Create a <p> element
            p.textContent = data.message; // Set the text content of the <p> element
                p.style.color = 'red';
            photoPreview.appendChild(p); // Append the <p> element to the 'photo-shaked' element
             
        }
    },
    error: function() {
        console.error('Gaza Strong');
    }
});
});
});



function displaySelectedImage() {
const input = document.getElementById('loaded-image');
const preview = document.getElementById('photo-preview');
const predictButton = document.getElementById('predict');
const image = document.getElementById('selected-image');

if (input.files && input.files[0]) {
    const reader = new FileReader();

    reader.onload = function (e) {
        image.src = e.target.result;
        preview.style.width = "450px";
        preview.style.display = 'block';
        predictButton.style.display = 'block';
    };

    reader.readAsDataURL(input.files[0]);
}
}
//cookies popup
document.addEventListener("DOMContentLoaded", function() {
const popupContainer = document.getElementById("popup-container");
const closeBtn = document.getElementById("close-btn");

// Check if the popup should be shown (using a cookie or local storage)
const popupShown = localStorage.getItem("popupShown");
if (!popupShown) {
//     // Show the popup
  popupContainer.style.display = "flex";

 // Set a flag to indicate that the popup has been shown
  localStorage.setItem("popupShown", "true");
}

// Close the popup when the close button is clicked
closeBtn.addEventListener("click", function() {
popupContainer.style.display = "none";
});
});