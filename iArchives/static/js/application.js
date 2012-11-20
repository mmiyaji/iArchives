!function ($) {

  $(function(){

    // Disable certain links in docs
    $('section [href^=#]').click(function (e) {
        e.preventDefault();
    });

    // make code pretty
      window.prettyPrint && prettyPrint();

    // position static twipsies for components page
    if ($(".twipsies a").length) {
      $(window).on('load resize', function () {
        $(".twipsies a").each(function () {
          $(this)
            .tooltip({
              placement: $(this).attr('title')
            , trigger: 'manual'
            })
            .tooltip('show')
        });
      });
    }

    // add tipsies to grid for scaffolding
    if ($('#grid-system').length) {
      $('#grid-system').tooltip({
          selector: '.show-grid > div'
        , title: function () { return $(this).width() + 'px' }
      });
    }

    // fix sub nav on scroll
    var $win = $(window)
      , $nav = $('.subnav')
      , navTop = $('.subnav').length && $('.subnav').offset().top - 40
      , isFixed = 0

      processScroll();
    // hack sad times - holdover until rewrite for 2.1
    $nav.on('click', function () {
      if (!isFixed) setTimeout(function () {  $win.scrollTop($win.scrollTop() - 47) }, 10)
    });

      $win.on('scroll', processScroll);
      $('.img_popover').popover({
          placement:'bottom'
      });

    function processScroll() {
        var i, scrollTop = $win.scrollTop();
      if (scrollTop >= navTop && !isFixed) {
          isFixed = 1;
          $nav.addClass('subnav-fixed');
      } else if (scrollTop <= navTop && isFixed) {
          isFixed = 0;
          $nav.removeClass('subnav-fixed');
      }
    }
      // 写真のスライドショー
      $('#myCarousel').carousel();
      $('.carousel').carousel({
          // default 5000
          interval: 10000
      });
      $("#author_table tbody tr").click(function () {
          document.location = "/author/"+$(this).attr("id").split("_")[1]+"/";
      });
      $("#atoggle").click(function(){
          if($(this).attr('checked')){
              $('.isarchive').attr('checked', true);
          }else{
              $('.isarchive').attr('checked', false);
          }
      });
  });

// Modified from the original jsonpi https://github.com/benvinegar/jquery-jsonpi
$.ajaxTransport('jsonpi', function(opts, originalOptions, jqXHR) {
  var url = opts.url;
  return {
    send: function(_, completeCallback) {
      var name = 'jQuery_iframe_' + jQuery.now()
        , iframe, form

      iframe = $('<iframe>')
        .attr('name', name)
        .appendTo('head')

      form = $('<form>')
        .attr('method', opts.type) // GET or POST
        .attr('action', url)
        .attr('target', name)

      $.each(opts.params, function(k, v) {

        $('<input>')
          .attr('type', 'hidden')
          .attr('name', k)
          .attr('value', typeof v == 'string' ? v : JSON.stringify(v))
          .appendTo(form)
      })

      form.appendTo('body').submit()
    }
  }
})

}(window.jQuery)
