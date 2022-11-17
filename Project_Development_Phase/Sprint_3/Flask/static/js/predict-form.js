$(document).ready(function () {
  var current_fs, next_fs, previous_fs;
  var opacity;
  var current = 1;
  var steps = $("fieldset").length;
  setProgressBar(current);
  function progessBarFunction() {
    $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");
    current_fs.animate(
      { opacity: 0 },
      {
        step: function (now) {
          opacity = 1 - now;
          current_fs.css({
            display: "none",
            position: "relative",
          });
          next_fs.css({ opacity: opacity });
        },
        duration: 500,
      }
    );
    setProgressBar(++current);
  }
  $(".next").click(function () {
    var form = $("#msform");
    form.validate({
      highlight: function (element) {
        $(element).closest(".form-card").addClass("has-error");
      },
      unhighlight: function (element) {
        $(element).closest(".form-card").removeClass("has-error");
      },
      rules: {
        title: {
          required: true,
          maxlength: 8,
        },
        url: {
          required: true,
        },
      },
      messages: {
        title: {
          required: "Title required",
        },
        url: {
          required: "URL required",
        },
      },
    });
    if (form.valid() === true) {
      if ($(".title-section").is(":visible")) {
        current_fs = $(".title-section");
        next_fs = $(".url-section");
        progessBarFunction();
      } else if ($(".url-section").is(":visible")) {
        current_fs = $(".url-section");
        next_fs = $(".confirm-section");
        progessBarFunction();
      }
      next_fs.show();
      current_fs.hide();
    }
  });
  $(".previous").click(function () {
    current_fs = $(this).parent();
    previous_fs = $(this).parent().prev();
    $("#progressbar li")
      .eq($("fieldset").index(current_fs))
      .removeClass("active");
    previous_fs.show();
    current_fs.animate(
      { opacity: 0 },
      {
        step: function (now) {
          opacity = 1 - now;
          current_fs.css({
            display: "none",
            position: "relative",
          });
          previous_fs.css({ opacity: opacity });
        },
        duration: 500,
      }
    );
    setProgressBar(--current);
  });
  function setProgressBar(curStep) {
    var percent = parseFloat(100 / steps) * curStep;
    percent = percent.toFixed();
    $(".progress-bar").css("width", percent + "%");
  }
});

document
  .getElementsByClassName("sureButton")[0]
  .addEventListener("click", () => {
    document.getElementsByClassName("urltitle")[0].innerHTML =
      $(".getTitle").val();
    document.getElementsByClassName("url")[0].innerHTML = $(".getURL").val();
  });
function submitForm() {
  document.getElementsByClassName("loading-message")[0].style.display = "block";
}
