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
		return this.element.style.display !== 'none';
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

class Validator {
	constructor(formField, validators) {
		this.formField = formField;
		this.value = formField.value.trim();
		this.errorMessage = '';

		//set the second label as the error label
		this.errorLabel = formField.parentNode.getElementsByTagName('label')[1];
		this.validators = validators;
	}

	hasError() {
		return this.errorMessage != '';
	}

	displayError() {
		if (this.hasError()) {
			this.formField.classList.add('has-error');
			if (this.errorLabel) {
				this.errorLabel.innerHTML = this.errorMessage;
				this.focus();
			}
		}
	}

	setErrorMessage(message) {
		this.errorMessage = message;
	}

	resetError() {
		this.setErrorMessage('');
		this.errorLabel.innerHTML = '';
		this.formField.classList.remove('has-error');
	}

	checkNull() {
		return this.value == '';
	}

	focus(formfield) {
		this.formField.focus();
	}

	checkLength(minLength) {
		return this.value.length > minLength;
	}

	fixedLength(length) {
		return this.value.length == length;
	}

	checkRegex(regex) {	
		return regex.test(this.value);
	}

	isInt() {
		return !isNaN(parseInt(this.value));
	}

	validate() {
		//reset error
		this.resetError();
		for (var key in validators) {
			switch (key) {
				case 'isInt':
					if(!this.isInt()) {
						this.setErrorMessage(validators[key]);
					}
					break;
				case 'checkNull':
					if (this.checkNull()) {
						this.setErrorMessage(validators[key]);
					}
					break;
				case 'minLength':
					if (!this.checkLength(parseInt(validators[key]['length'], 10))) {
						this.setErrorMessage(validators[key]['message']);
					}
					break;
				case 'fixedLength':
					if (!this.fixedLength(parseInt(validators[key]['length'], 10))) {
						this.setErrorMessage(validators[key]['message']);
					}
					break;
				case 'checkRegex':
					if (!this.checkRegex(validators[key]['regex'])) {
						this.setErrorMessage(validators[key]['message']);
					}
					break;
				case 'equal':
					if(this.value !== validators[key]['value']) {
							this.setErrorMessage(validators[key]['message']);
					}
					break;
			}
			if (this.hasError()) {
				return false;
			}
		}
		return true;
	}
}

function fieldsValidated(formElements, formFields) {
	let validated = true;
	for (obj in formFields) {
		if (validated) {
			for (formField in formFields[obj]) {
				validators = formFields[obj][formField];
				validator = new Validator(formElements.namedItem(formField), validators);

				if (!validator.validate()) {
					validated = false;
					validator.displayError();
					return false;
				}
			}
		}
	}
	return true;
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

	formElements = document.getElementById('login-form').elements;

	formFieldsToValidate = [
		{
			email: {
				checkNull: 'Please enter your email'
			}
		},
		{
			password: {
				checkNull: 'Please enter your password'
			}
		}
	];

	let validated = fieldsValidated(formElements, formFieldsToValidate);

	if (validated) {
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

	emailContainer = document.getElementById('email-input');
	codeContainer = document.getElementById('code-input');

	emailDis = new ToggleDisplay(emailContainer);
	codeDis = new ToggleDisplay(codeContainer);

	if (emailDis.visible()) {
		let formElements = document.getElementById('send-code').elements;

		let formFieldsToValidate = [
			{ 
				'email': { 
					checkNull: 'Please enter your email',
					checkRegex: {
						regex: /\S+@\S+\.\S+/,
						message: "Please enter a valid email"
					} 
				} 
			}
		];

		let validated = fieldsValidated(formElements, formFieldsToValidate);

		if (validated) {
			//send code to user and toggle display of code entry form
			emailDis.hide();
			codeDis.show();

		}

	} else {

		let formElements = document.getElementById('confirm-code').elements;

		let formFieldsToValidate = [
			{ 
				'code-confirmation': {
					checkNull: 'Please enter the code you\'ve received', 
					isInt: 'Please enter a valid code' 
				} 
			}
		];

		let validated = fieldsValidated(formElements, formFieldsToValidate);

		if (validated) {
			modal = new Modal(document.getElementById('pword-modal'));

			closeOnWindowClick(modal);
			closeOnButtonClick(modal);
			modal.show();
		}
	}
	return false;
}
function submitSignup(e) {
	e.preventDefault();

	formElements = document.getElementById('signup-form').elements;

	formFieldsToValidate = [
		{
			name: {
				checkNull: 'Please enter your name',
				checkRegex:
				{
					regex: /^[a-zA-Z ]+$/,
					message: "Please enter a valid name"
				}
			}
		},
		{ 
			email: { 
				checkNull: 'Please enter your email',
				checkRegex: {
					regex: /\S+@\S+\.\S+/,
					message: "Please enter a valid email"
				} 
			} 
		},
		{
			'id-number': {
				checkNull: 'Please enter your ID Number',
				isInt: "Please enter a valid ID Number",
				fixedLength: {
					length: '8',
					message: 'ID number should be 8 digits'
				}
			}
		},
		{
			password: {
				checkNull: 'Please enter your password',
				minLength: { 
					length: '8', 
					message: 'Short passwords are easy to guess. Try 8 or more characters.'
				}
			}
		},
		{
			'confirm-password': {
				checkNull: 'Please enter your password',
				equal: {
					value: formElements.namedItem('password').value,
					message: "Passwords don't match"
				}
			}
		}
	];

	let validated = fieldsValidated(formElements, formFieldsToValidate);

	if (validated) {
		modal = new Modal(document.getElementById('signin-modal'));

		closeOnWindowClick(modal);
		closeOnButtonClick(modal);
		modal.show();
	}

	return false;
}

function submitAdminUser(e) {
	e.preventDefault();

	let formElements = document.getElementById('add-admin-form').elements;

	let formFieldsToValidate = [
		{
			name: {
				checkNull: 'Please enter the name of the user',
				checkRegex:
				{
					regex: /^[a-zA-Z ]+$/,
					message: "Please enter a valid name"
				}
			}
		},
		{ 
			email: { 
				checkNull: 'Please enter the email of user',
				checkRegex: {
					regex: /\S+@\S+\.\S+/,
					message: "Please enter a valid email"
				} 
			} 
		},
		{
			'phone-number': {
				checkNull: 'Please enter the Phone Number of the user',
				isInt: "Please enter a valid phone number",
				fixedLength: {
					length: '8',
					message: 'Phone number should be 8 digits'
				}
			}
		}
	];

	let validated = fieldsValidated(formElements, formFieldsToValidate);

	if (validated) {

		modal = new Modal(document.getElementById('admin-signup-modal'));

		closeOnWindowClick(modal);
		closeOnButtonClick(modal);
		modal.show();

	}

	return false;
}

function submitAddParty(e) {
	e.preventDefault();

	let modal = new Modal(document.getElementById('add-party-modal'));

	let formElements = document.getElementById('add-party-form').elements;

	let formFieldsToValidate = [
		{
			'political-party': {
				checkNull: "Please specify a name for the political party"
			}
		}
	];

	let validated = fieldsValidated(formElements,formFieldsToValidate);

	if (validated) {
		closeOnButtonClick(modal);
		closeOnWindowClick(modal);
		modal.setMessage("Party added successfully!");
		modal.show();
	}

	return false;
}

function submitAddOffice(e) {
	e.preventDefault();

	let modal = new Modal(document.getElementById('add-office-modal'));

	let formElements = document.getElementById('add-office-form').elements;

	let formFieldsToValidate = [
		{
			'political-office': {
				checkNull: "Please specify a name for the political office"
			}
		}
	];

	let validated = fieldsValidated(formElements,formFieldsToValidate);

	if (validated) {
		closeOnButtonClick(modal);
		closeOnWindowClick(modal);
		modal.show();
	}

	return false;
}