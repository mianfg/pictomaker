
var cartas;



$(document).ready(function () {
    // Al iniciar la aplicación solo se ve la pantalla principal
    showWelcomeWindow();


});

// Esta función recoge la oración y pide a la API las cartas correspondientes.
function getText() {
    $.post("/textpost", {
        text: $('#oracion').val()
    }).done(function( data ) {
        cartas = data['cards'];
        console.log(cartas);
        // Una vez tenemos las cartas, las renderizamos
        populateCards();
        showCardsWindow();
        
    })
    .fail(function () {
        console.log ("Ha sido imposible contactar con el servidor")
        //Lo suyo es que saliera aquí un mensaje en el formulario
    });
}


//Muestra la pantalla de inicio
function showWelcomeWindow(){
    $('#cards_window').hide()
    $('#welcome_window').show()
};

//Muestra la pantalla de selección de cartas
function showCardsWindow(){
    $('#cards_window').show()
    $('#welcome_window').hide()
};

function populateCards(){
    // Funcion que parsea el JSON general y lo renderiza.
    container = document.getElementById("card_deck");
    container.innerHTML = "";
    for ( i=0; i<cartas.length; i++ ) {
        //Render a card e inyectarla en el HTML
        container.innerHTML += populateCard(cartas[i],i);
    }

};

function populateCard(card, num){
    console.log(card);
    texto = `<div class="card" style="width: 300px;" id="card-${num}">
    <img class="card-img-top" src="${card['image_path']}" alt="Card image cap">
    <div class="card-body">
      <h5 class="card-title">${card.text}</h5>
      <p class="card-text">SUSTANTIVO</p>
    </div>
    <div class="card-footer">
      <small class="text-muted">Last updated 3 mins ago</small>
    </div>
  </div>`;
  return texto;
};