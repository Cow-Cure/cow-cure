let menu = document.querySelector("#menu-btn");
let heading = document.querySelector(".heading");

menu.onclick = () => {
  menu.classList.toggle("fa-times");
  heading.classList.toggle("active");
};

window.onscroll = () => {
  menu.classList.remove("fa-times");
  heading.classList.remove("active");
};

// let btn4 = document.querySelector("#buttonsearch");
// let search = document.querySelector(".Searching");

// btn4.onclick = () => {
//   btn4.classList.toggle("fa-times");
//   search.classList.toggle("active");
// };

window.onscroll = () => {
  btn4.classList.remove("fa-times");
  search.classList.remove("active");
};

// ---------- Search Diseases ----------- //

function fetchSuggestions() {
  const query = document.getElementById('inputbox').value;
  const dropdown = document.getElementById('dropdown');
  if (query.length > 0) {
      fetch(`/search_disease?q=${query}`)
          .then(response => response.json())
          .then(data => {
              dropdown.innerHTML = '';
              if (data.length > 0) {
                  data.forEach(disease => {
                      const listItem = document.createElement('li');
                      listItem.textContent = disease;
                      listItem.onclick = () => redirectToDiseasePage(disease);
                      dropdown.appendChild(listItem);
                  });
                  dropdown.style.display = 'block';
              } else {
                  dropdown.style.display = 'none';
              }
          });
  } else {
      dropdown.innerHTML = '';
      dropdown.style.display = 'none';
  }
}

function redirectToDiseasePage(disease) {
  window.location.href = `/disease_info/${disease}`;
}

// Close dropdown when clicking outside
document.addEventListener('click', function(event) {
  const inputbox = document.getElementById('inputbox');
  const dropdown = document.getElementById('dropdown');
  if (!inputbox.contains(event.target) && !dropdown.contains(event.target)) {
      dropdown.style.display = 'none';
  }
});



// -------Queries Form-------- //

const scriptURL='https://script.google.com/macros/s/AKfycbzTWUFoRSDt9R-5g4OO_w2SKg2IpjyZNZq3pt6E9NDTaSiWB9py7IS2WwGQG-0Ez06F/exec '
const form=document.forms['queries-form']

form.addEventListener('submit', e => {
  e.preventDefault();

  // Validate form
  const name = form.querySelector('input[name="Name"]').value;
  const email = form.querySelector('input[name="Email"]').value;
  const query = form.querySelector('textarea[name="Query"]').value;
  
  // Check if any field is empty
  if (!name || !email || !query) {
      alert('Please fill in all fields.');
      return;
  }
  
  // Validate email format
  const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  if (!emailPattern.test(email)) {
      alert('Please enter a valid email address.');
      return;
  }

  fetch(scriptURL, { method: 'POST', body: new FormData(form) })
    .then(response => response.json())
    .then(data => {
      if (data.result === 'success') {
        alert('Thank you! Your query has been submitted successfully.');
        form.reset(); // Optional: Reset the form after submission
      } else {
        alert(`Error: ${data.error}`);
      }
    })
    .catch(error => console.error('Error!', error.message));
});

// Intro Screen

let intro = document.querySelector('.intro');
let logo = document.querySelector('.logo-header');
let logoSpan = document.querySelectorAll('.intro-logo');

window.addEventListener('DOMContentLoaded', ()=>{
    setTimeout(()=>{

        logoSpan.forEach((span, idx)=>{
            setTimeout(()=>{
                span.classList.add('active');
            }, (idx+1)*70)
        });

        setTimeout(()=>{
            logoSpan.forEach((span,idx)=>{
                setTimeout(()=>{
                    span.classList.remove('active');
                    span.classList.add('fade');
                }, (idx+1)*50)
            })
        },1500)

        setTimeout(()=>{
            intro.style.top='-100vh';
        },1800)
    })
})