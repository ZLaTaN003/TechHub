let sharewc = document.querySelector(".share-wa");
let sharefb = document.querySelector(".fb-share-button");

let title = encodeURIComponent("Check Out This Amazing Product\n");
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