chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === "complete" && tab.url && tab.url.startsWith("http")) {
    chrome.storage.local.get(["email", "password"], ({ email, password }) => {
      if (!email || !password) return;

      fetch("http://localhost:8000/testURL/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: tab.url,
          email: email,
          password: password
        })
      })
      .then(res => res.json())
      .then(data => {
        const jsonString = JSON.stringify(data);
        chrome.tabs.sendMessage(tabId, {
          action: "showAlert",
          data: jsonString
        });
      })
      .catch(err => {
        chrome.tabs.sendMessage(tabId, {
          action: "showAlert",
          data: "Error: " + err.message
        });
      });
    });
  }
});
