/*
 * dropdown.js
 * A utility JS file containing functions for creating a company dropdown.
 */

var LibDropdown = (function () {
    var makeCompanySuggestions = function (companies, inputElement, inputParent, onSelectCompanyPK) {
        var companySuggestions= document.createElement('ul');
        companySuggestions.className = "company-suggestions";
        var companyArray= companies["companies"];
        for(var i = 0; i< companyArray.length; i++) {
            var item = document.createElement('li');
            item.appendChild(document.createTextNode(companyArray[i].name));
            item.value = companyArray[i].id;
            item.id = "companyIndex%" + i;
            item.className = "company-suggestions-li";
            item.addEventListener(
                "click",
                (e) => {
                    onListItemClick(e, inputElement, inputParent, companyArray, onSelectCompanyPK);
                }
            );
            companySuggestions.appendChild(item);
        }
        return companySuggestions;
    };
    var onListItemClick = function (e, inputElement, inputParent, companyArray, onSelectCompanyPK) {
        var item = e.target;
        var companyIndex= item.id.split("%")[1];
        var company=companyArray[companyIndex];
        inputElement.value = company.name;
        inputParent.className = "";

        onSelectCompanyPK(company.id);
    };

    var exports = {
        /* LibDropdown.createCompanyDropdown
         * Creates a company search bar that allows users to search for companies and select from
         * a dropdown menu of suggested companies. The callback argument is the primary key of the selected company.
         *
         * @param {String} inputID - The HTML ID of the search input element.
         * @param {String} divID - The HTML ID of the search suggestions div element.
         * @param {Function: String -> void} onSelectCompanyPK -
            A function taking a string primary key, called when the user selects a company.
         *
         * Example:
         * LibDropdown.createCompanyDropdown("search-box", "dropdown-div", (pk) => console.log(pk));
         */
        createCompanyDropdown: function (inputID, divID, onSelectCompanyPK) {
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
                      suggestions = makeCompanySuggestions(json, searchbar, searchdiv, onSelectCompanyPK);
                      document.getElementById(divID).appendChild(suggestions);
                  });
            });
        },
    };

    return exports;
})();
