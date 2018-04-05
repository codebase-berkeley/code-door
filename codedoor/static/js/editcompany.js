// window.onload = checked();
// function checked() {
// 	var check = "{{company.structure}}";
// 	console.log(check);
// 	for (var i = 0; i < document.form.structure.length; i++) {
// 		if (document.form.structure[i] == check) {
// 			document.form.structure[i].setAttribute("checked", "true");
// 		}
// 	}
// }

document.addEventListener("DOMContentLoaded", function() {
  var check = {{company.structure}};
  console.log(check);
	for (var i = 0; i < document.getElementsByName("structure").length; i++) {
		if (document.getElementsByName("structure")[i].value == check) {
			document.getElementsByName("structure")[i].setAttribute("checked", "true");
		}
	}
});

