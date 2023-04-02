const width = screen.width;
const display = localStorage.getItem('dark-mode');
const postDate = document.getElementsByClassName('post-header-time')[0];
const timeText = document.getElementById('post-read-time');
const dateString = postDate.innerText;

window.addEventListener('scroll', this.handleScroll);
window.addEventListener("hashchange", this.addPixels);

// Display color
if (display !== null)
{
   const htmlTag = document.getElementsByTagName('html')[0];
   const displayButtons = document.getElementsByClassName('display-switch');

   // If last known theme was dark toggle the theme to dark
   if ( display === 'true' && !htmlTag.classList.contains('dark-mode') )
   {
      htmlTag.classList.toggle('dark-mode');
      displayButtons[0].innerText = '☀️'; 
   }
}

// Setup the date format
if (width >= 768)
{
   postDate.innerText = dateString;
   if (postDate.classList.contains('small-screen'))
   {
      postDate.classList.remove('small-screen');
   }
}
else
{
   const d = new Date(dateString);
   postDate.innerText = d.toLocaleDateString('en-US');
   postDate.classList.add('small-screen');
}

function addPixels(event) {
//   console.log(window.screen.width);
   window.scrollTo(window.scrollX, window.scrollY - 70);
}

// Scroll event
function handleScroll(event){
   const navbar = document.getElementById('nav-bar');
   if (window.scrollY > 50) 
   {
      navbar.classList.add('header-content--mini');
      navbar.children[0].classList.add('header-container--mini');
   } else 
   {
      navbar.classList.remove('header-content--mini');
      navbar.children[0].classList.remove('header-container--mini');
   }
}

// This is to toggle menu button on all phone or tablets
function toggleMenu(event) {
const menu = document.getElementById('menu-button');
const side_menu = document.getElementById('side-menu'); 
//   console.log(event.target) 
   if(event.target.id === 'menu-button' 
      || event.target.className === 'menu-line') {
   menu.classList.toggle('active');
   side_menu.classList.toggle('show');
   }

   const menu_color = document.documentElement.style.getPropertyValue('--menu-color');
   const menu_bg_color = document.documentElement.style.getPropertyValue('--menu-background-color');
//   console.log(menu_color,menu_bg_color);
   if(menu.classList.contains('active') && (menu_color === '#FFFFFF' && menu_bg_color === 'rgba(255, 255, 255, 0)')) {
      document.documentElement.style.setProperty('--menu-color', '#000000');
      document.documentElement.style.setProperty('--menu-background-color', 'rgba(255, 255, 255, 1)');
   } else if (!menu.classList.contains('active')) {
      document.documentElement.style.setProperty('--menu-color', this.state.menu_color);
      document.documentElement.style.setProperty('--menu-background-color', this.state.menu_bg_color);
   }
}
function changeDisplay(event) { 

   // Create a media condition that targets viewports prefers dark color scheme
   const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
   // Check if the media query is true
   if (mediaQuery.matches) {
      // Then trigger an alert
      return;
   }

   const htmlTag = document.getElementsByTagName('html')[0];
   const displayButtons = document.getElementsByClassName('display-switch');

   htmlTag.classList.toggle('dark-mode');
   
   // Store state of theme into local storage
   if ( htmlTag.classList.contains('dark-mode') )
   {
      displayButtons[0].innerText = '☀️';
      localStorage.setItem('dark-mode', "true");
   }
   else
   {
      displayButtons[0].innerText = '🌙';  
      localStorage.setItem('dark-mode', "false"); 
   }
}

function closeMenu(event) {
   if(event.target.className === 'side-link') {
      let menu = document.getElementById('menu-button');
      let side_menu = document.getElementById('side-menu'); 
      menu.classList.toggle('active');
      side_menu.classList.toggle('show');
   }
}



document.getElementsByClassName("display-switch")[0].addEventListener("click", () => {

})

document.getElementsByClassName("post-header-shareButton")[0].addEventListener("click",() => {
   navigator.clipboard.writeText(document.URL);
   alert("Copied to clipboard ok");
});

// READ TIME
function getReadTime() {
   let textContent;
   let wordsPerMinute = 250;
   let timeToRead;

   textContent = document.querySelector('body').innerText;
   let wordCount = textContent.split(' ').length;

   // Find all code blocks and count text
   let codeTextCount = 0;
   const codeBlocks = document.getElementsByClassName('code-snippet-container');
   for (let index = 0; index < codeBlocks.length; index++) {
      const codeBlock = codeBlocks[index].innerText;
      let codeWordCount = codeBlock.split(' ').length
      codeTextCount += codeWordCount;
   }
   console.log(`The code count is ${wordCount - codeTextCount}`);
   wordCount = wordCount - codeTextCount;
   timeToRead = (wordCount / wordsPerMinute) * 60;

   console.log(`It would take ${timeToRead} seconds to read this text.`); 

   const MINUTE = 60

   if (timeToRead > 0 && timeToRead <= MINUTE)
   {
      console.log(`It would take less than a minute to read.`); 
      timeText.innerText = '< 1 min';
   }
   else if (timeToRead > MINUTE && timeToRead <= MINUTE*2)
   {
      console.log(`It would take two minutes to read.`); 
      timeText.innerText = '2 mins';
   }
   else if (timeToRead > MINUTE*2 && timeToRead <= MINUTE*3)
   {
      console.log(`It would take three minutes to read.`);  
      timeText.innerText = '3 mins';
   }
   else if (timeToRead > MINUTE*3 && timeToRead <= MINUTE*4)
   {
      console.log(`It would take four minutes to read.`);  
      timeText.innerText = '4 mins';
   }
   else if (timeToRead > MINUTE*4 && timeToRead <= MINUTE*5)
   {
      console.log(`It would take five minutes to read.`);  
      timeText.innerText = '5 mins';
   }
   else if (timeToRead > MINUTE*5 && timeToRead <= MINUTE*6)
   {
      console.log(`It would take six minutes to read.`);  
      timeText.innerText = '6 mins';
   }
   else if (timeToRead > MINUTE*6 && timeToRead <= MINUTE*7)
   {
      console.log(`It would take seven minutes to read.`);  
      timeText.innerText = '7 mins';
   }
   else if (timeToRead > MINUTE*7 && timeToRead <= MINUTE*8)
   {
      console.log(`It would take eight minutes to read.`);  
      timeText.innerText = '8 mins';
   }
   else if (timeToRead > MINUTE*8 && timeToRead <= MINUTE*9)
   {
      console.log(`It would take nine minutes to read.`);  
      timeText.innerText = '9 mins';
   }
   else if (timeToRead > MINUTE*9 && timeToRead <= MINUTE*10)
   {
      console.log(`It would take nine minutes to read.`);  
      timeText.innerText = '10 mins';
   }
}

window.onload = getReadTime;

