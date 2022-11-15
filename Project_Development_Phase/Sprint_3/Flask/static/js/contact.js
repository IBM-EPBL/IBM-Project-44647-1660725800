AOS.init({
  duration: 1200,
});

(function () {
  emailjs.init("user_XXXXX");
})();
document
  .getElementsByClassName("contact-form")[0]
  .addEventListener("submit", (e) => {
    e.preventDefault();
    let name = document.getElementsByClassName("fullName")[0].value;
    let email = document.getElementsByClassName("emailId")[0].value;
    let msg = document.getElementsByClassName("message")[0].value;

    var contactParams = {
      fullname: name,
      emailid: email,
      message: msg,
    };
    emailjs
      .send("service_XXXXX", "template_XXXX", contactParams)
      .then(function (res) {
        document.getElementsByClassName(
          "contact-success-message"
        )[0].style.display = "block";
        setTimeout(() => {
          document.getElementsByClassName(
            "contact-success-message"
          )[0].style.display = "none";
        }, 5000);
        document.getElementsByClassName("contact-form")[0].reset();
      });
  });
