/* This page for scrolling animation */
const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        // the element is in the viewport appearing only once
        observer.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.3, // the element is considered in the viewport when 30% of it is visible
  }
);

document.querySelectorAll(".card").forEach((card) => {
  observer.observe(card);
});
