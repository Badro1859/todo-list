jQuery(function ($) {

    $(".sidebar-dropdown > a").click(function() {
        $(".sidebar-submenu").slideUp(200);
        if ($(this).parent().hasClass("active")) {
            $(".sidebar-dropdown").removeClass("active");
            $(this).parent().removeClass("active");
        } else {
            $(".sidebar-dropdown").removeClass("active");
            $(this).next(".sidebar-submenu").slideDown(200);
            $(this).parent().addClass("active");
        }
    });

    $("#sidebarCollapse").click(function() {
        $(".page-wrapper").toggleClass("toggled");
    });

    $("#finishedToastBtn").click(function() {
      $("#finishedToast").toast("show");
    });
    $("#deleteToastBtn").click(function() {
      $("#deleteToast").toast("show");
    });

    $(".search").click(function(e){
        // preventing from page reload and default actions
        e.preventDefault();
      
        // get the type (all, complete, primary)
        var searchType = $(this).attr('value');

        if (searchType == "other"){
          searchType = $('#search_input').val();
        }

        // GET AJAX request
        $.ajax({
            type: 'GET',
            url: '',
            headers: {
              "X-Requested-With": "XMLHttpRequest",
            },
            dataType : "json",
            data: {"search-area": searchType },
            success: function (response) {
              $("#display-area").html(response.tasks)
            },
            error: function (response) {
                console.log(response)
            }
        })
    });


    let loadForm = function() {
        let btn = $(this);
        $.ajax({
          url: btn.attr("href"),
          type: 'get',
          dataType: 'json',
          beforeSend: function () {
            $("#modal").modal("show");
          },
          success: function (data) {
            $("#modal .modal-content").html(data.html_form);
          }
        });
        return false;
    };

    let completeForm = function() {
      let btn = $(this);
      let complete = true;

      $.ajax({
        url: btn.attr("href"),
        type: 'GET',
        dataType: 'json',
        data: {"complete": complete},
        beforeSend: function () {
          $("#modal").modal("show");
        },
        success: function (data) {
          $("#modal .modal-content").html(data.html_form);
        },
      });
      return false;
    };

    let reload = function() {
      location.reload();
    }
    
    $("body").on('click', '.js-load-form', loadForm);
    $("body").on('click', '.js-complete-form', completeForm);
    $("body").on('click', '.js-reload-list', reload);
});