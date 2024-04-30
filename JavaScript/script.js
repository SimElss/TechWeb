// Function to generate a random ID
function getID() {
  return (
    Math.floor(Math.random() * 100) +
    "-" +
    Math.floor(Math.random() * 100) +
    "-" +
    Math.floor(Math.random() * 100)
  );
}

// It's not inside a function because we want to apply this to call it just one time
let cards = document.querySelectorAll(".card");

// Add the random ID to the books
cards.forEach(function (card) {
  card.querySelector(".book-id").innerText = "ID: " + getID();
});

// Function to delete a card
function deleteCard(event) {
  let card = event.target.closest(".card");
  card.remove();
}

// Function to get the element after the dragging element
function getDragAfterElement(container, y) {
  // Get all the draggable elements except the dragging element in a list
  const draggableElements = [
    ...container.querySelectorAll("#book_bought:not(.dragging)"),
  ];
  // Return the element which is the closest to the dragging element
  return draggableElements.reduce(
    (closest, child) => {
      const box = child.getBoundingClientRect();
      const offset = y - box.top - box.height / 2;
      if (offset < 0 && offset > closest.offset) {
        return { offset: offset, element: child };
      } else {
        return closest;
      }
    },
    { offset: Number.NEGATIVE_INFINITY }
  ).element;
}
// Function to add the behavior to panels
const addBehaviorToPanel = (container) => {
  // Add the dragover event listeners to the panel
  container.addEventListener("dragover", (e) => {
    e.preventDefault();
    // Get the container position only if the container is the bought container
    // Indeed we don't want to move the book to the container of the books to buy
    if (container.id === "bought") {
      // Call the getDragAfterElement function to get the element after the dragging element
      const afterElement = getDragAfterElement(container, e.clientY);
      const draggable = document.querySelector(".dragging");
      // Append the dragging element if there is no element after the dragging element
      if (afterElement == null) {
        container.appendChild(draggable);
        // Insert the dragging element before the element which is after the dragging element
      } else {
        container.insertBefore(draggable, afterElement);
      }
    }
  });
};

// Function to add the behavior to books
const addBehaviorTobook = (book) => {
  // Add the dragstart event listeners to the book
  book.addEventListener("dragstart", () => {
    book.classList.add("dragging");
  });

  // Add the dragend event listeners to the book
  book.addEventListener("dragend", () => {
    book.classList.remove("dragging");
    const container = document.getElementById("to_buy");
    // Get the container position
    const rect = container.getBoundingClientRect();
    // Get the mouse position on x axe
    const mouseX = event.clientX;
    // Check if the book is inside the container of the books to buy or not
    if (mouseX < rect.left || mouseX > rect.right) {
      book.draggable = false;
      book.id = "book_bought";
    } else {
      book.draggable = true;
      book.id = "book_to_buy";
    }
  });
};

// Main function to add the behavior to books and panels
const main = () => {
  // Add the behavior to all books
  const draggable = document.querySelectorAll("#book_to_buy");
  draggable.forEach(addBehaviorTobook);

  // Add the behavior to all panels
  const container = document.querySelectorAll("[name='dropzone']");
  container.forEach(addBehaviorToPanel);

  let deleteButtons = document.querySelectorAll("#delete_button");

  // Handle the delete button click event
  deleteButtons.forEach(function (button) {
    button.addEventListener("click", deleteCard);
  });
};

// Function to add a book to the list
function addBook(name, author, price, bought) {
  // Create the card-body for the card element
  const cardBody = $('<div class="card-body">')
    .append($("<h4 class='book-title'>").text(name))
    .append($("<h5 class='book-author'>").text(author))
    .append($("<h5 class='book-price'>").text(price + "€"))
    .append($("<h6 class='book-id'>").text("ID: " + getID()))
    .append(
      $("<button class='btn btn-danger' id='delete_button'>").text("Delete")
    );

  if (bought === true) {
    // Append the card to the bought div if the book is bought and append the cardBody to the card
    const div = $("#bought");
    //Setting the card to not draggable
    const card = $('<div class="card" id="book_bought" draggable="false">');
    card.append(cardBody);
    div.append(card);
  } else {
    // Append the card to the to_buy div if the book is not bought and append the cardBody to the card
    const div = $("#to_buy");
    //Setting the card to draggable
    const card = $('<div class="card" id="book_to_buy" draggable="true">');
    card.append(cardBody);
    div.append(card);
  }
}
// Function to validate the form
function validateForm(name, author, price) {
  // Check if the fields are not empty
  if (name === "" || author === "" || price === "") {
    alert("All fields must be filled out");
    return false;
  }
  // Check if the price is a number
  if (isNaN(parseInt(price))) {
    alert("Price must be a number");
    return false;
  }
  return true;
}

// Function to handle the form submission
function onSubmitForm(event) {
  // Collect all the form data in const variables
  event.preventDefault();
  const form = $(event.target);
  const name = form.find("#name").val().trim();
  const author = form.find("#author").val().trim();
  const price = form.find("#price").val().trim();
  const bought = form.find("#sold").prop("checked");

  //Check the user's input
  if (!validateForm(name, author, price)) {
    return;
  }
  // Add the book to the list if the input is valid
  addBook(name, author, price, bought);
  // Call main to Add the attributes to the new book
  main();
}

// Run onSubmitForm function when the form is submitted
$(document).ready(function () {
  $("#book_form").on("submit", onSubmitForm);
});

// Run main function when the document is loaded
document.addEventListener("DOMContentLoaded", main);
