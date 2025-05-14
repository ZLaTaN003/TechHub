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
let news_id; // just to make it in global scope

// Like No Reloads
function setLike() {
  let like = document.querySelector(".like-section");
  news_id = like.getAttribute("data-news");

  let likestatus = like.getAttribute("data-liked"); // get the current status
  console.log("trying", likestatus, pagetype);

  like.addEventListener("click", () => {
    likestatus = likestatus == "1" ? "0" : "1";
    fetch(`/${pagetype}/like/${news_id}/`, {
      //requests the server for a likestatus update

      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ status: likestatus }), // updated like status
    })
      .then((response) => {
        if (response.status == "403") {
          window.location.href = "/news/login/";
        }

        return response.json();
      })
      .then((data) => {
        console.log("Updated", data); //response from server
        if (data["liked"]) {
          like.setAttribute("data-liked", "1");
          console.log(like);
        } else {
          like.setAttribute("data-liked", "0");
          console.log(like);
        }
      })
      .catch((err) => {
        console.log("error catched", err);
      });
  });
}

// Comments
function setComment() {
  commentinput = document.querySelector(".commentform");
  commentbutton = document.querySelector(".commentsubmit");

  commentbutton.addEventListener("submit", () => {
    let comment = commentinput.innerText;
    fetch(`/${pagetype}/comment/${news_id}/`, {
      headers: {
        "X-CSRFToken": csrftoken,
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ comment: comment }),
    })
      .then((response) => {
        return response.json();
      })

      .then((data) => {
        console.log("got data", data);
      })

      .catch((err) => {
        console.log("error occured");
      });
  });
}
setLike();
