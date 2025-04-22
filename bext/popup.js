document.getElementById("save").addEventListener("click", () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  chrome.storage.local.set({ email, password }, () => {
    alert("Credentials saved.");
  });
});
