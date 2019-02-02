class ToggleDisplay {
	constructor(element) {
		this.element = element;
	}

	show() {
		this.element.style.display = 'block';
	}

	hide() {
		this.element.style.display = 'none';
  }
  
  visible() {
    return this.element.style.display !== "none";
  }
}

class Modal extends ToggleDisplay {
	constructor(modal) {
		super(modal);
		this.message = 'Success!';
	}

	setMessage(message) {
		this.message = message;
		this.element.getElementsByClassName('modal-message')[0].innerHTML = this.message;
	}
}

function closeOnWindowClick(modal) {
	window.onclick = function(event) {
		if (event.target == modal.element) {
			modal.hide();
		}
	};
}

function closeOnButtonClick(modal) {
	var btnClose = document.getElementsByClassName('close-modal')[0];
	if (btnClose)
		btnClose.onclick = function() {
			modal.hide();
		};
}

function submitLogin(e) {
	e.preventDefault();

	selectAccountModal = new Modal(document.getElementById('accounts-modal'));

	closeOnWindowClick(selectAccountModal);
	closeOnButtonClick(selectAccountModal);
	selectAccountModal.show();

	return false;
}

function submitInterestForm(e) {
	e.preventDefault();
	formElements = document.getElementById('interest-form').elements;

	politicalParty = formElements.namedItem('political-party').value;
	politicalOffice = formElements.namedItem('political-office').value;

	modal = new Modal(document.getElementById('interest-modal'));
	closeOnWindowClick(modal);
	closeOnButtonClick(modal);

	if (!politicalParty) {
		modal.setMessage('Please select a value for political party');
	} else if (!politicalOffice) {
		modal.setMessage('Please select a value for political office');
	} else {
		modal.setMessage('Application Successful');
	}

	modal.show();
	return false;
}

function submitEmail(e) {
  e.preventDefault();
  
  emailContainer = document.getElementById("email-input");
  codeContainer = document.getElementById("code-input");

  emailDis = new ToggleDisplay(emailContainer);
  codeDis = new ToggleDisplay(codeContainer);

  if(emailDis.visible()) {
    emailDis.hide()
    codeDis.show()
  } else {
    modal = new Modal(document.getElementById('pword-modal'));

    closeOnWindowClick(modal);
    closeOnButtonClick(modal);
    modal.show();
  } 
  return false;
}
