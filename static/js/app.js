var cartas;
var imgs;

/*$('a[href="#"]').click(function(event){

    event.preventDefault();

});*/

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
};

var staticbase = "https://raw.githubusercontent.com/mianfg/pictomaker/master/static/"
var cardtype = "color"
var selected_search_path = ""
var changenum = -1
var search_paths = []

var types = ["SUST", "ADJ", "DET", "PRON", "VERB", "ADVERB", "INTERJ", "PREP", "CONJ", "OTHER"]

$(document).ready(function () {
    // Al iniciar la aplicación solo se ve la pantalla principal
    showWelcomeWindow();
    var termTemplate = "<span class='ui-autocomplete-term'>%s</span>";
    
    /* $('#search').autocomplete({
        source: ['java', 'javascript', 'asp.net', 'PHP'],
        open: function(e,ui) {
            var
                acData = $(this).data('autocomplete'),
                styledTerm = termTemplate.replace('%s', acData.term);

            acData
                .menu
                .element
                .find('a')
                .each(function() {
                    var me = $(this);
                    me.html( me.text().replace(acData.term, styledTerm) );
                });
        }
    }); */
    var charMap = {
        "à": "a", "â": "a", "é": "e", "è": "e", "ê": "e", "ë": "e",
        "ï": "i", "î": "i", "ô": "o", "ö": "o", "û": "u", "ù": "u"
    };
    var normalize = function (input) {
        $.each(charMap, function (unnormalizedChar, normalizedChar) {
           var regex = new RegExp(unnormalizedChar, 'gi');
           input = input.replace(regex, normalizedChar);
        });
        return input;
       }

       var queryTokenizer = function(q) {
        var normalized = normalize(q);
        return Bloodhound.tokenizers.whitespace(normalized);
    };
    
    var words_suggestion = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.whitespace,
        queryTokenizer: queryTokenizer,
        prefetch: "/static/words.json"
    });
        
		
    $('#scrollable-dropdown-menu .typeahead').typeahead(null, {
        highlight: true,
        name: 'words',
        limit: 100,
        source: words_suggestion
    });
           /* { minLength: 1,
                limit: 3 },
			{ source: countries_suggestion }
        );*/
    $('#picture-scroll').hide()
    $('#empty-search-notice').hide()
});


// Esta función recoge la oración y pide a la API las cartas correspondientes.
function getText() {
    if ( $('#input-text').val() == "" ) {
        alertNoText();
    } else {
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
}

function searchPictos(avoid_error_message=false) {
    $('#picture-scroll').hide()
    $('#empty-search-notice').hide()
    $.post("/imagesearch", {
        text: $('#input-search').val()
    }).done(function( data ) {
        search_paths = data['results']
        populateSearchCards();
        if ( search_paths.length > 0 ) {
            $('#picture-scroll').show()
            $('#empty-search-notice').hide()
        } else {
            $('#picture-scroll').hide()
            if (!avoid_error_message)
                $('#empty-search-notice').show()
        }
        
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
        url = data['url']
        filename = data['filename']
        console.log("Received PNG: " + url)
        var a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()
        deleteFromServer(url)
    })
    .fail(function () {
        console.error("Ha sido imposible contactar con el servidor")
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
        url = data['url']
        filename = data['filename']
        console.log("Received ZIP: " + url)
        var a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()
        deleteFromServer(url)
    })
    .fail(function () {
        console.error("Ha sido imposible contactar con el servidor")
    });
}

function deleteFromServer(dir) {
    vals = {
        url: dir
    }
    $.post("/generate/delete", {
        values: JSON.stringify(vals)
    }).done(function( data ) {
        console.log("Deleted from server: " + dir)
    })
    .fail(function () {
        console.error("Could not delete from server: " + dir);
    })
}

$("#input-text").keyup(function(event) {
    if (event.keyCode === 13) {
        getText();
    }
});

$("#input-search").keyup(function(event) {
    if (event.keyCode === 13) {
        searchPictos();
    }
});

//Muestra la pantalla de inicio
function showWelcomeWindow(){
    $('#input-box').show()
    $('#generated-text').hide()
    $('#cards-div').hide()
    $('#download-buttons').hide()
    $('#notext-alert').hide()
};

function alertNoText(){
    $('#notext-alert').show()
}

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
    //lastclose = false;

    new_HTML += `<div class="row">`
    for ( i=0; i<cartas.length; i++ )
        new_HTML += populateCard(cartas[i],i);
    new_HTML += `<div>`

    /*for ( i=0; i<cartas.length; i++ ) {
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
        new_HTML += `</div>`*/

    document.getElementById("cards-div").innerHTML = new_HTML;
};

function populateSearchCards() {
    new_HTML = "";
    //lastclose = false;

    new_HTML += `<div class="row top-buffer" style="width:100%;">`;
    for ( i=0; i<search_paths.length; i++ )
        new_HTML += populateSearchCard(search_paths[i]);
    new_HTML += `</div>`;
    
    /*for ( i = 0; i < search_paths.length; i++ ) {
        if ( i % 3 == 0 ) {
            if ( i == 0 ) {
                new_HTML += `<div class="row top-buffer" style="width:100%;">`
            } else {
                new_HTML += `<div class="row" style="width:100%;">`
            }
        }
        new_HTML += populateSearchCard(search_paths[i]);
        if ( i % 3 == 2 ) {
            new_HTML += `</div>`
            lastclose = true;
        }
    }

    if ( !lastclose )
        new_HTML += `</div>`*/

    document.getElementById("search-cards-div").innerHTML = new_HTML;
}

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
        <a role="button" ${insertArrowsHTML(num, "prev")}><i class="fa fa-arrow-left"></i></a>
        <a role="button" class="badge badge-pill badge-info" data-toggle="modal"
          data-target="#custom-under-development" onclick="openModalImage(${num})"><i class="fa fa-camera"></i>&nbsp;&nbsp;&nbsp;Cambiar imagen</a>
        <a role="button" ${insertArrowsHTML(num, "next")}><i class="fa fa-arrow-right"></i></a>
      </div>
    </div>
  </div>`
  return texto;
};

function populateSearchCard(path) {
    border = ""
    if (false) //wip
        border = `style="border: 8px solid #1565c0"`
    texto = `<div class="col-md-6 col-lg-4 mb-3 mb-md-4"><div class="card h-100 hover-box-shadow" ${border} id="card-${path}">
    <img class="card-img-top selectable" id="img-${path}" src="${staticbase+cardtype+"/"+path}" alt="pictograma" onclick="changeImage('${path}')"> 
    </div></div>`
    return texto;
}

function changeImage(path) {
    for ( i = 0; i < search_paths.length; i++ )
        document.getElementById("card-"+search_paths[i]).style.border = ""
    document.getElementById("card-"+path).style.border = "4px solid #1565c0"
    selected_search_path = path;
    console.log("NEW selected path: "+selected_search_path)
}

function openModalImage(num) {
    $('#picture-scroll').hide()
    $('#empty-search-notice').hide()
    document.getElementById('input-search').value = cartas[num].text;
    changenum = num;
    searchPictos(true)
}

function setModalImage() {
    imgs[changenum] = cartas[changenum].image_path.indexOf(selected_search_path);
    if ( imgs[changenum] == -1 ) {
        imgs[changenum] = cartas[changenum].image_path.length;
        cartas[changenum].image_path.push(selected_search_path);
        document.getElementById("prev-arrow-"+changenum).className = "badge badge-pill badge-primary"
        document.getElementById("next-arrow-"+changenum).className = "badge badge-pill badge-primary"
    }
    
    console.log(imgs)
    console.log(cartas[changenum].image_path);
    refreshImages();
}

function insertArrowsHTML(num, mode) {
    if ( cartas[num].image_path.length > 1 )
        return `class="badge badge-pill badge-primary" onclick="${mode}Image(${num})" id="${mode}-arrow-${num}"`
    else
        return `class="badge badge-pill badge-primary-2" onclick="${mode}Image(${num})" id="${mode}-arrow-${num}"`
}

function getImage(num) {
    return staticbase+cardtype+"/"+cartas[num].image_path[imgs[num]];
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

function verifyURL() {
    $('#invalid-image-notice').hide()
    $('#input-text').val() = ""
    verifyImageURL($('#input-url').val(), function(imageExists) {
        if (imageExists)
            console.log("Image exists")
        else {
            console.log("Image does not exist")
            $('#invalid-image-notice').show()
        }
    });
}

function verifyImageURL(url, callBack) {
    var img = new Image();
    img.src = url;
    img.onload = function () {
        callBack(true);
    };
    img.onerror = function () {
        callBack(false);
    };
}