document.addEventListener("DOMContentLoaded", function () {
  const modal = document.getElementById("logoutModal");

  // Mở modal
  window.openModal = function () {
    if (modal) modal.style.display = "flex";
  };

  // Đóng modal
  window.closeModal = function () {
    if (modal) modal.style.display = "none";
  };

  // Xác nhận đăng xuất
  window.confirmLogout = function () {
    window.location.href = "/logout";
  };

  // Bấm ngoài modal để đóng
  window.addEventListener("click", function (event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  });
});
