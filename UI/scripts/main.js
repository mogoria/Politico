class ToggleDisplay {
  constructor(element) {
    this.element = element;
  }

  show() {
    this.element.style.display = "block";
  }

  hide() {
    this.element.style.display = "none";
  }

}

class Modal extends ToggleDisplay {
  constructor(modal) {
    super(modal);
    this.message = "Success!";
  }

  setMessage(message) {
    this.message = message;
    this.element.getElementsByClassName('modal-message')[0].innerHTML = this.message;
  }
}

// let interest_modal = document.getElementById('interest-modal');

// let close_interest_modal = document.getElementsByClassName("close")[0];

// close_interest_modal.onclick = function(){closeInterestModal();}

// window.onclick = function(event) {
//     if(event.target==interest_modal){
//         closeInterestModal();
//     }
// }

// function submitInterestForm(e) {
//     e.preventDefault();
//     let formElements = document.getElementById("interest-form").elements;

//     let politicalParty = formElements.namedItem('political-party').value;
//     let politicalOffice = formElements.namedItem("political-office").value;

//     if(!politicalParty) {
//         showInterestModal("Please select a value for political party");

//     } else if(!politicalOffice) {

//         showInterestModal("Please select a value for political office");

//     } else {

//         showInterestModal("Application Successful");

//     }

//     return false;
// }

// function closeInterestModal(){
//     interest_modal.style.display = "none";
// }

// function showInterestModal(message){
//     var modal_message = interest_modal.getElementsByClassName('modal-message')[0];
//     var btn_close = document.getElementById("cls-interest");

//     if(modal_message) {
//         modal_message.innerHTML = message;
//     }

//     interest_modal.style.display = "block";
//     btn_close.onclick = function(){closeInterestModal();}
// }
function closeOnWindowClick(modal){
  window.onclick = function(event) {
      if(event.target==modal.element){
          modal.hide();
      }
  }
}

function closeOnButtonClick(modal){
  var btnClose = document.getElementsByClassName("close-modal")[0];
  if(btnClose) btnClose.onclick = function(){modal.hide();}
}

function submitLogin(e) {
  e.preventDefault();

  selectAccountModal = new Modal(document.getElementById("accounts-modal"));
  
  closeOnWindowClick(selectAccountModal);
  closeOnButtonClick(selectAccountModal);
  selectAccountModal.show();

  return false;
}

function submitInterestForm(e) {
    e.preventDefault();
    formElements = document.getElementById("interest-form").elements;

    politicalParty = formElements.namedItem('political-party').value;
    politicalOffice = formElements.namedItem("political-office").value;

    modal = new Modal(document.getElementById('interest-modal'));
    closeOnWindowClick(modal);
    closeOnButtonClick(modal);

    if(!politicalParty) {

      modal.setMessage("Please select a value for political party");

    } else if(!politicalOffice) {

      modal.setMessage("Please select a value for political office");

    } else {

      modal.setMessage("Application Successful");

    }

    modal.show();
    return false;
}