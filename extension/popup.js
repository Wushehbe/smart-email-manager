document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const payload = {
    sender: "xyz@company.com",
    body: "Hello, coming 9:00pm."
  };

  try {
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload)
    });

    const data = await res.json();
    document.getElementById("result").textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    document.getElementById("result").textContent = "Error: " + err;
  }
});

document.getElementById("listBtn").addEventListener("click", async () => {
  try {
    const res = await fetch("http://127.0.0.1:8000/list_emails");
    const data = await res.json();
    document.getElementById("listResult").textContent =
      JSON.stringify(data, null, 2);
  } catch (err) {
    document.getElementById("listResult").textContent = "Error: " + err;
  }
});
