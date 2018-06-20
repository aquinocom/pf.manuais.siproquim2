$(document).ready(function () {
  $('.collapsible').collapsible();
});


function sim() {
  
  $('#feedback-nao').prop('disabled', true);
  $('#feedback-sim').text('Sim. Obrigado!').css('color', '#444444');
  $('#feedback-sim').css({'background-color': '#EAF1DF', 'border': '3px solid #444444'});
  $('#feedback-text-agradecimento').show();  
  
}

function nao() {
  
      $('#feedback-sim').prop('disabled', true); 
      $('#feedback-nao').css({
        'background-color': '#EAF1DF',
        'color': '#444444', 'border': '3px solid #444444'}); 
      $('#feedback-text').show();
	  
     
  }

