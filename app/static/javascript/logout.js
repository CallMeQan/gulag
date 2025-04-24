// Mở modal
function openModal() {
  const modal = document.getElementById("logoutModal");
  if (modal) modal.style.display = "flex";
}

// Đóng modal
function closeModal() {
  const modal = document.getElementById("logoutModal");
  if (modal) modal.style.display = "none";
}

// Xác nhận đăng xuất
function confirmLogout() {
  fetch("/logout", {
    method: "POST",
  })
    .then(() => {
      closeModal();

      // Hiện overlay/ảnh logout thành công
      document.getElementById("logoutSuccessModal").style.display = "flex";
    })
    .catch((err) => {
      console.error("Logout failed", err);
    });
}

// Chuyển về trang login
function goToLogin() {
  window.location.href = "/auth/logout";
}

// Đóng modal khi click ra ngoài
window.addEventListener("click", function (event) {
  const modal = document.getElementById("logoutModal");
  if (event.target === modal) {
    modal.style.display = "none";
  }
});
