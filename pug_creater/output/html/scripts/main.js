const width = screen.width;
const display = localStorage.getItem("dark-mode");
const postDate = document.getElementsByClassName("post-header-time")[0];
const dateString = postDate.innerText;

window.addEventListener("scroll", this.handleScroll);
window.addEventListener("hashchange", this.addPixels);

// Display color
if (display !== null) {
  const htmlTag = document.getElementsByTagName("html")[0];
  const displayButtons = document.getElementsByClassName("display-switch");

  // If last known theme was dark toggle the theme to dark
  if (display === "true" && !htmlTag.classList.contains("dark-mode")) {
    htmlTag.classList.toggle("dark-mode");
    displayButtons[0].innerText = "☀️";
  }
}

// Setup the date format
if (width >= 768) {
  postDate.innerText = dateString;
  if (postDate.classList.contains("small-screen")) {
    postDate.classList.remove("small-screen");
  }
} else {
  const d = new Date(dateString);
  postDate.innerText = d.toLocaleDateString("en-US");
  postDate.classList.add("small-screen");
}

function addPixels(event) {
  //   console.log(window.screen.width);
  window.scrollTo(window.scrollX, window.scrollY - 70);
}

// Scroll event
function handleScroll(event) {
  const navbar = document.getElementById("nav-bar");
  if (window.scrollY > 50) {
    navbar.classList.add("header-content--mini");
    navbar.children[0].classList.add("header-container--mini");
  } else {
    navbar.classList.remove("header-content--mini");
    navbar.children[0].classList.remove("header-container--mini");
  }
}

// This is to toggle menu button on all phone or tablets
function toggleMenu(event) {
  const menu = document.getElementById("menu-button");
  const side_menu = document.getElementById("side-menu");
  //   console.log(event.target)
  if (
    event.target.id === "menu-button" ||
    event.target.className === "menu-line"
  ) {
    menu.classList.toggle("active");
    side_menu.classList.toggle("show");
  }

  const menu_color =
    document.documentElement.style.getPropertyValue("--menu-color");
  const menu_bg_color = document.documentElement.style.getPropertyValue(
    "--menu-background-color"
  );
  //   console.log(menu_color,menu_bg_color);
  if (
    menu.classList.contains("active") &&
    menu_color === "#FFFFFF" &&
    menu_bg_color === "rgba(255, 255, 255, 0)"
  ) {
    document.documentElement.style.setProperty("--menu-color", "#000000");
    document.documentElement.style.setProperty(
      "--menu-background-color",
      "rgba(255, 255, 255, 1)"
    );
  } else if (!menu.classList.contains("active")) {
    document.documentElement.style.setProperty(
      "--menu-color",
      this.state.menu_color
    );
    document.documentElement.style.setProperty(
      "--menu-background-color",
      this.state.menu_bg_color
    );
  }
}
function changeDisplay(event) {
  // Create a media condition that targets viewports prefers dark color scheme
  const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  // Check if the media query is true
  if (mediaQuery.matches) {
    // Then trigger an alert
    return;
  }

  const htmlTag = document.getElementsByTagName("html")[0];
  const displayButtons = document.getElementsByClassName("display-switch");

  htmlTag.classList.toggle("dark-mode");

  // Store state of theme into local storage
  if (htmlTag.classList.contains("dark-mode")) {
    displayButtons[0].innerText = "☀️";
    localStorage.setItem("dark-mode", "true");
  } else {
    displayButtons[0].innerText = "🌙";
    localStorage.setItem("dark-mode", "false");
  }
}

function closeMenu(event) {
  if (event.target.className === "side-link") {
    let menu = document.getElementById("menu-button");
    let side_menu = document.getElementById("side-menu");
    menu.classList.toggle("active");
    side_menu.classList.toggle("show");
  }
}

document
  .getElementsByClassName("display-switch")[0]
  .addEventListener("click", () => {});

document
  .getElementsByClassName("post-header-shareButton")[0]
  .addEventListener("click", () => {
    navigator.clipboard.writeText(document.URL);
    alert("Copied to clipboard ok");
  });
