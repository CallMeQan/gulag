let timeoutId;

function showPopup() {
  const popup = document.getElementById('.congrats_message');
  popup.style.display = 'block';

  timeoutId = setTimeout(() => {
    popup.style.display = 'none';
  }, 5000);
}

function cancelPopup() {
  clearTimeout(timeoutId);
  document.getElementById('.congrats_message').style.display = 'none';
}