const apiBase = 'http://127.0.0.1:5000';

document.addEventListener('DOMContentLoaded', function () {
    console.log('DOM fully loaded and parsed');
    
    // Initial loading of books
    searchBooks();

    // Event listener for form submission
    const addForm = document.getElementById('addForm');
    if (addForm) {
        console.log('addForm found');
        addForm.addEventListener('submit', addBook);
    } else {
        console.log('addForm not found');
    }
});

function addBook(event) {
    event.preventDefault();  // Prevent form submission

    console.log('addBook function called');
    
    // Get the data from the form
    const data = {
        titre: document.getElementById('titre').value,
        auteur: document.getElementById('auteur').value,
        annee: document.getElementById('annee').value,
        genre: document.getElementById('genre').value,
        disponible: document.getElementById('disponible').value
    };

    console.log('Form data:', data);

    // Send the data to the backend via POST request
    fetch(`${apiBase}/books`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log('API response:', result);
        alert(result.message || 'Book added successfully!');
        document.getElementById('addForm').reset();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('There was an error adding the book.');
    });
}

function searchBooks() {
  const title = document.getElementById('searchInput').value;
  fetch(`${apiBase}/books?title=${encodeURIComponent(title)}`)
      .then(res => res.json())
      .then(data => {
          const tbody = document.querySelector('#bookTable tbody');
          tbody.innerHTML = '';  // Clear the table

          if (data.length === 0) {
              alert('Aucun livre trouvé.');
          }

          data.forEach(book => {
              const tr = document.createElement('tr');
              tr.innerHTML = `
                  <td>${book.titre}</td>
                  <td>${book.auteur}</td>
                  <td>${book.annee}</td>
                  <td>${book.genre}</td>
                  <td>${book.disponible}</td>
                  <td><button onclick="deleteBook(${book.id})">Supprimer</button></td>
              `;
              tbody.appendChild(tr);
          });
      })
      .catch(error => {
          console.error('Error fetching books:', error);
          alert('Il y a eu une erreur lors de la recherche.');
      });
}

function deleteBook(id) {
    if (!confirm('Supprimer le livre #' + id + ' ?')) return;

    fetch(`${apiBase}/books/${id}`, { method: 'DELETE' })
        .then(res => res.json())
        .then(resp => {
            alert(resp.message || resp.error);
            searchBooks();
        });
}

function showHtml() {
    window.open(`${apiBase}/books/html`, '_blank');
}
