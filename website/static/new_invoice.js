const saveButton = document.getElementById("save-button");

// Input Fields
const dateField = document.getElementById("date");
const dueDateField = document.getElementById("due_date");
const customerField = document.getElementById("customer");

const subtotal = document.getElementById("subtotal");

// State Variables
let numberItems = 3;

saveButton.addEventListener("click", () => {
	let dataArray = [];

	for (let number = 1; number <= numberItems; number++) {
		let classFields = document.getElementsByClassName(`field_${number}`);
		let dataObject = {};

		for (let i = 0; i < classFields.length; i++) {
			switch (i) {
				case 0:
					dataObject["item"] = classFields[i].value;
				case 1:
					dataObject["quantity"] = classFields[i].value;
				case 2:
					dataObject["unitPrice"] = classFields[i].value;
				case 3:
					dataObject["discount"] = classFields[i].value;
				case 4:
					dataObject["taxRate"] = classFields[i].value;
			}
		}

		if (dataObject["item"]) {
			dataArray.push(dataObject);
		}
	}

	const jsonData = {
		date: dateField.value,
		dueDate: dueDateField.value,
		customerName: customerField.value,
		products: dataArray,
	};

	fetch(window.location.href, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify(jsonData),
	});

	// redirect user to invoices page
	window.location.href = "/invoices";
});

// Auto Change Single Item's Total
for (let classNum = 1; classNum <= numberItems; classNum++) {
	let classFields = document.getElementsByClassName(`field_${classNum}`);
	let itemTotal = document.getElementById(`field_${classNum}_total`);

	let quantityField = classFields[1];
	let unitPriceField = classFields[2];
	let discountField = classFields[3];
	let taxRateField = classFields[4];

	let fieldsArray = [
		quantityField,
		unitPriceField,
		discountField,
		taxRateField,
	];

	fieldsArray.forEach((field) => {
		field.addEventListener("input", () => {
			// change individual totals
			itemTotal.textContent =
				Number(quantityField.value) * Number(unitPriceField.value) -
				Number(discountField.value) +
				Number(taxRateField.value);
		});
	});
}
