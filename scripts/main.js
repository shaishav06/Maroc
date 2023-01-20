// Search BUtton
$(document).on("click", ".search", function () {
  $(".search-bar").addClass("search-bar-active");
});
$(document).on("click", ".search-cancel", function () {
  $(".search-bar").removeClass("search-bar-active");
});
//LOGIN SIGN UP FORM
$(document).on("click", ".user, .already-account", function () {
  $(".form").addClass("login-active").removeClass("sign-up-active");
});
$(document).on("click", ".sign-up-btn", function () {
  $(".form").addClass("sign-up-active").removeClass("login-active");
});
$(document).on("click", ".form-cancel", function () {
  $(".form").removeClass("login-active").removeClass("sign-up-active");
});

$(document).on("click", ".wieghtloss", function () {
  $(".progress-wrapper").addClass("progress-wrapper-active");
});
// Stepper JS

// ------------step-wizard-------------
$(".step").click(function () {
    $(this).addClass("active").prevAll().addClass("active");
    $(this).nextAll().removeClass("active");
  });
  
  $(".step01").click(function () {
    $("#line-progress").css("width", "8%");
    $(".step1").addClass("active").siblings().removeClass("active");
  });
  
  $(".step02").click(function () {
    $("#line-progress").css("width", "50%");
    $(".step2").addClass("active").siblings().removeClass("active");
  });
  
  $(".step03").click(function () {
    $("#line-progress").css("width", "100%");
    $(".step3").addClass("active").siblings().removeClass("active");
  });
  