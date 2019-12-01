$( document ).ready(function() {
  //var url = $(this).data('url');
  //var item = url.queryKey['cards'];
  //changeP(item);

  renderCards(json_string);
});

function changeP(item) {
  elemento = document.getElementById('titletag');
  elemento.innerHTML = item;
}

function renderCards(json_string) {
  var cards = JSON.parse(json_string);
  elemento = document.getElementById('cards');
  elemento.innerHTML = "";
  for ( i=0; i<cards.length; i++ ) {
    renderCard(cards[i]['text'], cards[i]['image_path'], cards[i]['bg_color'], cards[i]['text_color'])
  }
}