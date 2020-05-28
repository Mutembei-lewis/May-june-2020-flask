// gets the odal element and assigns it to a variable
var modal = document.getElementById('simpleModal');
//get open modal
var modalBtn = document.getElementById('modalBtn');
//get close button
var closeBtn = document.getElementsByClassName('closeBtn')[0];


//function  open modal

function openModal() {
    modal.style.display = 'block';
    }

    //function close modal
function closeModal(){
    modal.style.display ='none'

}


//function to close modal if outside click
function outsideClick(e){
    if(e.target ==modal){
        modal.style.display ='none';
    }
}


//listen for click event
modalBtn.addEventListener('click',openModal);
//listen for close click event
closeBtn.addEventListener('click', closeModal);

//listen for outside click
window.addEventListener('click',outsideClick)






