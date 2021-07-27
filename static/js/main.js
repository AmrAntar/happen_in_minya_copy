// var interval;
// function startTicker(){
//     $('#news2 p:first').slideUp(function(){
//         $(this).appendTo($('#news2')).slideDown();
//     });
// }

// setInterval(startTicker, 3000);

// function stopTicker(){
//     clearInterval(interval);
// }
//
// $(document).ready(function(){
//     interval = setInterval(startTicker, 3000);
//     $('#news2').hover(function(){
//         stopTicker();
//     }, function(){
//         interval = setInterval(startTicker, 3000);
//         });
// });
//




//start button to up 

var btn = $('#button');

$(window).scroll(function() {
  if ($(window).scrollTop() > 300) {
    btn.addClass('show');
  } else {
    btn.removeClass('show');
  }
});

btn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:0}, '300');
});


//end button to up




// start jquery tickers
$(document).ready(function(){

$('.myWrapper').easyTicker({
    direction: 'up',
    easing: 'swing',
    speed: 'slow',
    interval: 2000,
    height: 'auto',
    visible: 0,
    mousePause: true,
    controls: {
        up: '',
        down: '',
        toggle: '',
        playText: 'Play',
        stopText: 'Stop'
    },
    callbacks: {
        before: false,
        after: false
    }
});

});
// end jquery tickers