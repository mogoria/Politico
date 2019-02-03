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

class Validator{
	constructor(formField, validators) {
		this.formField = formField;
		this.value = formField.value.trim();
		this.errorMessage = "";

		//set the second label as the error label
		this.errorLabel = formField.parentNode.getElementsByTagName("label")[1];
		this.validators = validators;
	}

	hasError(){
		return this.errorMessage!="";
	}

	displayError(){
		if(this.hasError()) {
			this.formField.classList.add("has-error");
			if(this.errorLabel) {
				this.errorLabel.innerHTML = this.errorMessage;
				this.focus();
			}
		}
	}

	setErrorMessage(message) {
		this.errorMessage = message;
	}

	resetError(){
		this.setErrorMessage("");
		this.errorLabel.innerHTML = "";
		this.formField.classList.remove('has-error');
	}

	checkNull(){
		return this.value == "";
	}

	focus(formfield){
		this.formField.focus();
	}

	checkLength(minLength){
		return this.value.length > minLength;
	}

	validate(){
		//reset error
		this.resetError();
		for(var key in validators) {
			switch(key) {
				case "checkNull":
					if(this.checkNull()) {
						this.setErrorMessage(validators[key]);
					}
					break;
				case "minLength":
					if(!this.checkLength(parseInt(validators[key]["length"],10))) {
						this.setErrorMessage(validators[key]["message"])
					}
					break;
			}
			if(this.hasError()) {
				return false;
			} 
		}
		return true
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

	validated = true;
	formElements = document.getElementById('login-form').elements;

	formFieldsToValidate = [
		{"email":{"checkNull":"Email cannot be blank"}},
		{"password":{"checkNull":"Password cannot be blank"}}
	];

	for(obj in formFieldsToValidate) {
		if(validated) {
			for(formField in formFieldsToValidate[obj]){
				validators = formFieldsToValidate[obj][formField];
				validator = new Validator(formElements.namedItem(formField),validators);
	
				if(!validator.validate()) {
					validated = false;
					validator.displayError();
					break;
				}
			}
		}
	}
	
	if(validated) {
		
		selectAccountModal = new Modal(document.getElementById('accounts-modal'));

		closeOnWindowClick(selectAccountModal);
		closeOnButtonClick(selectAccountModal);
		selectAccountModal.show();
	}


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
function submitSignin(e) {
  e.preventDefault();

	modal = new Modal(document.getElementById('signin-modal'));

	closeOnWindowClick(modal);
	closeOnButtonClick(modal);
	modal.show();

	return false;
}

function submitAdminUser(e) {
  e.preventDefault();

  modal = new Modal(document.getElementById('admin-signup-modal'));

	closeOnWindowClick(modal);
	closeOnButtonClick(modal);
	modal.show();

	return false;
}