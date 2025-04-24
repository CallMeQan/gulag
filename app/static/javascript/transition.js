document.addEventListener("DOMContentLoaded", function () {
  const overlay = document.getElementById("transition-overlay");
  const beginRunningBtn = document.getElementById("begin-running-btn");
  const homepageUrl = "/homepage";

  // Ẩn overlay ngay khi DOM sẵn sàng
  overlay.classList.add("hidden");

  // Thêm ẩn lại lần nữa sau khi toàn bộ trang (ảnh) load xong để chắc chắn
  window.addEventListener("load", () => {
    overlay.classList.add("hidden");
  });

  // FIX: Ẩn overlay khi back/forward
  window.addEventListener("pageshow", function (event) {
    overlay.classList.add("hidden");
  });

  // Bắt sự kiện khi người dùng click link
  document.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", function (e) {
      const href = this.getAttribute("href");
      if (
        href &&
        !href.startsWith("#") &&
        !href.startsWith("javascript") &&
        this.target !== "_blank"
      ) {
        e.preventDefault();
        overlay.classList.remove("hidden");

        // Đợi animation, sau đó chuyển trang
        setTimeout(() => {
          window.location.href = href;
        }, 1000); // khớp với thời gian trong CSS
      }
    });
  });

  // Bắt sự kiện click cho nút "Begin Running"
  // if (beginRunningBtn) {
  //   beginRunningBtn.addEventListener("click", function (e) {
  //     e.preventDefault();
  //     overlay.classList.remove("hidden");

  //     // Đợi animation, sau đó thực hiện hành động bạn muốn
  //     setTimeout(() => {
  //       // Ví dụ: Chuyển đến một trang cụ thể
  //       window.location.href = homepageUrl;
  //     }, 3000); // khớp với thời gian trong CSS
  //   });
  // }
});
