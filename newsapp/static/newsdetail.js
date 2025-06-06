let sharewc = document.querySelector(".share-wa");
let sharefb = document.querySelector(".fb-share-button");

let title = encodeURIComponent("Check Out This Article\n");
let link = encodeURIComponent(window.location.href);
let wfullurl = `https://wa.me/?text=${title}${link}`;

let sharelist = document.querySelector(".share-box");
let s = sharelist.children[1];

// Share button
sharelist.addEventListener("mouseenter", () => {
  s.style.display = "block";
});
sharelist.addEventListener("mouseleave", () => {
  s.style.display = "none";
});
sharewc.setAttribute("href", wfullurl);
sharefb.setAttribute("data-href", link);
let fb = document.querySelector("#fa");

const newHref = `https://www.facebook.com/sharer/sharer.php?u=${link}&src=sdkpreparse`;
fb.setAttribute("href", newHref);

let pagetype = document.querySelector(".details").dataset.page;
const csrftoken = document.querySelector("[name=csrfmiddlewaretoken]").value;
let news_id; // global scope


let userLiked = document.querySelector(".user-liked").dataset.userliked;

let like = document.querySelector(".like-button");
let unlike = document.querySelector(".unset-button");
if (userLiked == "1"){
  like.style.display = "none";

}
if (userLiked == "0"){
  unlike.style.display = "none";
}
// Like No Reloads
function Like() {
  news_id = like.getAttribute("data-news");

  checkEvent(like, "like");
  checkEvent(unlike, "unlike");
}

function checkEvent(button, mode) {
  button.addEventListener("click", () => {
    fetch(`/${pagetype}/like/${news_id}/`, {
      //requests the server

      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ status: mode }), // updated like status pressed like or unlike button
    })
      .then((response) => {
        if (response.status == "403") {
          window.location.href = "/news/login/";
        }

        return response.json();
      })
      .then((data) => {
        if (mode == "like") {
            unlike.style.display = "block";   
            like.style.display = "none";       
        }
        if (mode == "unlike"){
            like.style.display = "block";
            unlike.style.display = "none";       



        }
        document.querySelector(".like-count").textContent = data.likecount + " likes"
      })
      .catch((err) => {
        console.log("error catched", err);
      });
  });
}

// Comments
function setComment() {
  let commentinput = document.querySelector(".commentfield");
  let commentbutton = document.querySelector(".commentsubmit");
  let commentSection = document.querySelector(".comment-list");

  commentbutton.addEventListener("click", () => {
    let comment = commentinput.value;
    fetch(`/${pagetype}/comment/${news_id}/`, {
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ comment: comment }),
    })
      .then((response) => {

        if (response.status == "403") {
          window.location.href = "/news/login/";
        }
        return response.json();
      })

      .then((data) => {
        let date = new Date(data.date);

        let options = {
          month: "long",
          day: "numeric",
          year: "numeric",
          hour: "numeric",
          minute: "2-digit",
          hour12: true
      };
        let formatted = date.toLocaleString("en-US", options);
        formatted = formatted.replace("AM","a.m.").replace("PM","p.m.").replace(" at",",");

        commentPart = document.createElement("div");
        commentPart.classList.add("user-comments")
        commentPart.innerHTML = `<p>At ${formatted}</p>
          <p>${data.author} Said</p>
          <p>${data.commentmessage}</p>
          `;
        commentSection.insertBefore(commentPart,commentSection.firstChild);
      })

      .catch((err) => {
        console.log("error occured",err);
      })
  });
}

Like();
setComment();
