function listCompanies(inputID, divID){
    var searchbar = document.getElementById(inputID);
    var searchdiv = document.getElementById(divID);
    window.addEventListener("click", function(e) {
      if (e.target != searchbar && e.target.className != "company-suggestions-li") {
        searchdiv.className = "";
      }
    });
    searchbar.parentElement.addEventListener("focusin", function() {
      searchdiv.className = "active";
    });
    searchbar.addEventListener("keydown", function(){
      document.getElementById(divID).innerHTML = "";
      fetch(`/codedoor/companysearchsuggestion/${searchbar.value}`)
          .then(function(response) {
              return response.json();
          })
          .then(function(json) {
              console.log(json);
              suggestions = makeCompanySuggestions(json, searchbar, searchdiv);
              document.getElementById(divID).appendChild(suggestions);
          });
    });
};

function makeCompanySuggestions(companies, inputElement, inputParent){
    var companySuggestions= document.createElement('ul');
    companySuggestions.className = "company-suggestions";
    var companyArray= companies["companies"];
    for(var i = 0; i< companyArray.length; i++) {
        var item = document.createElement('li');
        item.appendChild(document.createTextNode(companyArray[i].name));
        item.value = companyArray[i].id;
        item.id = "companyIndex%" + i;
        item.className = "company-suggestions-li";
        item.addEventListener("click", (e) => {onListItemClick(e, inputElement, inputParent, companyArray)});
        companySuggestions.appendChild(item);
    }
    return companySuggestions;
};

function onListItemClick(e, inputElement, inputParent, companyArray){
    var item = e.target;
    var companyIndex= item.id.split("%")[1];
    var company=companyArray[companyIndex];
    pk = company.id;
    inputElement.value = company.name;
    inputParent.className = "";
};

listCompanies("companysearch", "suggestions");
listCompanies("companysearch2", "suggestions2");
