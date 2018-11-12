function listCompanies(inputID, divID){
    var searchbar = document.getElementById(inputID);
    searchbar.addEventListener("keydown", function(){
            document.getElementById(divID).innerHTML = "";
            fetch(`/codedoor/companysearchsuggestion/${searchbar.value}`)
                .then(function(response) {
                    return response.json();
                })
                .then(function(json) {
                    console.log(json);
                    suggestions = makeCompanySuggestions(json, searchbar);
                    document.getElementById(divID).appendChild(suggestions);
                });
    });
};

function makeCompanySuggestions(companies, inputElement){
    var companySuggestions= document.createElement('ul');
    var companyArray= companies["companies"];
    for(var i = 0; i< companyArray.length; i++) {
        var item = document.createElement('li');
        item.appendChild(document.createTextNode(companyArray[i].name));
        item.value= companyArray[i].id;
        item.id= "companyIndex%" + i;
        item.addEventListener("click", (e) => {onListItemClick(e.target, inputElement, companyArray)});
        companySuggestions.appendChild(item);
    }
    return companySuggestions;
};

function onListItemClick(item, inputElement, companyArray){
    var companyIndex= item.id.split("%")[1];
    var company=companyArray[companyIndex];
    pk = company.id;
    console.log(company.name);
    inputElement.value = company.name;


};

listCompanies("companysearch", "suggestions");
listCompanies("companysearch2", "suggestions2");
