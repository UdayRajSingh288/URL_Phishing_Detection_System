chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === "showAlert" && message.data) {
    alert(message.data);
  }
});
