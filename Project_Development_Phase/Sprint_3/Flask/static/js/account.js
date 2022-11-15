var showLogin = document.getElementsByClassName("showLogin")[0];
var showSignup = document.getElementsByClassName("showSignup")[0];
showLogin.addEventListener("click", () => {
  for (var i = 0; i < 3; i++) {
    document.getElementsByClassName("login")[i].style.display = "block";
    document.getElementsByClassName("signup")[i].style.display = "none";
  }
});
showSignup.addEventListener("click", () => {
  for (var i = 0; i < 3; i++) {
    document.getElementsByClassName("login")[i].style.display = "none";
    document.getElementsByClassName("signup")[i].style.display = "block";
  }
});
function checkRegisterForm() {
  var password = document.getElementsByClassName("registerPassword")[0].value;
  console.log(password);
  var status = true;
  if (password.length < 8) {
    document.getElementsByClassName("password-error")[0].innerHTML =
      "Password must be atleast 8 characters";
    console.log(password.length);
    status = false;
  }
  return status;
}
document
  .getElementsByClassName("registerPassword")[0]
  .addEventListener("keypress", () => {
    document.getElementsByClassName("password-error")[0].innerHTML = "";
  });
