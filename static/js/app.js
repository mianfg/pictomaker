var cartas;
var imgs;


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
        imgs = new Array(cartas.length).fill(0);
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
    $('#download_window').hide()
};

//Muestra la pantalla de selección de cartas
function showCardsWindow(){
    $('#cards_window').show()
    $('#welcome_window').hide()
    $('#download_window').show()
};

function populateCards(){
    // Funcion que parsea el JSON general y lo renderiza.
    container = document.getElementById("cards_content");
    container.innerHTML = "";
    for ( i=0; i<cartas.length; i++ ) {
        //Render a card e inyectarla en el HTML
        container.innerHTML += populateCard(cartas[i],i);
    }

};

function populateCard(card, num){
    console.log(card);
    texto = `<div class="card" style="border: 4px solid rgb(${card.bg_color.toString()})" id="card-${num}">
        <img class="card-img-top" src="${getImage(num)}" id="img-${num}">
        <div class="card-body">
            <h3 class="card-title text-center" style="font-family: escolar-bold">${card.text}</h3>
            <p class="card-text text-center">${card.gramm}</p>
        </div>
        <div class="card-footer">
            <div class="btn-group-">
                <div class="btn-group" role="group" aria-label="...">
                    <button class="btn btn-primary mb-2" id="enviar" onclick="prevImage(${num})"><i
                            class="fa fa-arrow-left"></i></button>
                </div>
                <div class="btn-group" role="group" aria-label="...">
                    <button class="btn btn-primary mb-2" id="enviar" data-toggle="modal" data-target="#modalPush"><i
                            class="fa fa-camera"></i></button>
                    <button class="btn btn-primary mb-2" id="enviar" onclick="dialogText(${num})"><i
                            class="fa fa-paint-brush"></i></button>
                    <button class="btn btn-primary mb-2" id="enviar" onclick="dialogText(${num})"><i
                            class="fa fa-align-left"></i></button>
                </div>

                <div class="btn-group" role="group" aria-label="...">
                    <button class="btn btn-primary mb-2" id="enviar" onclick="nextImage(${num})"><i
                            class="fa fa-arrow-right"></i></button>
                </div>
            </div>
        </div>
    </div>`
  return texto;
};

function getImage(num) {
    return cartas[num].image_path[imgs[num]];
}

function mod(num, total) {
    var new_num = num;
    if ( new_num < 0 )
        new_num = total-1;
    if ( new_num >= total )
        new_num = 0;
    
    return new_num;
}
function prevImage(num) {
    var size = cartas[num].image_path.length;
    imgs[num] = mod(imgs[num] - 1, size);
    image = document.getElementById("img-"+num).src=getImage(num);
}
function nextImage(num) {
    var size = cartas[num].image_path.length;
    imgs[num] = mod(imgs[num] - 1, size);
    image = document.getElementById("img-"+num).src=getImage(num);
}

