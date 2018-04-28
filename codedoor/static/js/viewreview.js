

function getCookie(name) {
  var regexp = new RegExp("(?:^" + name + "|;\s*"+ name + ")=(.*?)(?:;|$)", "g");
  var result = regexp.exec(document.cookie);
  return (result === null) ? null : result[1];
}



document.getElementById("addcomment").addEventListener("click", function(){

document.getElementById("blackout").style.display = "block";
console.log("debugged");
});


console.log("Do somethings");
    document.getElementById("cancel").addEventListener("click", function() {

document.getElementById("blackout").style.display = "none";

});
    document.getElementById("submit").addEventListener("click", function() {
        console.log("In the addEventListener");


        var title = document.getElementById("addtitle").value;
        var content = document.getElementById("addbody").value;

        var commentData = new FormData();
        commentData.append("title", title);
        commentData.append("content", content);
        var review = document.getElementById("reviewpk").value;
        commentData.append("review", review )
        var headers = new Headers();

        var csrftoken = getCookie("csrftoken")
        headers.append('X-CSRFToken', csrftoken);

        fetch("/codedoor/addrc/", {
            method: "POST",
            body: commentData,
            headers: headers,
            credentials: "include"
        }).then(function(response) {
            return response.json();
        }).then(function(json) {
            if (json.success) {
                document.getElementById("comment").innerHTML =


                "<div id=\"comment\"><div id=\"profile-img\" style=\"background-image: url(" +json.profile_url+ ");\">"
                  +"</div><p id='commenter'>"+json.name+"</p>"
                  +"<p class='commentcontents'>"+json.content+"</p><br></div>"
                   + document.getElementById("comment").innerHTML;
            }
        })

      document.getElementById("blackout").style.display = "none";
    }



  );