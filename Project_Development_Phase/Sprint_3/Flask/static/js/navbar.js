(() => {
  const factorySideNav = function factorySideNav() {
    // DOM
    const showButtonEl = document.querySelector(".js-menu-show");
    const hideButtonEl = document.querySelector(".js-menu-hide");
    const sideNavEl = document.querySelector(".js-side-nav");
    const sideNavContainerEl = document.querySelector(".js-side-nav-container");
    // State
    let startX = 0;
    let currentX = 0;
    let touchingSideNav = false;
    const onTransitionEnd = function onTransitionEnd(evt) {
      sideNavEl.classList.remove("side-nav--animatable");
      sideNavEl.removeEventListener("transitionend", onTransitionEnd);
    };
    const showSideNav = function showSideNav() {
      sideNavEl.classList.add("side-nav--animatable");
      sideNavEl.classList.add("side-nav--visible");
      sideNavEl.addEventListener("transitionend", onTransitionEnd);
    };
    const hideSideNav = function hideSideNav() {
      sideNavEl.classList.add("side-nav--animatable");
      sideNavEl.classList.remove("side-nav--visible");
      sideNavEl.addEventListener("transitionend", onTransitionEnd);
    };
    const update = function update() {
      if (!touchingSideNav) return;
      requestAnimationFrame(update);
      const translateX = Math.min(0, currentX - startX);
      sideNavContainerEl.style.transform = `translateX( ${translateX}px )`;
    };
    const onTouchStart = function onTouchStart(evt) {
      if (!sideNavEl.classList.contains("side-nav--visible")) return;
      startX = evt.touches[0].pageX;
      currentX = startX;
      touchingSideNav = true;
      requestAnimationFrame(update);
    };
    const onTouchMove = function onTouchMove(evt) {
      if (!touchingSideNav) return;
      currentX = evt.touches[0].pageX;
    };
    const onTouchEnd = function onTouchEnd(evt) {
      if (!touchingSideNav) return;
      touchingSideNav = false;
      const translateX = Math.min(0, currentX - startX);
      sideNavContainerEl.style.transform = "";
      if (translateX < 0) hideSideNav();
    };
    const blockClicks = function blockClicks(evt) {
      evt.stopPropagation();
    };
    const addEventListeners = function addEventListeners() {
      showButtonEl.addEventListener("click", showSideNav);
      hideButtonEl.addEventListener("click", hideSideNav);
      sideNavEl.addEventListener("click", hideSideNav);
      sideNavContainerEl.addEventListener("click", blockClicks);
      sideNavEl.addEventListener("touchstart", onTouchStart);
      sideNavEl.addEventListener("touchmove", onTouchMove);
      sideNavEl.addEventListener("touchend", onTouchEnd);
    };
    return {
      addEventListeners,
    };
  };
  const sideNav = factorySideNav();
  sideNav.addEventListeners();
})();
