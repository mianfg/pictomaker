var cartas;
var imgs;

var syntaxColors = {
    'SUST' : "#d32f2f",
    'ADJ' : "#2e7d32",
    'DET' : "#1565c0",
    'PRON' : "#d32f2f",
    'VERB' : "#ff6f00",
    'ADVERB' : "#004d40",
    'INTERJ' : "#37474f",
    'PREP' : "#c2185b",
    'CONJ' : "#c2185b",
    'OTHER' : "#eeeeee"
}

var cardtype = "color"
var changenum = -1

var types = ["SUST", "ADJ", "DET", "PRON", "VERB", "ADVERB", "INTERJ", "PREP", "CONJ", "OTHER"]

$(document).ready(function () {
    // Al iniciar la aplicación solo se ve la pantalla principal
    showWelcomeWindow();
});

// Esta función recoge la oración y pide a la API las cartas correspondientes.
function getText() {
    $.post("/textpost", {
        text: $('#input-text').val()
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


function downloadPNG() {
    vals = {
        cards: cartas,
        colors: syntaxColors,
        type: cardtype,
        images: imgs
    }
    $.post("/generate/png", {
        values: JSON.stringify(vals)
    }).done(function( data ) {
        console.log("Receiving PNG")
        
    })
    .fail(function () {
        console.log ("Ha sido imposible contactar con el servidor")
    });
}

function downloadZIP() {
    vals = {
        cards: cartas,
        colors: syntaxColors,
        type: cardtype,
        images: imgs
    }
    $.post("/generate/zip", {
        values: JSON.stringify(vals)
    }).done(function( data ) {
        console.log("Receiving ZIP")
        
    })
    .fail(function () {
        console.log ("Ha sido imposible contactar con el servidor")
    });
}

//Muestra la pantalla de inicio
function showWelcomeWindow(){
    $('#input-box').show()
    $('#generated-text').hide()
    $('#cards-div').hide()
    $('#download-buttons').hide()
};

//Muestra la pantalla de selección de cartas
function showCardsWindow(){
    $('#input-box').hide()
    $('#generated-text').show()
    $('#cards-div').show()
    $('#download-buttons').show()
};

function populateCards(){
    // Funcion que parsea el JSON general y lo renderiza.
    new_HTML = "";
    lastclose = false;

    for ( i=0; i<cartas.length; i++ ) {
        //Render a card e inyectarla en el HTML
        if ( i % 3 == 0 ) {
            new_HTML += `<div class="row">`
            lastclose = false;
        }
        
        new_HTML += populateCard(cartas[i],i);
        if ( i % 3 == 2 ) {
            new_HTML += `</div>`
            lastclose = true;
        }
    }

    if ( !lastclose )
        new_HTML += `</div>`

    document.getElementById("cards-div").innerHTML = new_HTML;
};

function populateCard(card, num){
    console.log(card);
    texto = `<div class="col-md-6 col-lg-4 mb-3 mb-md-4">
    <div class="card h-100 hover-box-shadow" style="border: 8px solid ${getColor(card.gramm)}" id="card-${num}">
      <img class="card-img-top" id="img-${num}" src="${getImage(num)}" alt="pictograma">
      <div class="card-body">
        <a href="#" data-toggle="modal" data-target="#change-text" onclick="openModalText(${num})">
          <h3 style="font-family: escolar; font-size: 40px;" id="text-${num}">${card.text}</h3>
        </a>
        <a href="#" data-toggle="modal" data-target="#change-syntax" onclick="openModalSyntax(${num})">
          <p id="syntax-${num}">${verboseSyntax(card.gramm)}</p>
        </a>
      </div>
      <div class="card-footer d-flex justify-content-between align-items-center">
        <div ${insertArrowsHTML(num, "prev")}><i class="fa fa-arrow-left"></i></div>
        <a href="#" class="badge badge-pill badge-info" data-toggle="modal"
          data-target="#custom-under-development"><i class="fa fa-camera"></i>&nbsp;&nbsp;&nbsp;Imagen</a>
        <div ${insertArrowsHTML(num, "next")}><i class="fa fa-arrow-right"></i></div>
      </div>
    </div>
  </div>`
  return texto;
};

function insertArrowsHTML(num, mode) {
    if ( cartas[num].image_path.length > 1 )
        return `class="badge badge-pill badge-primary" onclick="${mode}Image(${num})"`
    else
        return `class="badge badge-pill badge-primary-2"`
}

function getImage(num) {
    return "/static/"+cardtype+"/"+cartas[num].image_path[imgs[num]];
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

function setSyntaxColorPickerValues() {
    for ( i=0; i < types.length; i++ )
        document.getElementById('color-picker-'+types[i]).value = getColor(types[i])
}

function getColor(syntax) {
    if ( types.includes(syntax) )
        return syntaxColors[syntax];
    else
        return "#000";
}

function setSyntaxColors() {
    for ( i=0; i < types.length; i++ )
        syntaxColors[types[i]] = document.getElementById('color-picker-'+types[i]).value;
        refreshColors();
}

function verboseSyntax(syntax) {
    if (syntax == "SUST")
        return "Sustantivo";
    else if (syntax == "ADJ")
        return "Adjetivo";
    else if (syntax == "DET")
        return "Determinante"
    else if (syntax == "PRON")
        return "Pronombre";
    else if (syntax == "VERB")
        return "Verbo";
    else if (syntax == "ADVERB")
        return "Adverbio";
    else if (syntax == "INTERJ")
        return "Interjección";
    else if (syntax == "PREP")
        return "Preposición";
    else if (syntax == "CONJ")
        return "Conjunción";
    else
        return "Otro";
}

function pressColorSwitch() {
    setTimeout(function(){
        //do what you need here
    }, 100)
    if ( !document.getElementById('color-switch').checked )
        cardtype = "color"
    else
        cardtype = "bnw"
    
    refreshImages()
}

function refreshColors() {
    for ( i = 0; i < cartas.length; i++ )
        document.getElementById("card-"+i).style["border"] = "8px solid " + getColor(cartas[i].gramm)
}

function refreshImages() {
    for ( i = 0; i < cartas.length; i++ )
        document.getElementById("img-"+i).src = getImage(i)
}

function restoreSyntaxPalette() {
    prevSyntaxColors = {
        'SUST' : "#d32f2f",
        'ADJ' : "#2e7d32",
        'DET' : "#1565c0",
        'PRON' : "#d32f2f",
        'VERB' : "#ff6f00",
        'ADVERB' : "#004d40",
        'INTERJ' : "#37474f",
        'PREP' : "#c2185b",
        'CONJ' : "#c2185b",
        'OTHER' : "#eeeeee"
    }

    for ( i=0; i < types.length; i++ )
        document.getElementById('color-picker-'+types[i]).value = prevSyntaxColors[types[i]]
}

function openModalText(num) {
    document.getElementById('input-new-text').value = cartas[num].text
    changenum = num
}

function setModalText() {
    cartas[changenum].text = document.getElementById('input-new-text').value
    console.log(cartas[changenum].text)
    document.getElementById('text-'+changenum).innerHTML = cartas[changenum].text
}

function openModalSyntax(num) {
    $('input:radio[name=gridRadios]').filter('[value='+cartas[num].gramm+']').prop('checked',true)
    changenum = num
}

function setModalSyntax() {
    cartas[changenum].gramm = $('input:radio[name=gridRadios]:checked').val()
    console.log(cartas[changenum].gramm)
    document.getElementById('syntax-'+changenum).innerHTML = verboseSyntax(cartas[changenum].gramm)
    refreshColors()
}

function downloadPDF(type) {
    console.log("Downloading PDF")
}