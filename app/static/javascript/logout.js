const modal = document.getElementById("logoutModal");

function openModal() {
  modal.style.display = "flex";
}

function closeModal() {
  modal.style.display = "none";
}

function confirmLogout() {
  // Redirect hoặc gửi request logout
  window.location.href = "{{ url_for('auth.logout') }}"; // Tùy theo route logout
}

// Đóng khi click ra ngoài modal-content
window.onclick = function (event) {
  if (event.target === modal) {
    closeModal();
  }
};
