// console.log(document.links);
// var active = 0;
// for (var i = 0; i < document.links.length; i++) {
//     console.log("document url: " + document.URL);
//     console.log("link url: " + document.links[i].href);
//     if (document.links[i].href === document.URL) {
//         active = i;
//     }
// }
// document.links[active].className = 'active';

var interest_modal = document.getElementById('interest-modal');

var close_interest_modal = document.getElementsByClassName("close")[0];

close_interest_modal.onclick = function(){closeInterestModal();}

window.onclick = function(event) {
    if(event.target==interest_modal){
        closeInterestModal();
    }
}

function submitInterestForm(e) {
    e.preventDefault();
    var formElements = document.getElementById("interest-form").elements;

    var politicalParty = formElements.namedItem('political-party').value;
    var politicalOffice = formElements.namedItem("political-office").value;

    if(!politicalParty) {
        showInterestModal("Please select a value for political party");

    } else if(!politicalOffice) {

        showInterestModal("Please select a value for political office");

    } else {

        showInterestModal("Application Successful");

    }
    
    return false;
}

function closeInterestModal(){
    interest_modal.style.display = "none";
}

function showInterestModal(message){
    var modal_message = interest_modal.getElementsByClassName('modal-message')[0];
    var btn_close = document.getElementById("cls-interest");

    if(modal_message) {
        modal_message.innerHTML = message;
    }

    interest_modal.style.display = "block";
    btn_close.onclick = function(){closeInterestModal();}
}

