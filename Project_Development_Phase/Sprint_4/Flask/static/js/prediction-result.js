$(".faq-heading").click(function () {
  $(this)
    .parent("li")
    .toggleClass("the-active")
    .find(".faq-text")
    .slideToggle();
});
