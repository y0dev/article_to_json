const copyBttns = document.getElementsByClassName('copy-bttn');

for (const copyBtn of copyBttns) {
   copyBtn.addEventListener('click', (event) => {
      const container = event.currentTarget.parentElement.parentNode.childNodes;
      const code_body = container[3];
      // console.log(event);
      // console.log(code_body);
      navigator.clipboard.writeText(code_body.textContent);
   });
}

