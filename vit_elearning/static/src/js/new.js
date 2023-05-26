
  // $(document).ready(function(){

  //   $(".filter-button").click(function(){
  //       var value = $(this).attr('data-filter');
  //       if(value == "all")
  //       {
  //         $('.filter').show('1000');
  //       }
  //       else
  //       {
  //         $(".filter").not('.'+value).hide('3000');
  //         $('.filter').filter('.'+value).show('3000');
                      
  //       }
  //     });

  //   });


            
  // $(document).ready(function() {
  //   $(".filter-button").click(function () {
  //       $(".filter-button").removeClass("active");
  //       $(this).addClass("active");   
  //   });
  // });

  var selector = '.nav li';
  $(selector).on('click', function(){
      $(selector).removeClass('active');
      $(this).addClass('active');
  });

  $("#hidden_box_btn").on('click', function () {
                    $('#hidden_box').modal('show');
                });

  var myVideo = document.getElementById("video1");
  function playPause() { 
    myVideo.play(); 
  }

  $("#btn").on('click', function() {
     $(this).hide();
     $("#btn").hide();
     $("#video1").show();
  });

  $("#link_btn").on('click', function () {
                    $('#link_box').modal('show');
                });

  // var share_btn = document.querySelector(".share_btn");
  // var tgl_btn = document.querySelector(".tgl_btn");

  // share_btn.addEventListener("click", function() {
  //   tgl_btn.classList.toggle("active");
  // })

  