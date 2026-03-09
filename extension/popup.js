document.getElementById('analyzeBtn').addEventListener('click', async () => {
  const resultDiv = document.getElementById('status'); // Also change this to 'status' to match your HTML
  resultDiv.innerText = "Analyzing...";

  const emailData = {
    sender: "xyz@company.com",
    body: "Hello, coming 9:00pm"
  };

  try {
    const response = await fetch('http://127.0.0.1:8000/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(emailData)
    });

    const data = await response.json();
    resultDiv.innerHTML = `<b>Category:</b> ${data.category}<br><b>Priority:</b> ${data.priority}`;
  } catch (error) {
    resultDiv.innerText = "Error: Backend not running!";
  }
});