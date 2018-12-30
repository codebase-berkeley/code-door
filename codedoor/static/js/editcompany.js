document.addEventListener("DOMContentLoaded", function() {
  var check = {{company.structure}};
  console.log(check);
	for (var i = 0; i < document.getElementsByName("structure").length; i++) {
		if (document.getElementsByName("structure")[i].value == check) {
			document.getElementsByName("structure")[i].setAttribute("checked", "true");
		}
	}
});

